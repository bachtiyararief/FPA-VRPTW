import numpy 
import pandas
from data import Data

class VehicleRoutingProblemwithTimeWindows():

    def __init__(
        self, data: pandas.DataFrame, maks_kapasitas_kendaraan: float, chaotic: str = None
    ):
        self.data_vrp = data
        self.perhitungan = Data() 
        self.maks_kapasitas = maks_kapasitas_kendaraan
        
    def urutkan_posisi(
        self, posisi
    ) -> pandas.DataFrame:
        
        urutkan_nilai = numpy.argsort(
            posisi.values,
            axis = 1
        )

        # Mengganti nilai dengan label sesuai urutan
        pelabelan = numpy.argsort(
            urutkan_nilai,
            axis = 1
        ) + 1

        # Membuat DataFrame dari label
        hasil = pandas.DataFrame(
            pelabelan,
            columns = posisi.columns,
            index = posisi.index
        )

        # Menampilkan DataFrame
        return(hasil)
    
    def perhitungan_fungsi_tujuan(
        self, solusi: list, show: bool = False
    ) -> float:

        total_jarak_sebelum = [0]
        total_permintaan = total_jarak = lama_pelayanan = 0
        
        rute, rute_terpotong, jarak_terpotong = list(), list(), list()
        
        dari_depot = True
        banyak_pelanggan = len(solusi)
        
        for j in range(banyak_pelanggan):
            if (dari_depot):
                depot = self.data_vrp.loc[0, :]
                customer_1 = self.data_vrp.loc[solusi[j], :]
                
                jarak = self.perhitungan.jarak_euclidian(depot, customer_1)
                waktu = self.perhitungan.waktu_perjalanan(jarak)
                permintaan = customer_1['Demand']
                
                waktu_buka = customer_1['Ready Time']
                waktu_tutup = customer_1['Due Date']

                rute.append(0)
                rute.append(solusi[j])

                if((waktu <= waktu_tutup) and (permintaan <= self.maks_kapasitas)):
                    if (waktu <= waktu_buka):
                        awal_pelayanan = waktu_buka
                    else:
                        awal_pelayanan = waktu
                        
                    lama_pelayanan += (awal_pelayanan + customer_1['Service Time'])
                    total_jarak += jarak

                    if(j < banyak_pelanggan - 1):
                        next_customer = self.data_vrp.loc[solusi[j+1], :]

                        next_jarak = self.perhitungan.jarak_euclidian(customer_1, next_customer)
                        next_waktu = self.perhitungan.waktu_perjalanan(next_jarak)
                        next_permintaan = next_customer['Demand']

                        if((lama_pelayanan + next_waktu <= next_customer['Due Date']) and (next_permintaan <= self.maks_kapasitas)):
                            dari_depot = False
                        else:
                            total_jarak += jarak
                            lama_pelayanan, total_permintaan = 0, 0

                            rute_terpotong.append(rute + [0])
                            jarak_terpotong.append(total_jarak - total_jarak_sebelum[-1])
                            
                            if(show):
                                print(f'{"-".join(map(str, rute))}-0', end = '\t')
                                print(f'Jarak = {total_jarak - total_jarak_sebelum[-1] : .2f}')
                            
                            total_jarak_sebelum.append(total_jarak)
                            rute = []
                    else :
                        total_jarak += jarak
                        total_jarak_sebelum.append(total_jarak)
                        rute_terpotong.append(rute + [0])
                        jarak_terpotong.append(total_jarak - total_jarak_sebelum[-2])
                        
                        if(show):
                            print(f'{"-".join(map(str, rute))}-0', end = '\t')
                            print(f'Jarak = {total_jarak - total_jarak_sebelum[-2]: .2f}')
                else:
                    print('Periksa Data!')
                    break
            else:
                customer_1 = self.data_vrp.loc[solusi[j-1], :]
                customer_2 = self.data_vrp.loc[solusi[j], :]

                jarak = self.perhitungan.jarak_euclidian(customer_1, customer_2)
                waktu = self.perhitungan.waktu_perjalanan(jarak)
                permintaan = customer_2['Demand']

                waktu_buka = customer_2['Ready Time']
                waktu_tutup = customer_2['Due Date']
                rute.append(solusi[j])

                # Periksa constraint
                if((lama_pelayanan + waktu <= waktu_tutup) and (permintaan <= self.maks_kapasitas)):
                    if (lama_pelayanan + waktu <= waktu_buka):
                        awal_pelayanan = waktu_buka
                    else:
                        awal_pelayanan = lama_pelayanan + waktu
                    lama_pelayanan = (awal_pelayanan + customer_2['Service Time'])
                    total_jarak += jarak

                    # Periksa customer selanjutnya
                    if(j < banyak_pelanggan - 1):
                        next_customer = self.data_vrp.loc[solusi[j+1], :]

                        next_jarak = self.perhitungan.jarak_euclidian(customer_2, next_customer)
                        next_waktu = self.perhitungan.waktu_perjalanan(next_jarak)
                        next_permintaan = next_customer['Demand']

                        if((lama_pelayanan + next_waktu <= next_customer['Due Date']) and (next_permintaan <= self.maks_kapasitas)):
                            dari_depot = False
                        else :
                            dari_depot = True
                            lama_pelayanan = total_permintaan = 0
                            total_jarak += self.perhitungan.jarak_euclidian(customer_2, depot)
                            rute_terpotong.append(rute + [0])
                            jarak_terpotong.append(total_jarak - total_jarak_sebelum[-1])
                            if(show):
                                print(f'{"-".join(map(str, rute))}-0', end = '\t')
                                print(f'Jarak = {total_jarak - total_jarak_sebelum[-1]: .2f}')
                            
                            total_jarak_sebelum.append(total_jarak)
                            rute = []
                    else :
                        total_jarak += self.perhitungan.jarak_euclidian(customer_2, depot)
                        total_jarak_sebelum.append(total_jarak)
                        rute_terpotong.append(rute + [0])
                        jarak_terpotong.append(total_jarak - total_jarak_sebelum[-2])
                        
                        if(show):
                            print(f'{"-".join(map(str, rute))}-0', end = '\t')
                            print(f'Jarak = {total_jarak - total_jarak_sebelum[-2]: .2f}')

        total_jarak = round(total_jarak, 2)
        
        if(show):
            print(f'\nTotal Jarak = {total_jarak : .2f}\n')
        
        return(total_jarak, rute_terpotong, jarak_terpotong)
    
    def fungsi_tujuan(
        self, permutasi: pandas.DataFrame, show: bool = False
    ) -> pandas.DataFrame:
        
        banyak_bunga = permutasi.shape[0]
        evaluasi_bunga = list()
        
        for i in range(banyak_bunga):
            solusi = permutasi.loc[f'Bunga {i+1}', :].tolist()
            
            if(show):
                print(f'========= Solusi {i+1} =========')
                print(f'{"-".join(map(str, solusi))}\n')
            
            y, _, _ = self.perhitungan_fungsi_tujuan(solusi, show)
            evaluasi_bunga.append(y)
        
        hasil = pandas.DataFrame({
            'Bunga' : [f'Bunga {i+1}' for i in range(banyak_bunga)],
            'Fungsi Tujuan' : evaluasi_bunga
        })
        
        hasil = hasil.set_index('Bunga')
        
        return(hasil)
