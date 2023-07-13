import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import requests
from PIL import Image
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Display the logo image
st.image("logo.jpeg", width=200, output_format='auto', )

# Add a button
if st.button("Learn more"):
    # Show more information
    st.write("Helios EcoSolution is a smart energy storage system that helps you reduce your grid cost and maximize your solar energy usage. It uses a smart optimiser that automatically adjusts the charging and discharging of your battery based on your energy demand, solar generation, and grid price. With Helios EcoSolution, you can save money, reduce your carbon footprint, and enjoy a reliable and clean energy supply.")


# Title
st.title("Helios EcoSolution")
# Short Description
st.write("Welcome to the Helios EcoSolution Energy Storage System. Helios EcoSolutions(HES) - saving money by optimizing energy storage, enabling  renewable energy integration and smarter utilization..")

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

# # Plot for Solar Generation Forecasting
# st.subheader("Solar Generation Forecast")
# # Generate the plot for solar generation forecasting
# fig_solar = plt.figure()
# # Add your code to create the plot for solar generation forecasting using the forecasted data
# # Display the plot
# st.pyplot(fig_solar)

# # Plot for Consumption Forecasting
# st.subheader("Consumption Forecast")
# # Generate the plot for consumption forecasting
# fig_consumption = plt.figure()
# # Add your code to create the plot for consumption forecasting using the forecasted data

# # Display the plot
# st.pyplot(fig_consumption)

# # Plot for Price Forecasting
# st.subheader("Price Forecast")
# # Generate the plot for price forecasting
# fig_price = plt.figure()
# # Add your code to create the plot for price forecasting using the forecasted data

# # Display the plot
# st.pyplot(fig_price)





# Create some fake data for forecasting
forecast_start_date = pd.to_datetime("2023-01-01 00:00:00")
forecast_end_date = pd.to_datetime("2023-01-01 23:45:00")
intervals = np.arange(1, 97)
dates = pd.date_range(start=forecast_start_date, end=forecast_end_date, freq="15min") # Change the frequency to "15min"
solar = np.random.rand(96) * 10 # Dummy prediction, replace with actual model
consumption = np.random.rand(96) * 5 # Dummy prediction, replace with actual model
price = solar * consumption # Dummy prediction, replace with actual model

# Show forecast on table
st.subheader('Forecast for next 24 hours')
forecast = pd.DataFrame({
    'Date': dates,
    'Interval': intervals,
    'Solar': solar,
    'Consumption': consumption,
    'Price': price
})
st.write(forecast)

# Show forecast on line chart
st.subheader('Forecast on line chart')
st.line_chart(forecast[['Solar', 'Consumption', 'Price']])

# # Load the data for today
# today = pd.to_datetime("2023-01-01")
# data_today = load_data(today, today) # Replace with your loading function

# # Filter data by hour
# data_today = data_today[data_today['Date'].dt.hour == hour]

# # Compare actual price and forecasted price
# actual_price = data_today['price'].values
# forecasted_price = forecast['Price'].values[:len(actual_price)]
# difference = actual_price - forecasted_price

# # Calculate savings
# savings_today = difference.sum()

# # Display savings
# st.subheader('Savings for today')
# st.write(f"By using the model's forecast, you saved **${savings_today:.2f}** today.")






# # Load the model from Google Drive
# @st.cache_data
# def load_model():
#     url = 'https://drive.google.com/file/d/1xNgz_G77T1dx4rPQUSB_lAItRwSIH6K_/uc?export=download'
#     response = requests.get(url)
#     json_content = response.content.decode('utf-8')
#     model = json.loads(json_content)
#     return model

# # Define the preprocess_data function
# def preprocess_data(data):
#     # Extract hour, day, month and year from date column
#     data['Hour'] = data['Date'].dt.hour
#     data['Day'] = data['Date'].dt.dayofweek
#     data['Month'] = data['Date'].dt.month
#     data['Year'] = data['Date'].dt.year

#     # Encode base column using label encoding
#     le = LabelEncoder()
#     data['Base'] = le.fit_transform(data['Base'])

#     # Scale lat, lon and price columns using standardization
#     scaler = StandardScaler()
#     data[['Lat', 'Lon', 'Price']] = scaler.fit_transform(data[['Lat', 'Lon', 'Price']])

#     return data

# # Create some fake data for the last 1 week
# start_date = datetime.now() - timedelta(days=7)
# end_date = datetime.now()

# # Generate random dates and intervals in 15-minute frequency
# dates = pd.date_range(start=start_date, end=end_date, freq="15min")
# intervals = np.arange(1, len(dates) + 1)

# # Generate random values for base, lat, lon, solar and consumption columns
# base = np.random.choice(['A', 'B', 'C'], size=len(dates))
# lat = np.random.uniform(52.3, 52.7, size=len(dates))
# lon = np.random.uniform(13.2, 13.6, size=len(dates))
# solar = np.random.normal(10, 5, size=len(dates))
# consumption = np.random.normal(20, 10, size=len(dates))

# # Generate random values for price column based on a linear function of solar and consumption plus some noise
# price = 0.5 * solar - 0.3 * consumption + np.random.normal(0, 1, size=len(dates))

# # Create a dataframe from the generated values
# data = pd.DataFrame({
#     'Date': dates,
#     'Interval': intervals,
#     'Base': base,
#     'Lat': lat,
#     'Lon': lon,
#     'Solar': solar,
#     'Consumption': consumption,
#     'Price': price
# })

# # Perform data preprocessing and feature engineering
# preprocessed_data = preprocess_data(data)

# # Load the model
# model = load_model()

# # Forecast solar, consumption and price for next 24 hours
# forecast_start_date = end_date + timedelta(hours=1)
# forecast_end_date = end_date + timedelta(hours=24)

# # Create arrays of dates and intervals
# dates = pd.date_range(start=forecast_start_date, end=forecast_end_date, freq="15min")
# intervals = np.arange(1, len(dates) + 1)

# # Create features from dates and intervals
# X = pd.DataFrame({
#     'Date': dates,
#     'Interval': intervals,
#     'Hour': dates.dt.hour,
#     'Day': dates.dt.dayofweek,
#     'Month': dates.dt.month,
#     'Year': dates.dt.year
# })

# # Predict solar, consumption and price using the model
# solar = model['solar'].predict(X) # Replace with your model's prediction function
# consumption = model['consumption'].predict(X) # Replace with your model's prediction function
# price = model['price'].predict(X) # Replace with your model's prediction function

# # Show forecast on table
# st.subheader('Forecast for next 24 hours')
# forecast = pd.DataFrame({
#     'Date': dates,
#     'Interval': intervals,
#     'Solar': solar,
#     'Consumption': consumption,
#     'Price': price
# })
# st.write(forecast)

# # Show forecast on line chart
# st.subheader('Forecast on line chart')
# st.line_chart(forecast[['Solar', 'Consumption', 'Price']])

# # Load the data for today
# today = pd.to_datetime("2023-01-01")
# data_today = load_data(today, today)

# # Filter data by hour
# data_today = data_today[data_today['Date'].dt.hour == hour]

# # Compare actual price and forecasted price
# actual_price = data_today['price'].values
# forecasted_price = forecast['Price'].values[:len(actual_price)]
# difference = actual_price - forecasted_price

# # Calculate savings
# savings_today = difference.sum()

# # Display savings
# st.subheader('Savings for today')
# st.write(f"By using the model's forecast, you saved **${savings_today:.2f}** today.")


