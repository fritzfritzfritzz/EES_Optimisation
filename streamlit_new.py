import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime as dt
#import plotly.express as px
#import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

#[theme]
primaryColor='#353535'
backgroundColor='#353535'
secondaryBackgroundColor='#353535'
textColor="#262730"
#font=

st.set_page_config(layout="wide", page_icon = ":sun_with_face:")

# Title
st.title(":sun_with_face: Helios EcoSolution") # also can be use :moneybag:

# Short Description
st.write("Welcome to the Helios EcoSolution Energy Storage System. Helios EcoSolution(HES)- is a smart energy storage system that helps you reduce your grid cost and maximize your solar energy usage. It uses a smart optimiser that automatically adjusts the charging and discharging of your battery based on your energy demand, solar generation, and grid price. With Helios EcoSolution, you can save money, reduce your carbon footprint, and enjoy a reliable and clean energy supply.")


# Load the dataframe
df_solar_pred = pd.read_pickle('data/optimisation_constrained_5kW_solar.pkl')

# timeframe to plot 
timeframe = 10

# starting point for the visualisations
offset = 2500


# we choose here the targets for each plot 
for t in range(offset, (offset+96*timeframe)):
    if t == offset:
        result = [[df_solar_pred.iloc[t][1][:]]]
    else:
        result = np.append(result,[[df_solar_pred.iloc[t][1][:]]],axis=0)

for t in range(offset, (offset+96*timeframe)):
    if t == offset:
        result_solar = [[df_solar_pred.iloc[t][2][:]]]
        result_price = [[df_solar_pred.iloc[t][4][:]]]
        result_consumption = [[df_solar_pred.iloc[t][3][:]]]
        result_charging = [[df_solar_pred.iloc[t][21][:]]]
        result_discharging = [[df_solar_pred.iloc[t][22][:]]]
        result_soc = [[df_solar_pred.iloc[t][18]]]
        result_charge_action = [[df_solar_pred.iloc[t][13]]]
        result_discharge_action = [[df_solar_pred.iloc[t][14]]]
    else:
        result_solar = np.append(result_solar,[[df_solar_pred.iloc[t][2][:]]],axis=0)
        result_price = np.append(result_price,[[df_solar_pred.iloc[t][4][:]]],axis=0)
        result_consumption = np.append(result_consumption,[[df_solar_pred.iloc[t][3][:]]],axis=0)
        result_charging = np.append(result_charging,[[df_solar_pred.iloc[t][21][:]]],axis=0)
        result_discharging = np.append(result_discharging,[[df_solar_pred.iloc[t][22][:]]],axis=0)
        result_soc = np.append(result_soc,[[df_solar_pred.iloc[t][18]]],axis=0)
        result_charge_action = np.append(result_charge_action,[[df_solar_pred.iloc[t][13]]],axis=0)
        result_discharge_action = np.append(result_discharge_action,[[df_solar_pred.iloc[t][14]]],axis=0)


#  dashboard
st.title("Dashboard")

total_savings = df_solar_pred['cumulated_savings'].round(0)
daily_savings = df_solar_pred['objective_function'].round(0)

# 

st.subheader("Predictions")

# Get the plots  
#plot = st.empty()
#plot_b = st.empty()

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

#barplot for the battery charging status 




# function for plotting the first plots 
def plot_graph(ax, x, y, x2, y2,  title, ylabel, beg, end, result, linecolor1, linecolor2, legend ):
    # Plot the line
    ax.clear()
    ax.plot(x, y, linecolor1)
    ax.plot(x2, y2, linecolor2)
    ax.set_title(title)
    ax.title.set_color('white')
    ax.set_ylabel(ylabel)
    ax.set_ylim(beg, end)
    ax.legend(labels=legend, loc=(0.76,0.69))
    ax.set_xticks([result[i][0][0],result[i][0][47],result[i][0][-1]],labels=[f"{result[i][0][0].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][0].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][47].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][47].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][-1].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][-1].astype('datetime64[m]').astype(int) % 60:02}"])
    ax.patch.set_facecolor('lightgrey')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white', which='both') 

#function for plotting the second plot
def plot_2(ax, ax2,  x, y, x2, y2, x3, y3, title, y_label,  ylabel_2, beg, end, beg_2, end_2, result, linecolor1, linecolor2, linecolor3, legend ):
    # Clear the plots before plotting another loop 
    ax.clear()
    ax2.clear()
    ax.plot(x, y, linecolor1)
    ax.plot(x2, y2, linecolor2)
    #ax.plot(x3, y3, linecolor2)
    ax.set_title(title)
    ax.title.set_color('white')
    ax.set_ylabel(y_label)
    ax.set_ylim(beg, end)
    ax.legend(labels=legend, loc=(0.82,0.69))
    ax.set_xticks([result[i][0][0],result[i][0][47],result[i][0][-1]],labels=[f"{result[i][0][0].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][0].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][47].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][47].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][-1].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][-1].astype('datetime64[m]').astype(int) % 60:02}"])
    ax.patch.set_facecolor('lightgrey')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white', which='both') 

    ax2.plot(x3, y3, linecolor3, linestyle = 'dotted')
    ax2.legend(labels= ["Price"], loc=(0.70,0.81))
    ax2.set_ylim(beg_2, end_2)
    ax2.set_ylabel(ylabel_2)
    ax2.yaxis.label.set_color('white')
    ax2.tick_params(colors='white')
    ax2.set_xticks([result[i][0][0],result[i][0][47],result[i][0][-1]],labels=[f"{result[i][0][0].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][0].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][47].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][47].astype('datetime64[m]').astype(int) % 60:02}",f"{result[i][0][-1].astype('datetime64[h]').astype(int) % 24:02}:{result[i][0][-1].astype('datetime64[m]').astype(int) % 60:02}"])
    ax2.spines['right'].set_color('white')
    ax2.yaxis.set_label_position('right')
    ax2.xaxis.label.set_color('white')
    ax2.tick_params(colors='white', which='both') 
    ax2.spines['bottom'].set_color('white')
    ax2.spines['top'].set_color('white')
    ax2.spines['left'].set_color('white')

