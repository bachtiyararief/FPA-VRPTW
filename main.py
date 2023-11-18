import data, vrp, fpa

import warnings
warnings.filterwarnings('ignore')

from_data = data.Data()

data_vrptw = from_data.ekstrak_data(
    path = 'https://raw.githubusercontent.com/bachtiyararief/FPA-VRPTW/main/Data VRP-TW (2).xlsx', 
    sheet_name = 'Data Kecil'
)

banyak_pelanggan = data_vrptw.shape[0] - 1

FPA = fpa.FlowerPollination(
    banyak_bunga = 5,
    step_size = 0.1,
    switch_probability = 0.5,
    lamda = 0.1,
    dimensi = banyak_pelanggan,
    chaotic = {
        'type' : 'logistic',
        'params' : {
            'alpha' : 4,
            'x_awal' : 0.3
        }
    }
)

VRPTW = vrp.VehicleRoutingProblemwithTimeWindows(
    data = data_vrptw,
    maks_kapasitas_kendaraan = 500
)

posisi = FPA.bangkitkan_posisi_bunga()

iterasi = 1
max_iterasi = 2

while(iterasi <= max_iterasi):
    
    print(f'\n========== ITERASI {iterasi} ==========')
    print(f'\n{posisi}')
    
    permutasi = VRPTW.urutkan_posisi(posisi)
    print(f'\n{permutasi}\n')

    total_jarak = VRPTW.fungsi_tujuan(permutasi = permutasi, show = True)
    print(f'\n{total_jarak}')

    nilai_optimum, index_bunga_terbaik = FPA.solusi_terbaik(fitness = total_jarak['Fungsi Tujuan'])
    print(f'\nBunga terbaik : {index_bunga_terbaik}')

    posisi_baru = FPA.penyerbukan(posisi, index_bunga_terbaik, show = True)
    print(posisi_baru)

    permutasi_baru = VRPTW.urutkan_posisi(posisi_baru)
    print(f'\n{permutasi_baru}\n')

    total_jarak_baru = VRPTW.fungsi_tujuan(permutasi = permutasi_baru, show = True)
    print(f'\n{total_jarak_baru}')

    banding = FPA.bandingkan_hasil(total_jarak['Fungsi Tujuan'], total_jarak_baru['Fungsi Tujuan'])
    print(f'\n{banding}')

    posisi_akhir = FPA.update_posisi(hasil_banding = banding, posisi_awal = posisi, posisi_baru = posisi_baru)
    print(f'\n{posisi_akhir}')

    nilai_optimum_akhir, index_bunga_terbaik_akhir = FPA.solusi_terbaik(fitness = banding['Fungsi Tujuan Terbaik'])
    print(f'\nBunga terbaik : {index_bunga_terbaik_akhir}')
    
    permutasi_bunga_terbaik = VRPTW.urutkan_posisi(posisi_akhir.loc[[index_bunga_terbaik_akhir]])
    VRPTW.perhitungan_fungsi_tujuan(solusi = permutasi_bunga_terbaik.loc[index_bunga_terbaik_akhir], show = True)
    
    posisi = posisi_akhir
    iterasi += 1
