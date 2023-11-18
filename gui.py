import streamlit as st

st.set_page_config(
    page_title = 'FPA-VRPTW Ismi',
    page_icon = '-',
    layout = 'wide'
)

@st.cache_resource
def header():
    _, row1, _ = st.columns([0.1, 8, 0.1])
    row1.title('Penyelesaian VRPTW dengan Algoritma Flower Pollination')
    row1.subheader('Ismi Yayuk')

    row1.markdown('<h1>🚗 Latar Belakang</h1>', unsafe_allow_html = True)
    row1.markdown('''
        Vehicle Routing Problem with Time Windows (VRPTW) merupakan suatu permasalahan penentuan rute kendaraan
        yang digunakan untuk melayani pelanggan yang melibatkan lebih dari satu kendaraan dengan batasan waktu,
        sehingga diperoleh rute dengan jarak minimum tanpa melanggar kendala kapasitas muatan kendaraan dan rentang waktu.
        ''',
        unsafe_allow_html = True
    )

if __name__ == '__main__':
    header()
