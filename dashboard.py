import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from babel.numbers import format_currency


#build a helper
def create_payments_info(df) :
    #hitung jumlah tipe pembayaran yang digunakan pelanggan
    by_payments = df.groupby("payment_type").size().reset_index(name='count').sort_values(by='count', ascending=False)
    return by_payments

def create_order_info(df):
     # Ubah kolom delivery_time menjadi durasi dalam jam
    df['delivery_time'] = df['delivery_time'].apply(lambda x: pd.Timedelta(x).total_seconds() / 3600)
    
    # Ubah kolom delivery_month menjadi tipe datetime
    df['delivery_month'] = pd.to_datetime(df['delivery_month'])
    
    # Hitung rata-rata waktu pengiriman per bulan
    by_order = df.groupby(df['delivery_month'].dt.strftime('%Y-%m'))['delivery_time'].mean().reset_index()
    return by_order

def create_customer_info(df):
    #hitung jumlah kota pelanggan
    by_customer = df.groupby('customer_city').size().reset_index(name='count').sort_values(by='count', ascending=False)
    return by_customer

#Load cleaned data
fix_df = pd.read_csv("fix_data.csv")

order_data = create_order_info(fix_df)

st.title("A Simple Dashboard for Learning")
st.write("Dibawah ini adalah visualiasi sederhana mengenai :point_down:")

col1, col2 = st.columns(2)
with col1 :
# Judul aplikasi
    st.sidebar.header('Filter Kota dengan Jumlah Pembeli Terbanyak')
#col 1 : interaktif filter kota dengan jumlah pembeli terbanyak
    by_customer = create_customer_info(fix_df) 
    min_count = st.sidebar.slider('Jumlah Minimal Pembeli', min_value=0, max_value=by_customer['count'].max(), value=0)
    filtered_cities = by_customer[by_customer['count'] >= min_count]['customer_city']

    # Tampilkan informasi di main area
    st.write(f"Menampilkan kota dengan setidaknya {min_count} pembeli:")
    #st.write(filtered_cities)
    st.dataframe(filtered_cities)


with col2:
# Column 2: Payments Bar Chart
    st.write("Jenis Pembayaran yang digunakan")
    payments_data = create_payments_info(fix_df)
    fig, ax = plt.subplots()
    ax.bar(payments_data['payment_type'], payments_data['count'])
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.write("Rata-rata waktu pengiriman (jam) setiap bulan")
# Buat chart Altair untuk visualisasi
chart = alt.Chart(order_data).mark_line().encode(
    x=alt.X('delivery_month:T', title='Bulan Pengiriman'),
    y=alt.Y('delivery_time:Q', title='Rata-rata Waktu Pengiriman (Jam)'),
    tooltip=['delivery_month:T', 'delivery_time:Q']
).properties(
    width=600,
    height=400
)
# Tampilkan chart dengan st.altair_chart
st.altair_chart(chart, use_container_width=True)