col7, col8 = st.columns([0.8,0.20])

with col7:
    plot = st.empty()

with plt.rc_context({'xtick.color':'white', 'ytick.color':'white', 'figure.facecolor':'#353535'}):
        fig1, (axes1, axes2)  = plt.subplots(2 , figsize=(8,4.5))#, sharex=True
        axes3 = axes2.twinx()
        fig1.tight_layout(pad=1.5)

f = 0.3
with col8:
    plot_b = st.empty()

def plot_battery(ax0,soc):
    ax0.clear()
    ax0.set_facecolor('#353535')
    ax0.fill(battery_shape[:, 0], battery_shape[:, 1], 'lightgrey')
    ax0.set_xlim(0, 1)
    ax0.set_ylim(0, 1)
    ax0.set_title('Battery Charge')
    ax0.spines['top'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['left'].set_visible(False)
    ax0.title.set_color('white')
    ax0.set_xticks([])
    ax0.set_yticks([0.15,0.85])
    ax0.set_yticklabels(['0 %','100 %'])
    ax0.bar(0.5, 0.7 * soc, width=0.7, bottom=0.15, color='#27c7bd')
    ax0.tick_params(colors='white')

def plot_bar(ax0,charge_action,discharge_action):
    ax0.clear()
    ax0.set_facecolor('#353535')
    ax0.set_xlim(0, 1)
    ax0.set_ylim(0, 5)
    ax0.set_title('Energy Flow')
    ax0.spines['top'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['left'].set_visible(False)
    ax0.title.set_color('white')
    ax0.set_xticks([0.25,0.75])
    ax0.set_ylabel('power [kW]')
    ax0.yaxis.label.set_color('white')
    #ax0.set_yticks([0.15,0.85])
    ax0.set_xticklabels(['charge','discharge'])
    ax0.bar(0.25, charge_action, width=0.5, bottom=0, color='#F46524')
    ax0.bar(0.75, discharge_action, width=0.5, bottom=0, color='#1d57a9')

    ax0.tick_params(colors='white')


fig_b,ax_b = plt.subplots(2,figsize=(2,5.5),facecolor='#353535')
#ax_b.set_facecolor('white')#353535')


# Removing ticks and labels



#num_iterations = result.shape[0]

header = st.empty()

col1, col2, col3 , col4, col5, col6 = st.columns(6)
with col1:
        title_1 = st.empty()
        savings_2 = st.empty()
with col2:
        title_3 = st.empty()
        savings_3 = st.empty()
with col3:
        pass
with col4:
        pass
with col5:
        pass
with col6:
        pass

for i in range(result.shape[0]):
    #make columns for the KPI's 


    # data sets for the plots 
    x1, y1 = result[i][0], result_solar[i][0]
    x2, y2 = result[i][0], result_price[i][0]
    x3, y3 = result[i][0], result_consumption[i][0]
    x4, y4 = result[i][0], result_charging[i][0]
    x5, y5 = result[i][0], result_discharging[i][0]

    #lables for the plots 
    label_1 = "Power [kW]"
    label_2 = "Price [€/MWh]"
    label_3 = "Charging status[kW]"

    #legend for the plots 
    legend_1 = ['Solar generation', 'Consumption']
    legend_2 = ['Price']
    legend_3 = ['Charge' , 'Discharge', 'Price']

    # solar and consumption plot
    plot_graph(axes1, x1, y1, x3, y3,  'Solar generation and Consumption', label_1, -0.1, 5, result, '#FB8C00', '#27C7BD', legend_1)

    #price and battery status plots 
    plot_2(axes2, axes3, x4, y4, x5, y5, x2, y2, 'Charging status', label_3,  label_2, -0.1, 6, 0.1, 0.5, result, '#F46524', '#1d57a9', 'black', legend_3)
    
    plot_battery(ax_b[0],result_soc[i])
    plot_bar(ax_b[1],result_charge_action[i],result_discharge_action[i])
    # print the plot
    plot.pyplot(fig1)
    plot_b.pyplot(fig_b)

    # print the KPIs 
    title_1.write( f"Savings for the next 24 h:")
    savings_2.subheader(f'{daily_savings.iloc[i+offset]} €')

    title_3.write( "Total accumulated savings:")
    savings_3.subheader( f'{total_savings.iloc[i+offset]} €')

    # Pause for simulation speed
    time.sleep(0.02)
