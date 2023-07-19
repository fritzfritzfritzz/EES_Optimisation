import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(layout="wide")
# Create a sample dataframe
df_solar_pred = pd.read_pickle('data/solar_predictions.pkl')

progress_bar = st.progress(0)
status_text = st.empty()
plot_type = st.sidebar.selectbox("Select plot type", ('bar', 'line', 'scatter'))

for t in range(10):
    if t == 0:
        result = [[df_solar_pred.iloc[t:t+96,0].values]]
    else:
        result = np.append(result,[[df_solar_pred.iloc[t:t+96,0].values]],axis=0)

for t in range(10):
    if t == 0:
        result2 = [[df_solar_pred.iloc[t,1]]]
    else:
        result2 = np.append(result2,[[df_solar_pred.iloc[t,1]]],axis=0)


# Set up Streamlit
st.title("Dataframe Plotting Dashboard")

# Display the dataframe
st.subheader("Dataframe")
#st.write(result2)

# Plot the dataframe
st.subheader("Plot")
#plot_type = st.selectbox("Select plot type", ('bar', 'line', 'scatter'))
plot = st.empty()

fig, ax = plt.subplots(figsize=(20,7))
# Removing ticks and labels

# Setting the axis limits
num_iterations = result.shape[0]
for i in range(num_iterations):
    # Perform simulation step
        
    # Update progress bar and status text
    progress = (i + 1) / num_iterations
    progress_bar.progress(progress)
    status_text.text(f"Simulation Progress: {int(progress * 100)}%")

# Plotting the charging bars
    plt.clf()
    plt.xticks([result[i][0][0],result[i][0][47],result[i][0][-1]],labels=[f"{result[i][0][0].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][0].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][47].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][47].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][-1].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][-1].astype('datetime64[m]').astype(int) % 60:02}"])
    plt.yticks([0,1000,2000,3000,4000,5000])
    plt.scatter(x=result[i][0],y=result2[i][0])
    plt.xlim((result[i][0][0],result[i][0][-1]))
    plt.ylim(-1000, 5000)
    plt.ylabel('predicted power [kW]')
    plt.xlabel('time')
    plt.title('Solar Prediction')


    # Pause for simulation speed
    # Update plot
    plot.pyplot(fig)


    
    #plot.line_chart(random_walk[:i+1])
    # Pause for simulation speed
    time.sleep(0.4)
st.header('KPIs ')
st.subheader(f"Savings today: {result2[1][0][0]}")
# Display the plot
#st.pyplot(fig)
