import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/PRSA_Data_Wanliu_20130301-20170228.csv")
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    return df

# Panggil fungsi untuk memuat data
df = load_data()

# Sidebar untuk navigasi
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.selectbox("Pilih Analisis:", ["Home", "Kualitas Udara Wanliu", "Faktor yang Mempengaruhi Kualitas Udara"])

# Home Section
if menu == "Home":
    st.title("Dashboard Kualitas Udara")
    st.markdown("""
    Proyek Analisis Data: Kualitas Udara di Wanliu\n
    Nama: Ja'far Shodiq\n
    Email: jafarshodiq.alkaf@gmail.com\n
    ID Dicoding: jafar_shodiq
    """)

elif menu == "Kualitas Udara Wanliu":
    st.title("Kualitas Udara di Wanliu (2013-2017)")
    
    # Cek apakah dataset berhasil dimuat
    if df.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Statistik Deskriptif Kualitas Udara")
        st.write(df.describe())

        # Visualisasi PM2.5 Rata-rata per Tahun
        yearly_avg = df.groupby('year')['PM2.5'].mean().reset_index()
        plt.figure(figsize=(10, 5))
        sns.barplot(x='year', y='PM2.5', data=yearly_avg, palette='viridis')
        plt.title('Rata-rata PM2.5 per Tahun di Wanliu')
        plt.xlabel('Tahun')
        plt.ylabel('Rata-rata PM2.5')
        st.pyplot(plt)

elif menu == "Faktor yang Mempengaruhi Kualitas Udara":
    st.title("Faktor yang Mempengaruhi Kualitas Udara di Wanliu")
    
    # Cek apakah dataset berhasil dimuat
    if df.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Korelasi antara Polutan")
        corr_matrix = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Heatmap Korelasi Antara Polutan')
        st.pyplot(plt)

        st.subheader("Boxplot PM2.5 berdasarkan Kelompok Intensitas Hujan")
        df['RAIN_GROUP'] = pd.cut(df['RAIN'], bins=[0, 1, 4, 8, 10], labels=['No Rain', 'Light Rain', 'Moderate Rain', 'Heavy Rain'])
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='RAIN_GROUP', y='PM2.5', data=df)
        plt.title('Boxplot PM2.5 berdasarkan Intensitas Hujan')
        st.pyplot(plt)