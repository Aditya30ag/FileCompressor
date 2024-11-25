import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time
import sys
from bye import resize_image
from PIL import Image

def initialize_plot(window_size=100, compression_factor=1, image_path="./projectimg.jpg", output_path="jhhj.jpg"):
    """Initialize the plotting environment and return necessary variables"""
    compression_factor = max(1, compression_factor)
    
    # Process image
    original_file_size, compressed_file_size, image_width, image_height = resize_image(
        image_path, output_path, scale=0.5, quality=70
    )
    
    # Initialize data structures
    x_data = deque(maxlen=window_size)
    y_data = deque(maxlen=window_size)
    compressed_data = deque(maxlen=window_size // compression_factor)
    
    # Set up plot
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'b-', label='Raw Data')
    compressed_line, = ax.plot([], [], 'r-', label='Compressed', alpha=0.7)
    
    # Configure plot
    ax.set_xlim(0, window_size)
    ax.set_ylim(0, 10)
    ax.grid(True)
    ax.set_title('Real-time Data Plot')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend()
    
    # Add text box
    text_box = ax.text(0.05, 0.95, '', transform=ax.transAxes, verticalalignment='top')
    
    plot_state = {
        'window_size': window_size,
        'compression_factor': compression_factor,
        'x_data': x_data,
        'y_data': y_data,
        'compressed_data': compressed_data,
        'fig': fig,
        'ax': ax,
        'line': line,
        'compressed_line': compressed_line,
        'text_box': text_box,
        'original_file_size': original_file_size,
        'compressed_file_size': compressed_file_size
    }
    
    return plot_state

def compress_data(y_data, compressed_data, compression_factor):
    """Apply simple moving average compression to the data"""
    if len(y_data) >= compression_factor:
        compressed_y = np.mean(list(y_data)[-compression_factor:])
        compressed_data.append(compressed_y)

def update_plot(plot_state, new_value):
    """Update the plot with new data"""
    # Unpack necessary values
    x_data = plot_state['x_data']
    y_data = plot_state['y_data']
    compressed_data = plot_state['compressed_data']
    compression_factor = plot_state['compression_factor']
    window_size = plot_state['window_size']
    
    # Update data
    x_data.append(len(x_data))
    y_data.append(new_value)
    
    if len(x_data) % compression_factor == 0:
        compress_data(y_data, compressed_data, compression_factor)
    
    # Update raw data line
    plot_state['line'].set_xdata(list(x_data))
    plot_state['line'].set_ydata(list(y_data))
    
    # Update compressed data line
    if compressed_data:
        compressed_x = np.linspace(0, len(x_data), len(compressed_data))
        plot_state['compressed_line'].set_xdata(compressed_x)
        plot_state['compressed_line'].set_ydata(list(compressed_data))
    
    # Update plot window
    if len(x_data) >= window_size:
        plot_state['ax'].set_xlim(len(x_data) - window_size, len(x_data))
    
    # Update text box
    plot_state['text_box'].set_text(
        f"Original file size: {plot_state['original_file_size']:.2f} KB\n"
        f"Compressed file size: {plot_state['compressed_file_size']:.2f} KB"
    )
    
    # Refresh plot
    plot_state['fig'].canvas.draw()
    plot_state['fig'].canvas.flush_events()

def close_plot(plot_state):
    """Close the plot properly"""
    plt.ioff()
    plt.close(plot_state['fig'])

def main():
    # Create plot with window of 100 points and compression factor of 5
    plot_state = initialize_plot(window_size=100, compression_factor=5)
    
    try:
        # Simulate real-time data
        for i in range(200):
            # Generate random data (replace with your data source)
            new_value = np.random.rand() * 10
            
            # Update plot
            update_plot(plot_state, new_value)
            
            # Control update rate
            time.sleep(0.05)
    
    except KeyboardInterrupt:
        print("Stopping data collection...")
    
    finally:
        close_plot(plot_state)
if __name__=="__main__":
    main()