import numpy as np
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