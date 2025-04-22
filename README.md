The Julia CSV parser interprets the time and voltage columns from Analog Discovery oscilloscope data as strings instead of as numbers. The function readwaveforms takes in a filepath and a skipto value, and returns two vectors of type Float64. 

To find the correct skipto value for your data, open the CSV a spreadsheet program and note the first row number after the metadata ends. This may be different from one file to another, but should be consistent across multiple CSVs if you are using the same workspace in Waveforms. 

Example code to plot the data and lines around the mean can be seen in plot_waveforms_log.jl. 
