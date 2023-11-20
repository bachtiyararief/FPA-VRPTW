import streamlit as st
import pandas as pd
from data import Data
from run_fpa_vrptw import *
from plot_grafik import *

st.set_page_config(
    page_title = 'FPA-VRPTW Ismi',
    page_icon = '🚗',
    layout = 'wide'
)

st.set_option('deprecation.showfileUploaderEncoding', False)

def header():
    _, row1, _ = st.columns([0.1, 8, 0.1])
    row1.markdown('<h1>Penyelesaian VRPTW dengan Algoritma Flower Pollination</h1>', unsafe_allow_html = True)
    row1.markdown('<h4><a href="https://id.linkedin.com/in/ismi-yayuk-rakhmawati-366917126">Ismi Yayuk Rakhmawati</a> - 11XXXXXX</h4>', 
                  unsafe_allow_html = True)

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
        <a href="http://neo.lcc.uma.es/vrp/vrp-instances/capacitated-vrp-with-time-windows-instances/">
        <i>http://neo.lcc.uma.es/vrp/vrp-instances/capacitated-vrp-with-time-windows-instances/</i></a>. 
        Data yang diolah terdiri dari koordinat posisi customer, permintaan tiap customer termasuk
        juga Time Windows dan Waktu Pelayanan.</p>
        ''',    
        unsafe_allow_html = True
    )
    
    ukuran_data = row2.radio(
        label = 'Pilih Data', 
        options = ['Data Kecil', 'Data Sedang', 'Data Besar'],
        horizontal = True
    )
    
    from_data = Data()
    data_vrptw = from_data.ekstrak_data(
        path = 'https://raw.githubusercontent.com/bachtiyararief/FPA-VRPTW/main/Data VRP-TW.xlsx', 
        sheet_name = ukuran_data
    )
    
    row2.dataframe(
        data_vrptw, 
        width = 1200, 
        height = 300
    )

    return(data_vrptw)

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
    _, row4, _ = st.columns([0.1, 8, 0.1])
    row4.markdown('<h4>🚀 Input Parameter</h4>', unsafe_allow_html = True)
    row4.markdown('''
        <p align="justify">
        Ketika mengimplementasikan Algoritma <i>Flower Pollination</i>, perlu menentukan terlebih dahulu
        beberapa parameter untuk mengontrol perilaku algoritma tersebut. Masukan beberapa
        parameter utama yang digunakan dalam FPA dengan benar.<br>
        </p>
        ''', unsafe_allow_html = True
    )                 
    
    _, row4A, _, row4B, _ = st.columns([0.1, 4, 0.1, 4, 0.1])   
    
    maks_kapasitas_kendaraan = row4A.number_input(
        'Kapasitas Max Kendaraan', 
        min_value = 1,
        format = '%d',
    )

    banyak_bunga = row4A.number_input(
        'Banyak Bunga', 
        min_value = 1, 
        max_value = 1000,
        format = '%d',
    )

    step_size = row4A.number_input(
        'Step Size', 
        min_value = 0.0000, 
        max_value = 1.0000,
        format = '%.4f',
        placeholder = "Masukan bilangan real 0 s.d 1"
    )

    switch_probability = row4A.number_input(
        'Switch Probability (ρ)', 
        min_value = 0.0000, 
        max_value = 1.0000,
        format = '%.4f'
    )

    lamda = row4A.number_input(
        'Lambda (λ)', 
        min_value = 0.0000, 
        format = '%.4f'
    )

    maks_iterasi = row4A.number_input(
        'Iterasi Maksimum', 
        min_value = 1,
        placeholder = "Masukan bilangan bulat > 0",
        format = '%d',
    )

    is_chaotic = row4B.selectbox(
        label = 'Gunakan Chaotic Maps?', 
        options = ['Tidak', 'Ya']
    )

    tipe_chaotic = x_awal = alpha = mu = None
    
    if(is_chaotic == 'Ya'):
        tipe_chaotic = row4B.selectbox(
            label = 'Pilih Tipe Chaotic', 
            options = ['Logistic', 'Iterative', 'Sine', 'Tent', 'Singer']
        )
        
        x_awal = row4B.number_input(
            'x0', 
            min_value = 0.0000, 
            format = '%.4f'
        )
        
        if(tipe_chaotic in ['Logistic', 'Iterative', 'Sine']):
            alpha = row4B.number_input(
                'alpha (α)', 
                min_value = 0.0000, 
                format = '%.4f'
            ) 
            
        elif(tipe_chaotic == 'Singer'):
            mu = row4B.number_input(
                'mu (μ)', 
                min_value = 0.0000, 
                format = '%.4f'
            )

    _, row4C, _ = st.columns([0.1, 8, 0.1])
    row4C.markdown('<br>', unsafe_allow_html = True)
    run = row4C.button(
        'Jalankan Program',
        use_container_width = True
    )
    
    return(run, maks_kapasitas_kendaraan, banyak_bunga, step_size, switch_probability, lamda, maks_iterasi, tipe_chaotic, x_awal, alpha, mu)

def hasil_perhitungan(permutasi = None, hasil = None):
    _, row5, _ = st.columns([0.1, 8, 0.1])
    row5.markdown('<h4>⭐ Hasil Perhitungan</h4>', unsafe_allow_html = True)
    row5.markdown('''
        <p align="justify">
        Berikut ini adalah solusi terbaik yang diperoleh dari hasil running program dengan data yang dipilih dan
        menggunakan parameter yang telah diinput. Anda dapat mengklik kembali tombol <b>Jalankan Program</b> diatas
        untuk mendapatkan hasil lain dengan nilai yang mungkin berbeda<br>
        </p>
        ''', unsafe_allow_html = True
    )   
    
    fig = plot_pergerakan_fungsi_tujuan(y = hasil)
    row5.plotly_chart(fig, use_container_width=True)
    
if __name__ == '__main__':
    header()
    data_vrptw = tampilkan_data()
    intro_fpa()
    run, maks_kapasitas_kendaraan, banyak_bunga, step_size, switch_probability, lamda, maks_iterasi, tipe_chaotic, x_awal, alpha, mu = input_parameter_fpa()

    if(run):
        permutasi_terbaik, hasil_terbaik, rute_potong, jarak_potong = jalankan_program(
            data_vrptw, 
            maks_kapasitas_kendaraan = maks_kapasitas_kendaraan, 
            banyak_bunga = banyak_bunga, 
            step_size = step_size, 
            switch_probability = switch_probability, 
            lamda = lamda, 
            maks_iterasi = maks_iterasi, 
            tipe_chaotic = tipe_chaotic, 
            x_awal = x_awal,
            alpha = alpha,
            mu = mu
        )

        hasil_perhitungan(hasil = hasil_terbaik)
        rute_terbaik = pd.DataFrame({
                'Index' : [f'Rute - {i+1}' for i in range(len(jarak_potong))],
                'Rute' : rute_potong, 
                'Jarak' : jarak_potong
            }
        )
        
        _, row6, _ = st.columns([0.1, 8, 0.1])
        row6.markdown('<h4>🏆 Rute Terbaik</h4>', unsafe_allow_html = True)
        row6.markdown(f'<b>Rute</b> : {"-".join(str(num) for num in permutasi_terbaik.loc[0].tolist())}', unsafe_allow_html = True)
        row6.markdown(f'<b>Total Jarak</b> : {hasil_terbaik[-1]}', unsafe_allow_html = True)
        row6.dataframe(
            rute_terbaik, 
            width = 1200, 
            height = 250,
            hide_index = True
        )
        
        fig_vrptw = plot_rute_vrptw(data_coord = data_vrptw, rute = rute_potong)
        row6.plotly_chart(fig_vrptw.to_dict(), use_container_width = True)
        
