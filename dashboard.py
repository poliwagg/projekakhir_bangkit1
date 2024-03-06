import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

day_df = pd.read_csv("day.csv", delimiter = ',')
hour_df = pd.read_csv("hour.csv", delimiter = ',')

season_mapping = {1: 'Spring', 2:'Summer', 3:'Fall', 4:'Winter'}
year_mapping = {0: 2011, 1:2012}
weather_mapping = {1: 'Clear/Few clouds', 2: 'Misty/Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow/Fog'}
working_day_mapping = {1: 'True', 0: 'False'}


day_df['season'].replace(season_mapping, inplace = True)
day_df['yr'].replace(year_mapping, inplace = True)
day_df['weathersit'].replace(weather_mapping, inplace = True)
day_df['workingday'].replace(working_day_mapping, inplace = True)

hour_df['season'].replace(season_mapping, inplace = True)
hour_df['yr'].replace(year_mapping, inplace = True)
hour_df['weathersit'].replace(weather_mapping, inplace = True)
hour_df['workingday'].replace(working_day_mapping, inplace = True)



workingday_summer_df = hour_df[(hour_df['workingday']== 'True') & (hour_df['season'] == 'Summer')]
result = workingday_summer_df.groupby(by='hr').agg({ 'casual':'sum'}).reset_index()
result.set_index('hr', inplace = True)

workingday_weather_df = hour_df[(hour_df['workingday']== 'True')]
workingday_weather_df = hour_df.groupby(['hr', 'weathersit']).agg({
    'casual':'sum',
    'registered':'sum',
    'cnt':'sum'
}).reset_index()

sidebar_opt = st.sidebar.selectbox(
    'Pilih pertanyaan',
    ('Pertanyaan 1', 'Pertanyaan 2')
)

if sidebar_opt == 'Pertanyaan 1':

    st.header("Pertanyaan 1")
    st.subheader("Bagaimana kondisi cuaca mempengaruhi jumlah peminjaman sepeda pada hari kerja setiap jamnya?")

    hourly_data = workingday_weather_df.groupby(['hr', 'weathersit']).agg({'cnt': 'sum'}).reset_index()
    weather_conditions = hourly_data['weathersit'].unique()
    plt.figure(figsize=(10, 6))

    for condition in weather_conditions:
        data_subset = hourly_data[hourly_data['weathersit'] == condition]
        plt.plot(data_subset['hr'], data_subset['cnt'], marker='o', label=f'{condition}')

    plt.xlabel('Jam')
    plt.ylabel('Jumlah sepeda yang dipinjam')
    plt.title('Jumlah peminjaman sepeda pada hari kerja di setiap jamnya berdasarkan cuaca')
    plt.xticks(range(0, 24))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

if sidebar_opt == 'Pertanyaan 2':

    st.header("Pertanyaan 2")
    st.subheader("Pada pukul berapa casual user paling banyak meminjam sepeda di workingday pada musim panas?")

    result_sorted = result.sort_values(by='casual', ascending=False)
    highlight_color = ['#FF5733', '#FFC300', '#FF5733']  
    highlight_index = result_sorted.index[:3]

    plt.figure(figsize=(10,5))
    bars = plt.bar(result.index, result["casual"], color='#69b3a2', alpha=0.5, align='center')

    for i in range(len(bars)):
        if i in highlight_index:
            bars[i].set_color(highlight_color[highlight_index.get_loc(i)])

    plt.bar(result.index, result["casual"], color='#69b3a2', alpha =0.5, align='center', label='Jumlah Peminjaman')
    plt.plot(result.index, result["casual"], marker='o', linewidth=2, color='#72BCD4', label='Grafik Garis')
    plt.title("Total peminjaman sepeda oleh pengguna umum pada hari kerja di musim panas", fontsize=18)
    plt.xlabel('Jam dalam sehari', fontsize=12)
    plt.ylabel('Jumlah Peminjaman', fontsize=12)
    plt.xticks(np.arange(24), fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)