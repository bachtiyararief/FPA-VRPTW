import streamlit as st
from data import Data

st.set_page_config(
    page_title = 'FPA-VRPTW Ismi',
    page_icon = '-',
    layout = 'wide'
)

st.set_option('deprecation.showfileUploaderEncoding', False)

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
        path = 'https://raw.githubusercontent.com/bachtiyararief/FPA-VRPTW/main/Data VRP-TW (2).xlsx', 
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
    
    kapasitas_max = row4A.number_input(
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

    max_iterasi = row4A.number_input(
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
            
    row4B.markdown('<br>', unsafe_allow_html = True)
                   
    run = row4B.button(
        'Jalankan Program',
        use_container_width = True
    )

    parameter_fpa_vrptw = dict(
        kapasitas_max = kapasitas_max, 
        banyak_bunga = banyak_bunga, 
        step_size = step_size, 
        switch_probability = switch_probability, 
        lamda = lamda, 
        max_iterasi = max_iterasi, 
        tipe_chaotic = tipe_chaotic, 
        x_awal = x_awal,
        alpha = alpha,
        mu = mu
    )
    
    return(run, parameter_fpa_vrptw)
    
if __name__ == '__main__':
    header()
    data_vrptw = tampilkan_data()
    intro_fpa()
    run, parameter_fpa_vrptw = input_parameter_fpa()
    
    if(run):
        pass
        #jalankan_program(data_vrptw, **parameter_fpa)
