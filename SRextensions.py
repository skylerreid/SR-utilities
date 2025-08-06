import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import math

def projectilestats(speed, angle, start_height):
    g = 9.80665
    angle = np.deg2rad(angle)

    horz_speed = speed*np.cos(angle)
    vert_speed = speed*np.sin(angle)

    rise_height = (vert_speed^2)/(2*g)
    rise_time = (2*rise_height)/(vert_speed)

    time_of_flight = rise_time+fall_time
    fall_time = math.sqrt(2*(start_height + rise_height)/g)
    
    range = (time_of_flight)*horz_speed
    
    return [range, time_of_flight, rise_height]

def moving_avg(signal, window_size):
    kernel = np.full(window_size, 1.0 / window_size)
    smoothed = np.convolve(signal, kernel, mode='same')  # same output size
    return smoothed

def plot_contour(
    table: pd.DataFrame,
    title: str,
    figsize: tuple | float = 10,
    cmap: str = 'viridis',
    show_scatter: int = 1,
    subtitle: str = None,
    title_fontsize: int = 14,
    subtitle_fontsize: int = 12,
    colorbar_label: str = 'Value',
    show_labels: bool = True
):
    if not isinstance(table, pd.DataFrame) or not all(col in table.columns for col in ['latitude', 'longitude', 'value']):
        print("Error: Input table must be a Pandas DataFrame with 'latitude', 'longitude', and 'value' columns.")
        return

    # Extract data
    latitudes = table['latitude'].values
    longitudes = table['longitude'].values
    values = table['value'].values

    # Plot extent with margin
    lat_min, lat_max = latitudes.min(), latitudes.max()
    lon_min, lon_max = longitudes.min(), longitudes.max()
    lat_range = lat_max - lat_min
    lon_range = lon_max - lon_min
    lat_margin = lat_range * 0.25
    lon_margin = lon_range * 0.25
    plot_lat_min = lat_min - lat_margin
    plot_lat_max = lat_max + lat_margin
    plot_lon_min = lon_min - lon_margin
    plot_lon_max = lon_max + lon_margin

    # Interpolation grid
    grid_lon, grid_lat = np.meshgrid(
        np.linspace(plot_lon_min, plot_lon_max, 100),
        np.linspace(plot_lat_min, plot_lat_max, 100)
    )
    grid_values = griddata(
        (longitudes, latitudes),
        values,
        (grid_lon, grid_lat),
        method='linear'
    )

    # Handle figsize
    if isinstance(figsize, (int, float)):
        fig_width, fig_height = figsize, figsize
    elif isinstance(figsize, tuple) and len(figsize) == 2:
        fig_width, fig_height = figsize
    else:
        print("Warning: Invalid figsize. Using default (10, 10).")
        fig_width, fig_height = 10, 10

    # Plot setup
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([plot_lon_min, plot_lon_max, plot_lat_min, plot_lat_max], crs=ccrs.PlateCarree())

    # Features
    ax.add_feature(cfeature.STATES, edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

    # Contour
    contour_fill = ax.contourf(
        grid_lon, grid_lat, grid_values,
        levels=20, cmap=cmap,
        transform=ccrs.PlateCarree()
    )

    # Optional scatter
    if show_scatter == 1:
        ax.scatter(
            longitudes, latitudes, c=values, cmap=cmap, s=10,
            edgecolor='k', linewidth=0.5, transform=ccrs.PlateCarree(), zorder=2
        )

    # Colorbar
    cbar = fig.colorbar(contour_fill, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)
    cbar.set_label(colorbar_label)

    # Gridlines & lat/lon labels
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, linestyle='--', alpha=0.6)
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = show_labels
    gl.bottom_labels = show_labels

    # Axis labels
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Main title
    ax.set_title(title, fontsize=title_fontsize)

    # Subtitle (below)
    if subtitle:
        fig.text(0.5, 0.01, subtitle, ha='center', fontsize=subtitle_fontsize)

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.show()
