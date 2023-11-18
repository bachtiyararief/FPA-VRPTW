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

if __name__ == '__main__':
    header()