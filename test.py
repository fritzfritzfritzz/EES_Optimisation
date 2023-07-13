
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
plt.style.use("ggplot")
plt.ioff()
from datetime import datetime, timedelta
import json
import requests
from PIL import Image
import random
from sklearn.preprocessing import LabelEncoder, StandardScaler
#import plotly.graph_objects as go

#[theme]
primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

# Display the logo image
st.image("logo.jpeg", width=200, output_format='auto', )

# Title
st.title("Helios EcoSolution")
# Short Description
st.write("Welcome to the Helios EcoSolution Energy Storage System. Helios EcoSolutions(HES) - saving money by optimizing energy storage, enabling  renewable energy integration and smarter utilization..")

# Add a button
if st.button("Learn more"):
    # Show more information
    st.write("""
Helios EcoSolution is a smart energy storage system that helps you reduce your grid cost and maximize your solar energy usage. It uses a smart optimiser that automatically adjusts the charging and discharging of your battery based on your energy demand, solar generation, and grid price. With Helios EcoSolution, you can save money, reduce your carbon footprint, and enjoy a reliable and clean energy supply..
""")

# Dataset Loading
pkl_file = st.file_uploader("Upload Dataset", type=["pkl"])

if pkl_file is not None:
    # Perform dataset loading and preprocessing steps
    # ...

    # Load the .pkl file
    @st.cache(allow_output_mutation=True)
    def load_data():
        data = pd.read_pickle(pkl_file)
        return data

    # Load the data
    data = load_data()

    # Display the loaded data
    if data is not None:
        st.write("Loaded Dataset:")
        st.write(data)


# Create a sidebar with a feature column
feature = st.sidebar.selectbox('Select Feature:', ['Solar Generation', 'Consumption', 'Price'])

# Display the selected feature
st.write('Selected Feature:', feature)

# Display more information about the feature
if feature == 'Solar Generation':
    st.write('Solar generation is the amount of solar energy that is generated by your solar panels.')
elif feature == 'Consumption':
    st.write('Consumption is the amount of energy that is used by your home or business.')
elif feature == 'Price':
    st.write('Price is the cost of electricity per MWh.')

# # Plot the forecasts
# def plot_forecast(feature):
#     fig, ax = plt.subplots()
#     df[feature].plot(ax=ax)
#     ax.set_title(feature + " Forecast")
#     st.pyplot(fig)

# if st.sidebar.checkbox("Solar"):
#     plot_forecast("Solar")

# if st.sidebar.checkbox("Consumption"):
#     plot_forecast("Consumption")

# if st.sidebar.checkbox("Price"):
#     plot_forecast("Price")

# # KPI section
# today_saving = df["Optimised Consumption"] - df["Actual Consumption"]
# yesterday_saving = df["Optimised Consumption"].shift(1) - df["Actual Consumption"].shift(1)

# st.write("Today's savings: ", today_saving)
# st.write("Yesterday's savings: ", yesterday_saving)

# Function to generate random forecast data
def generate_forecast_data():
    return np.random.randint(0, 100, size=(24,))

# Function to calculate optimization savings today
def calculate_savings_today(forecast):
    # Perform calculations to determine the savings for today
    # ...

    return np.random.randint(1000, 5000)

# Generate fake forecast data for each model
model_1_forecast = generate_forecast_data()
model_2_forecast = generate_forecast_data()
model_3_forecast = generate_forecast_data()

# Create a dictionary to store the forecast data
forecast = {
    "model_1_forecast": model_1_forecast,
    "model_2_forecast": model_2_forecast,
    "model_3_forecast": model_3_forecast
}

# Create plots for each forecast file
for file, forecast_data in forecast.items():
    st.write("Forecast for", file)
    st.line_chart(forecast_data)

    # Plot the forecast data using the plot_forecast function
    plt.plot(forecast_data)
    plt.title(file)
    plt.show()

# Calculate and display the optimization savings
optimization_savings_today = calculate_savings_today(forecast)
optimization_savings_yesterday = np.random.randint(1000, 5000)

st.write("You saved Today:", optimization_savings_today)
st.write("You saved Yesterday:", optimization_savings_yesterday)