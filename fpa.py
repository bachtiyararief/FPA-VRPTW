import numpy
import pandas
import scipy
import functools
import chaotic_map as chmap 

#pandas.set_option('display.max_columns', None)

class FlowerPollination():

    def __init__(
        self, chaotic: dict = None, **parameter
    ):
        self.banyak_bunga = parameter.get('banyak_bunga')
        self.step_size = parameter.get('step_size')
        self.switch_probability = parameter.get('switch_probability')
        self.lamda = parameter.get('lamda')
        self.dimensi = parameter.get('dimensi')

        self.__nama_kolom = [f'{kolom + 1}' for kolom in range(self.dimensi)]
        self.__nama_baris = [f'Bunga {baris + 1}' for baris in range(self.banyak_bunga)]

        self.sigma = ((scipy.special.gamma(1 + self.lamda) * numpy.sin(numpy.pi * (self.lamda / 2))) \
                      /(scipy.special.gamma((1 + self.lamda) / 2) * self.lamda * (2 ** ((self.lamda - 1) / 2))))**(1 / self.lamda)
        
        chaotic_type = chaotic.get('type', None)
        default_params_chaotic = chaotic.get('params', None)

        self.chaotic_function = None
        if(chaotic_type is None):
            self.chaotic_maps(chaotic_type, default_params_chaotic)
    
    def chaotic_maps(
        self, chaotic_type: str, default_params_chaotic: dict
    ):
        
        alpha = default_params_chaotic.get('alpha')
        
        if(chaotic_type == 'logistic'):
            self.chaotic_function = functools.partial(chmap.logistic, alpha = alpha)
        elif(chaotic_type == 'iterative'):
            self.chaotic_function = functools.partial(chmap.iterative, alpha = alpha)
        elif(chaotic_type == 'sine'):
            self.chaotic_function = functools.partial(chmap.sine, alpha = alpha)
        elif(chaotic_type == 'tent'):
            self.chaotic_function = functools.partial(chmap.tent)
        elif(chaotic_type == 'singer'):
            mu = default_params_chaotic.get('mu')
            self.chaotic_function = functools.partial(chmap.singer, mu = mu)

        self.x_chmap_seleksi = self.x_chmap_penyerbukan = default_params_chaotic.get('x_awal')        
        return(self)
            
    def bangkitkan_posisi_bunga(self) -> pandas.DataFrame:
        
        real_acak = numpy.random.rand(
            self.banyak_bunga, 
            self.dimensi
        )

        posisi_bunga = pandas.DataFrame(
            real_acak,
            columns = self.__nama_kolom,
            index = self.__nama_baris,
        )

        return(posisi_bunga)
    
    def solusi_terbaik(
        self, fitness: pandas.Series, tipe: str = 'min'
    ) -> tuple:

        if(tipe.lower() == 'min'):
            nilai_optimum = fitness.min()
            index_bunga_terbaik = fitness.idxmin()
        else:
            nilai_optimum = fitness.max()
            index_bunga_terbaik = fitness.idxmax()
        
        return(nilai_optimum, index_bunga_terbaik)

    def seleksi_penyerbukan(self) -> pandas.DataFrame:
        
        if(self.chaotic_function is None):
            real_acak = numpy.random.rand(self.banyak_bunga)
        else:
            real_acak = list()
            for i in range(self.banyak_bunga):
                x_baru = self.chaotic_function(x = self.x_chmap_seleksi)
                real_acak.append(x_baru)
                
                self.x_chmap_seleksi = x_baru   
        
        switch_prob = [self.switch_probability] * self.banyak_bunga
        
        seleksi = pandas.DataFrame({
                'Random' : real_acak,
                'Switch Probability' : switch_prob
            }, 
            index = self.__nama_baris
        )

        seleksi['Penyerbukan'] = numpy.where(
            seleksi['Random'] < self.switch_probability,
            'GLOBAL',
            'LOKAL'
        )

        return(seleksi)
    
    def penyerbukan_lokal(
        self, posisi: list
    ) -> list:
        
        hasil = list()
        
        for i in range(self.dimensi):
            
            if(self.chaotic_function is None):
                epsilon = numpy.random.rand()
            else:
                epsilon = self.chaotic_function(x = self.x_chmap_penyerbukan)
                self.x_chmap_penyerbukan = epsilon
                
            int_acak = numpy.arange(0, self.dimensi)  
            int_acak = numpy.setdiff1d(int_acak, i)

            j = numpy.random.choice(int_acak)
            int_acak = numpy.setdiff1d(int_acak, j)

            k = numpy.random.choice(int_acak)

            posisi_baru = posisi[i] + epsilon*(posisi[j] - posisi[k])
            hasil.append(posisi_baru)
        
        return(hasil)
    
    def penyerbukan_global(
        self, posisi: list, posisi_terbaik: list
    ) -> list:

        hasil = []

        u = numpy.random.normal(
            loc = 0,
            scale = 1,
            size = (1, self.dimensi)
        )

        v = numpy.random.normal(
            loc = 0,
            scale = 1,
            size = (1, self.dimensi)
        )

        u = u.flatten()
        v = v.flatten()

        for i in range(self.dimensi):
            s = (u[i] * self.sigma)/((numpy.abs(v[i]))**(1 / self.lamda))
            L = ((self.lamda * scipy.special.gamma(self.lamda) * numpy.sin(numpy.pi/2 * self.lamda))/numpy.pi) * \
                (1/(numpy.abs(s) ** (1 + self.lamda)))
            posisi_baru = posisi[i] + self.step_size * L * (posisi_terbaik[i] - posisi[i])
            hasil.append(posisi_baru)

        return(hasil)
    
    def penyerbukan(
        self, posisi: pandas.DataFrame, index_bunga_terbaik: str, show: bool = False
    ) -> pandas.DataFrame:

        hasil_seleksi = self.seleksi_penyerbukan()
        posisi_bunga_terbaik = posisi.loc[index_bunga_terbaik]
        
        if(show):
            print(f'\n{hasil_seleksi}\n')
            
        for i in range(self.banyak_bunga):
            index_bunga = f'Bunga {i+1}'
            posisi_bunga = posisi.loc[index_bunga]
            
            if(hasil_seleksi.loc[index_bunga]['Penyerbukan'] == 'GLOBAL'):
                hasil_penyerbukan = self.penyerbukan_global(
                    posisi = posisi_bunga,
                    posisi_terbaik = posisi_bunga_terbaik
                )

            else:
                hasil_penyerbukan = self.penyerbukan_lokal(
                    posisi_bunga
                )

            if(i == 0):
                posisi_bunga_baru = pandas.DataFrame([hasil_penyerbukan])
            else:
                posisi_bunga_baru.loc[i] = hasil_penyerbukan

        posisi_bunga_baru.index = self.__nama_baris
        posisi_bunga_baru.columns = self.__nama_kolom

        return(posisi_bunga_baru)
    
    def bandingkan_hasil(
        self, evaluasi_bunga: pandas.Series, evaluasi_bunga_baru: pandas.Series, tipe: str = 'min'
    ) -> pandas.DataFrame:

        hasil_banding = pandas.DataFrame({
            'Sebelum Penyerbukan' : evaluasi_bunga,
            'Setelah Penyerbukan' : evaluasi_bunga_baru
        })
        
        if(tipe.lower() == 'min'):
            hasil_banding['Fungsi Tujuan Terbaik'] = hasil_banding[['Sebelum Penyerbukan', 'Setelah Penyerbukan']].min(axis=1)
            kondisi = (hasil_banding['Sebelum Penyerbukan'] <= hasil_banding['Setelah Penyerbukan'])
        else:
            hasil_banding['Fungsi Tujuan Terbaik'] = hasil_banding[['Sebelum Penyerbukan', 'Setelah Penyerbukan']].max(axis=1)
            kondisi = (hasil_banding['Sebelum Penyerbukan'] >= hasil_banding['Setelah Penyerbukan'])
            
        hasil_banding['Keterangan'] = numpy.where(
            kondisi, 
            'Pertahankan Posisi', 
            'Update Posisi' 
        )

        return(hasil_banding)
    
    def update_posisi(
        self, hasil_banding: pandas.DataFrame, posisi_awal: pandas.DataFrame, posisi_baru: pandas.DataFrame
    ) -> pandas.DataFrame:
                
        update_posisi = pandas.DataFrame(columns = self.__nama_kolom)

        for i in range(self.banyak_bunga):
            if(hasil_banding['Keterangan'][i] == 'Pertahankan Posisi'):
                posisi_terpilih = posisi_awal.loc[f'Bunga {i+1}']
            else:
                posisi_terpilih = posisi_baru.loc[f'Bunga {i+1}']

            update_posisi.loc[i] = posisi_terpilih
        
        update_posisi.index = self.__nama_baris

        return(update_posisi)
