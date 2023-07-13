import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Set up the layout
st.title("Simulation Dashboard")
st.sidebar.header("Simulation Settings")

# Simulation parameters
num_iterations = st.sidebar.number_input("Number of Iterations", min_value=1, value=100)
simulation_speed = st.sidebar.slider("Simulation Speed", min_value=0.1, max_value=2.0, value=1.0)

# Simulation logic
progress_bar = st.progress(0)
status_text = st.empty()
plot = st.empty()

# Generate random data for the simulation
data = np.random.randn(num_iterations)  # Replace with your simulation data

# Create an array to store the random walk values
random_walk = np.zeros(num_iterations)

battery_shape = np.array([
    [0.09, 0.09],
    [0.09, 0.91],
    [0.4, 0.91],
    [0.4, 0.95],
    [0.6, 0.95],
    [0.6, 0.91],
    [0.91, 0.91],
    [0.91, 0.09],
    [0.09, 0.09]
])


fig = plt.figure(figsize=(2, 3))
plt.fill(battery_shape[:, 0], battery_shape[:, 1], 'black')
# Setting the axis limits
plt.xlim(0, 1)
plt.ylim(0, 1)

# Removing ticks and labels
plt.xticks([])
plt.yticks([])

for i in range(num_iterations):
    # Perform simulation step
    #random_walk[i] = random_walk[i-1] + data[i]
    
    # Update progress bar and status text
    progress = (i + 1) / num_iterations
    progress_bar.progress(progress)
    status_text.text(f"Simulation Progress: {int(progress * 100)}%")
    bar_height = 0.7 * progress

# Plotting the charging bars
    plt.bar(0.5, bar_height, width=0.7, bottom=0.15, color='green')
    # Pause for simulation speed
    # Update plot
    #plot.line_chart(random_walk[:i+1])
    plot.pyplot(fig)
    # Pause for simulation speed
    time.sleep(simulation_speed)

# Simulation complete
progress_bar.empty()
status_text.text("Simulation Complete")

# Final plot
#plot.line_chart(random_walk)
