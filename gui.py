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
        Vehicle Routing Problem with Time Windows (VRPTW) merupakan suatu permasalahan penentuan rute kendaraan
        yang digunakan untuk melayani pelanggan yang melibatkan lebih dari satu kendaraan dengan batasan waktu,
        sehingga diperoleh rute dengan jarak minimum tanpa melanggar kendala kapasitas muatan kendaraan dan rentang waktu.
        ''',
        unsafe_allow_html = True
    )

def tampilkan_data(data = None):
     _, row2, _ = st.columns([0.1, 8, 0.1])
    row2.markdown('<h4>📊 Data Digunakan</h4>', unsafe_allow_html = True)
    row2.markdown('''
        Data yang digunakan terdiri dari 25, 50, dan 100 pelanggan yang digunakan
        untuk perhitungan pada program. Data diperoleh dari 
        <i>http://neo.lcc.uma.es/vrp/vrp-instances/capacitated-vrp-with-time-windows-instances/</i>. 
        Data yang diolah terdiri dari koordinat posisi customer, permintaan tiap customer termasuk
        juga Time Windows dan Waktu Pelayanan.
        ''',    
        unsafe_allow_html = True
    )

if __name__ == '__main__':
    header()
    tampilkan_data()
