import vrp, fpa
import warnings
warnings.filterwarnings("ignore")

def jalankan_program(data_vrptw, **parameter_fpa):

    dimensi = data_vrptw.shape[0] - 1
    maks_kapasitas_kendaraan = parameter_fpa.get('maks_kapasitas_kendaraan')
    banyak_bunga = parameter_fpa.get('banyak_bunga')
    step_size = parameter_fpa.get('step_size')
    switch_probability = parameter_fpa.get('switch_probability')
    lamda = parameter_fpa.get('lamda')
    maks_iterasi = parameter_fpa.get('maks_iterasi')
    tipe_chaotic = parameter_fpa.get('tipe_chaotic')

    x_awal = alpha = mu = None
    if(tipe_chaotic is not None):
        x_awal = parameter_fpa.get('x_awal')
        alpha = parameter_fpa.get('alpha')
        mu = parameter_fpa.get('mu')
    
    FPA = fpa.FlowerPollination(
        banyak_bunga = banyak_bunga,
        step_size = step_size,
        switch_probability = switch_probability,
        lamda = lamda,
        dimensi = dimensi,
        chaotic = {
            'type' : tipe_chaotic,
            'params' : {
                'x_awal' : x_awal,
                'alpha' : alpha,
                'mu' : mu
            }
        }
    )

    VRPTW = vrp.VehicleRoutingProblemwithTimeWindows(
        data = data_vrptw,
        maks_kapasitas_kendaraan = maks_kapasitas_kendaraan
    )
    
    iterasi = 1
    show = True
    maks_iterasi = maks_iterasi

    permutasi_tiap_iterasi = list()
    total_jarak_tiap_iterasi = list()
    
    posisi = FPA.bangkitkan_posisi_bunga()
    
    while(iterasi <= maks_iterasi):

        permutasi = VRPTW.urutkan_posisi(posisi)
        total_jarak = VRPTW.fungsi_tujuan(permutasi = permutasi, show = show)
        nilai_optimum, index_bunga_terbaik = FPA.solusi_terbaik(fitness = total_jarak['Fungsi Tujuan'])
        posisi_baru = FPA.penyerbukan(posisi, index_bunga_terbaik, show = show)
        permutasi_baru = VRPTW.urutkan_posisi(posisi_baru)
        total_jarak_baru = VRPTW.fungsi_tujuan(permutasi = permutasi_baru, show = show)
        banding = FPA.bandingkan_hasil(total_jarak['Fungsi Tujuan'], total_jarak_baru['Fungsi Tujuan'])
        posisi_akhir = FPA.update_posisi(hasil_banding = banding, posisi_awal = posisi, posisi_baru = posisi_baru)
        nilai_optimum_akhir, index_bunga_terbaik_akhir = FPA.solusi_terbaik(fitness = banding['Fungsi Tujuan Terbaik'])
        permutasi_bunga_terbaik = VRPTW.urutkan_posisi(posisi_akhir.loc[[index_bunga_terbaik_akhir]])

        total_jarak_tiap_iterasi.append(nilai_optimum_akhir)

        if(iterasi == 1):
            print(f'\n========== ITERASI {iterasi} ==========')
            print(f'\n{posisi}')
            print(f'\n{permutasi}\n')
            print(f'\n{total_jarak}')
            print(f'\nBunga terbaik : {index_bunga_terbaik}')
            print(posisi_baru)
            print(f'\n{permutasi_baru}\n')
            print(f'\n{total_jarak_baru}')
            print(f'\n{banding}')
            print(f'\n{posisi_akhir}')
            print(f'\nBunga terbaik : {index_bunga_terbaik_akhir}')
            
        _, rute_potong, jarak_potong = VRPTW.perhitungan_fungsi_tujuan(
            solusi = permutasi_bunga_terbaik.loc[index_bunga_terbaik_akhir], 
            show = True
        )

        permutasi_bunga_terbaik = permutasi_bunga_terbaik.reset_index(drop = True)
        posisi = posisi_akhir
        iterasi += 1
    
    return(permutasi_bunga_terbaik, total_jarak_tiap_iterasi, rute_potong, jarak_potong)
