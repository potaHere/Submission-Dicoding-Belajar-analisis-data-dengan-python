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
        # Filter data berdasarkan rentang waktu
        st.sidebar.subheader("Filter Data")
        start_date = st.sidebar.date_input("Tanggal Mulai", df['datetime'].min().date())
        end_date = st.sidebar.date_input("Tanggal Akhir", df['datetime'].max().date())
        filtered_df = df[(df['datetime'] >= pd.Timestamp(start_date)) & (df['datetime'] <= pd.Timestamp(end_date))]

        if filtered_df.empty:
            st.warning("Tidak ada data dalam rentang waktu yang dipilih.")
        else:
            # Visualisasi PM2.5 Rata-rata per Tahun (Line Chart)
            st.subheader("Rata-rata PM2.5 per Tahun")
            pm25_yearly = filtered_df.groupby('year')['PM2.5'].mean().reset_index()
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=pm25_yearly, x='year', y='PM2.5', marker='o')
            plt.title('Rata-rata PM2.5 per Tahun di Wanliu (2013-2017)')
            plt.xlabel('Tahun')
            plt.ylabel('Rata-rata PM2.5')
            plt.grid(True)
            st.pyplot(plt)

            # Visualisasi Distribusi Kategori PM2.5
            st.subheader("Distribusi Kategori PM2.5")
            filtered_df['PM2.5_Category'] = pd.cut(
                filtered_df['PM2.5'],
                bins=[0, 35, 75, 115, 150, 250, 500],
                labels=['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya', 'Berbahaya Ekstrem']
            )
            plt.figure(figsize=(10, 6))
            sns.countplot(data=filtered_df, x='PM2.5_Category', order=filtered_df['PM2.5_Category'].cat.categories)
            plt.title('Distribusi Kategori PM2.5')
            plt.xlabel('Kategori PM2.5')
            plt.ylabel('Jumlah')
            st.pyplot(plt)

elif menu == "Faktor yang Mempengaruhi Kualitas Udara":
    st.title("Faktor yang Mempengaruhi Kualitas Udara di Wanliu")
    
    # Cek apakah dataset berhasil dimuat
    if df.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        # Pilih kolom untuk visualisasi korelasi
        st.sidebar.subheader("Pilih Kolom untuk Korelasi")
        selected_columns = st.sidebar.multiselect(
            "Pilih Kolom:",
            ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM'],
            default=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
        )

        if len(selected_columns) < 2:
            st.warning("Pilih minimal dua kolom untuk melihat korelasi.")
        else:
            # Visualisasi Heatmap Korelasi Antar Variabel
            st.subheader("Heatmap Korelasi Antar Variabel")
            corr_matrix = df[selected_columns].corr()
            plt.figure(figsize=(20, 10))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title('Heatmap Korelasi Antar Variabel')
            st.pyplot(plt)

        # Pilih variabel untuk scatter plot
        st.sidebar.subheader("Pilih Variabel untuk Scatter Plot")
        scatter_var = st.sidebar.selectbox(
            "Pilih Variabel:",
            ['PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
        )

        # Visualisasi Scatter Plot
        st.subheader(f"Scatter Plot PM2.5 vs {scatter_var}")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=scatter_var, y='PM2.5')
        plt.title(f'Scatter Plot PM2.5 vs {scatter_var}')
        plt.xlabel(scatter_var)
        plt.ylabel('PM2.5')
        plt.grid(True)
        st.pyplot(plt)