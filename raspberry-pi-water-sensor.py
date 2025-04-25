#!/usr/bin/env python3
"""
Water Sensor Monitor for Raspberry Pi 5

This script:
1. Reads water sensor data from an Arduino via USB serial connection
2. Displays the data in real-time with Matplotlib
3. Shows warnings when moisture levels exceed thresholds
4. Exports the data to a CSV file
"""

import serial
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
import numpy as np
import threading
import os

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Change this to match your Arduino's port (or /dev/ttyACM0)
BAUD_RATE = 9600              # Match this to your Arduino's baud rate
WARNING_THRESHOLD = 70        # Warning threshold (%) - adjust based on your needs
MAX_DATA_POINTS = 100         # Number of data points to display
CSV_FILENAME = f"water_sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Global variables for data storage
timestamps = []
moisture_values = []
warning_flags = []
is_running = True

def setup_serial():
    """Establish connection with Arduino"""
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to Arduino on {SERIAL_PORT}")
        time.sleep(2)  # Allow time for Arduino to reset
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        print("Please check connections and port name.")
        exit(1)

def read_sensor_data(ser):
    """Read and parse data from Arduino"""
    global timestamps, moisture_values, warning_flags
    
    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Moisture Level (%)', 'Warning'])
        
        while is_running:
            try:
                if ser.in_waiting > 0:
                    # Read line from Arduino (expects format: "moisture_percent")
                    line = ser.readline().decode('utf-8').strip()
                    
                    try:
                        # Parse the moisture value
                        value = float(line)
                        current_time = datetime.now()
                        timestamp = current_time.strftime('%H:%M:%S')
                        
                        # Check if value exceeds warning threshold
                        warning = value > WARNING_THRESHOLD
                        
                        # Append to data lists
                        timestamps.append(timestamp)
                        moisture_values.append(value)
                        warning_flags.append(warning)
                        
                        # Keep only the most recent MAX_DATA_POINTS
                        if len(timestamps) > MAX_DATA_POINTS:
                            timestamps.pop(0)
                            moisture_values.pop(0)
                            warning_flags.pop(0)
                        
                        # Write to CSV
                        csv_writer.writerow([current_time.strftime('%Y-%m-%d %H:%M:%S'), value, warning])
                        csvfile.flush()  # Ensure data is written immediately
                        
                        print(f"Moisture: {value}%, Warning: {warning}")
                    except ValueError:
                        print(f"Received invalid data: {line}")
            except Exception as e:
                print(f"Error reading from serial port: {e}")
                time.sleep(1)
            
            time.sleep(0.1)  # Small delay to prevent CPU hogging

def setup_plot():
    """Initialize the matplotlib plot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title('Water Sensor Data')
    plt.xlabel('Time')
    plt.ylabel('Moisture Level (%)')
    
    # Create a horizontal line for the warning threshold
    ax.axhline(y=WARNING_THRESHOLD, color='r', linestyle='--', alpha=0.7, 
               label=f'Warning Threshold ({WARNING_THRESHOLD}%)')
    
    # Add color regions for interpretation
    ax.axhspan(0, 30, alpha=0.2, color='red', label='Dry (0-30%)')
    ax.axhspan(30, 70, alpha=0.2, color='yellow', label='Moderate (30-70%)')
    ax.axhspan(70, 100, alpha=0.2, color='blue', label='Wet (70-100%)')
    
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    return fig, ax

def update_plot(frame, ax):
    """Update function for matplotlib animation"""
    ax.clear()
    
    # Add the color regions
    ax.axhspan(0, 30, alpha=0.2, color='red', label='Dry (0-30%)')
    ax.axhspan(30, 70, alpha=0.2, color='yellow', label='Moderate (30-70%)')
    ax.axhspan(70, 100, alpha=0.2, color='blue', label='Wet (70-100%)')
    
    # Add the threshold line
    ax.axhline(y=WARNING_THRESHOLD, color='r', linestyle='--', alpha=0.7, 
               label=f'Warning Threshold ({WARNING_THRESHOLD}%)')
    
    # Plot the moisture data
    if moisture_values:
        # Create line plot
        ax.plot(range(len(timestamps)), moisture_values, '-o', color='green', markersize=4, alpha=0.7)
        
        # Highlight warning points
        for i in range(len(timestamps)):
            if warning_flags[i]:
                ax.plot(i, moisture_values[i], 'ro', markersize=6)  # Red circle for warnings
    
    # Set x-axis tick labels to show timestamps
    if timestamps:
        # Only show a subset of timestamps to avoid overcrowding
        step = max(1, len(timestamps) // 10)
        ax.set_xticks(range(0, len(timestamps), step))
        ax.set_xticklabels([timestamps[i] for i in range(0, len(timestamps), step)], rotation=45)
    
    # Add labels and grid
    ax.set_title('Water Sensor Data')
    ax.set_xlabel('Time')
    ax.set_ylabel('Moisture Level (%)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    
    # Set y-axis limits to 0-100% with some padding
    ax.set_ylim(-5, 105)
    
    plt.tight_layout()

def main():
    """Main function to run the program"""
    global is_running
    
    print("Water Sensor Monitor for Raspberry Pi")
    print(f"Data will be saved to {CSV_FILENAME}")
    
    # Connect to Arduino
    ser = setup_serial()
    
    # Create thread for reading sensor data
    data_thread = threading.Thread(target=read_sensor_data, args=(ser,))
    data_thread.daemon = True
    data_thread.start()
    
    # Setup plot
    fig, ax = setup_plot()
    
    # Create animation that updates every 500ms
    ani = animation.FuncAnimation(fig, update_plot, fargs=(ax,), interval=500)
    
    # Show plot (this blocks until the window is closed)
    plt.show()
    
    # Cleanup
    is_running = False
    data_thread.join(timeout=1)
    ser.close()
    print("Program terminated.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        is_running = False
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print(f"Data saved to {CSV_FILENAME}")
