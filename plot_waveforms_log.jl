using DataFrames, CSV, Statistics, Plots
filename = "your_filepath_to_csv"
data = CSV.read(filename, DataFrame; delim = ',', skipto=9)  #skip the csv header containing metadata

time_strings = data[9:end, 1]  #table gets read in as string instead of float
voltage_strings = data[9:end, 2]

times = parse.(Float64, time_strings) #parse the strings to float64
voltages = parse.(Float64, voltage_strings)

#--------generate plot-----------
mean_voltage = mean(voltages)
line1 = mean_voltage + 0.01 #plot additional lines around the mean if necessary
line2 = mean_voltage - 0.01
line3 = mean_voltage + 0.03
line4 = mean_voltage - 0.03

plot(times, voltages, label="Output Voltage", color=:blue, linewidth=1.5, grid=true, gridlinewidth = 2)
hline!([mean_voltage], linestyle=:dash, color=:black, label="Mean")
hline!([line1, line2], linestyle=:dash, color=:red, label="±10mV")
hline!([line3, line4], linestyle=:dash, color=:green, label="±30mV")

# Formatting
title!("Time Series Plot of Waveforms Data Log")
xlabel!("Time (s)")
ylabel!("Voltage (V)")
