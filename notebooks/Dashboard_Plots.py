import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import plotly.express as px
import seaborn as sns



st.set_page_config(layout="wide")
# Create a sample dataframe
df_solar_pred = pd.read_pickle('../predictions/predictions_full.pkl')

progress_bar = st.progress(0)
status_text = st.empty()


# we choose here 
for t in range(96*2):
    if t == 0:
        result = [[df_solar_pred.iloc[t][1][:]]]
    else:
        result = np.append(result,[[df_solar_pred.iloc[t][1][:]]],axis=0)

for t in range(96*2):
    if t == 0:
        result_solar = [[df_solar_pred.iloc[t][2][:]]]
        result_price = [[df_solar_pred.iloc[t][4][:]]]
        result_consumption = [[df_solar_pred.iloc[t][3][:]]]
    else:
        result_solar = np.append(result_solar,[[df_solar_pred.iloc[t][2][:]]],axis=0)
        result_price = np.append(result_price,[[df_solar_pred.iloc[t][4][:]]],axis=0)
        result_consumption = np.append(result_consumption,[[df_solar_pred.iloc[t][3][:]]],axis=0)
# Set up Streamlit
st.title("Dataframe Plotting Dashboard")

# Display the dataframe
st.subheader("Dataframe")
#st.write(result2)
# 
# Plot the dataframe
st.subheader("Plot")
#plot_type = st.selectbox("Select plot type", ('bar', 'line', 'scatter'))
plot = st.empty()




def plot_graph(ax, x, y, title, ylabel, beg, end, result):
    # Plot the line
    ax.clear()
    ax.plot(x, y, 'white')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_ylim(beg, end)
    ax.set_xticks([result[i][0][0],result[i][0][47],result[i][0][-1]],labels=[f"{result[i][0][0].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][0].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][47].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][47].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][-1].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][-1].astype('datetime64[m]').astype(int) % 60:02}"])
    ax.set_xlim((result[i][0][0],result[i][0][-1]))
    ax.patch.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white', which='both') 



with plt.rc_context({'xtick.color':'white', 'ytick.color':'white', 'figure.facecolor':'black'}):
    fig1, (axes1, axes2, axes3)  = plt.subplots(3 , figsize=(10,7))
#fig1.patch.set_facecolor('grey')
#fig2, axes2 = plt.subplots(figsize=(20,3))
#fig3, axes3 = plt.subplots(figsize=(20,3))

# Setting the axis limits
num_iterations = result.shape[0]
for i in range(num_iterations):
    # Perform simulation step

    # Update progress bar and status text
    progress = (i + 1) / num_iterations
    progress_bar.progress(progress)
    status_text.text(f"Simulation Progress: {int(progress * 100)}%")
    # data 
    x1, y1 = result[i][0], result_solar[i][0]
    x2, y2 = result[i][0], result_price[i][0]
    x3, y3 = result[i][0], result_consumption[i][0]

    #ticks

    #legend
    label_1 = "Predicted power [MWh]"
    label_2 = "Predicted price per MWh"
    label_3 = "Predicted Consumption [MWh]"

#    plt.subplot(3, 1, 2)
    plot_graph(axes1, x1, y1, 'Solar Generation', label_1, -200, 10000, result)
    plot_graph(axes2, x2, y2, 'Price per MWh', label_2, -0, 90, result)
    plot_graph(axes3, x3, y3, 'Consumption in [MWh]', label_3, 10000, 16000, result)

    #st.pyplot(fig1)
    plot.pyplot(fig1)




    
    #plot.line_chart(random_walk[:i+1])
    # Pause for simulation speed
    time.sleep(0.01)


# Display the plot
#st.pyplot(fig1)