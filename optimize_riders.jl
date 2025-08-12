using CSV, DataFrames
using JuMP, HiGHS 

# Load the data
df = CSV.read("pinkbike_riders.csv", DataFrame)

budget = 1_500_000
model = Model(HiGHS.Optimizer)  

@variable(model, x[1:nrow(df)], Bin)

# Objective: maximize points
@objective(model, Max, sum(df.points[i] * x[i] for i in 1:nrow(df)))

# Budget
@constraint(model, sum(df.cost[i] * x[i] for i in 1:nrow(df)) <= budget)

# Gender constraints
@constraint(model, sum(x[i] for i in 1:nrow(df) if df.gender[i] == "Male") == 4)
@constraint(model, sum(x[i] for i in 1:nrow(df) if df.gender[i] == "Female") == 2)

# Injury constraint: no injured riders
@constraint(model, sum(x[i] for i in 1:nrow(df) if df.injured[i] == 1) == 0)

optimize!(model)

chosen_indices = [i for i in 1:nrow(df) if value(x[i]) > 0.5]
chosen_team = df[chosen_indices, :]

println("Chosen Team:")
println(chosen_team)
println("Total Points: ", sum(chosen_team.points))
println("Total Cost: ", sum(chosen_team.cost))
