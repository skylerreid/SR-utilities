using DataFrames, CSV

function read_waveforms(filename::String, start::Int)
    # Read the CSV file into a DataFrame
    data = CSV.read(filename, DataFrame; delim = ',', skipto=start)

    time_strings = data[9:end, 1]  #table gets read in as string instead of float
    voltage_strings = data[9:end, 2]

    times = parse.(Float64, time_strings) #parse the strings to float64
    voltages = parse.(Float64, voltage_strings)

    return times, voltages
end