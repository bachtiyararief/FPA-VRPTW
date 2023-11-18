from data import Data
import streamlit as st

st.set_page_config(
    page_title = 'FPA-VRPTW Ismi',
    page_icon = '-',
    layout = 'wide'
)

@st.cache_resource
def header():
    _, row1, _ = st.columns([0.1, 8, 0.1])
    row1.markdown('<h1>Penyelesaian VRPTW dengan Algoritma Flower Pollination</h1>', unsafe_allow_html = True)
    row1.markdown('<h3>Ismi Yayuk</h3>', unsafe_allow_html = True)

    row1.markdown('<h4>🚗 Latar Belakang</h4>', unsafe_allow_html = True)
    row1.markdown('''
        <p align="justify">
        Vehicle Routing Problem with Time Windows (VRPTW) merupakan suatu permasalahan penentuan rute kendaraan
        yang digunakan untuk melayani pelanggan yang melibatkan lebih dari satu kendaraan dengan batasan waktu,
        sehingga diperoleh rute dengan jarak minimum tanpa melanggar kendala kapasitas muatan kendaraan dan rentang waktu.
        </p>
        ''',
        unsafe_allow_html = True
    )
    
    row1.markdown('''
        <p align="center">
        <img src="https://miro.medium.com/v2/resize:fit:1400/1*yYIxxq81QOgq5DuqEnrGcg.gif" width="558" height="300">
        </p>
        <p align="center"><b>Simulasi <i>Vehicle Routing Problem</i></b></p>
        ''',
        unsafe_allow_html = True
    )

def tampilkan_data():
    _, row2, _ = st.columns([0.1, 8, 0.1])
    row2.markdown('<h4>📊 Data Digunakan</h4>', unsafe_allow_html = True)
    row2.markdown('''
        <p align="justify">
        Data yang digunakan terdiri dari 25, 50, dan 100 pelanggan yang digunakan
        untuk perhitungan pada program. Data diperoleh dari 
        <i>http://neo.lcc.uma.es/vrp/vrp-instances/capacitated-vrp-with-time-windows-instances/</i>. 
        Data yang diolah terdiri dari koordinat posisi customer, permintaan tiap customer termasuk
        juga Time Windows dan Waktu Pelayanan.</p>
        ''',    
        unsafe_allow_html = True
    )
    
    from_data = Data()
    data_vrptw = from_data.ekstrak_data(
        path = 'https://raw.githubusercontent.com/bachtiyararief/FPA-VRPTW/main/Data VRP-TW (2).xlsx', 
        sheet_name = 'Data Kecil'
    )

    row2.dataframe(
        data_vrptw, 
        width = 1200, 
        height = 300
    )
    
def intro_fpa():
    _, row3, _ = st.columns([0.1, 8, 0.1])
    row3.markdown('<h4>🌼 Flower Polination Algorithm (FPA)</h4>', unsafe_allow_html = True)
    row3.markdown('''
        <p align="justify">
        Dalam penyelesaian masalah Vehicle Routing Problem with Time Window (VRPTW)
        terdapat beberapa algoritma yang pernah digunakan. Saat ini muncul beberapa 
        algoritma baru salah satunya adalah Flower Polination Algorithm (FPA). 
        Flower Polination Algorithm (FPA) pertama kali ditemukan oleh Xin She Yang pada tahun 2012.
        Flower Polination Algorithm (FPA) mengadopsi proses dari penyerbukan bunga. 
        Dimana proses penyerbukan terdiri atas dua jenis yaitu penyerbukan sendiri (lokal) dan penyerbukan silang (global)
        ''', unsafe_allow_html = True
    )

def input_parameter_fpa():
    _, row4A, _, row4B, _ = st.columns([0.1, 4, 0.1, 4, 0.1])
    row3A.markdown('<h4>🚀 Input Parameter</h4>', unsafe_allow_html = True)
    
    ukuran_data = row4A.selectbox(
        label = 'Pilih Data', 
        options = ['Data Kecil', 'Data Sedang', 'Data Besar']
    )   
    
    kapasitas_max = row4A.number_input(
        'Kapasitas Max Kendaraan', 
        min_value = 1,
    )

    banyak_bunga = row4A.number_input(
        'Banyak Bunga', 
        min_value = 1, 
        max_value = 1000
    )

    step_size = row4A.number_input(
        'Step Size (α)', 
        min_value = 0, 
        max_value = 1,
        step = 0.00001,
        placeholder = "Masukan bilangan real 0 s.d 1"
    )

    switch_probability = row4A.number_input(
        'Switch Probability (ρ)', 
        min_value = 0, 
        max_value = 1,
        step = 0.00001,
        placeholder = "Masukan bilangan real 0 s.d 1"
    )

    lamda = row4A.number_input(
        'Lambda (λ)', 
        min_value = 0, 
        max_value = 1,
        step = 0.00001,
        placeholder = "Masukan bilangan real > 0"
    )

    max_iterasi = row4A.number_input(
        'Iterasi Maksimum', 
        min_value = 1,
        placeholder = "Masukan bilangan bulat > 0"
    )
    
    return(ukuran_data, kapasitas_max, banyak_bunga, step_size, switch_probability, lamda, max_iterasi)
    
if __name__ == '__main__':
    header()
    tampilkan_data()
    intro_fpa()
