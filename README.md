The Julia CSV parser interprets the time and voltage columns from Analog Discovery oscilloscope data as strings instead of as numbers. The function readwaveforms takes in a filepath and a skipto value, and returns two vectors of type Float64. 

To find the correct skipto value for your data, open the CSV a spreadsheet program and note the first row number after the metadata ends. This may be different from one file to another, but should be consistent across multiple CSVs if you are using the same workspace in Waveforms. 

Example code to plot the data and lines around the mean can be seen in plot_waveforms_log.jl. 

plot_contour.py: plots an interpolated contour with or without the underlying scatter points. can be called using this example, and generates the plot below:
```python
plot_contour(
    table=combined_df,
    title="Generic Title",
    subtitle="Data generated on August 5, 2025",
    title_fontsize=18,
    subtitle_fontsize=12,
    colorbar_label="Values (units)",
    show_scatter=0,
    figsize=(12, 10),
    cmap="viridis"
)
```
<!--![Example plot showing random data scattered over Texas, Oklahoma, and Arkansas](https://github.com/skylerreid/Assets/blob/main/Figure_1.jpeg)-->
