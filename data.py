import math
import pandas
import requests
import io

class Data():
    
    def __init__(self):
        pass
    
    def ekstrak_data(
        self, path: str, sheet_name: str
    ) -> pandas.DataFrame: 
        
        data_io = requests.get(path).content
        data = pandas.read_excel(io.BytesIO(data_io), sheet_name = sheet_name, engine = 'openpyxl')
        data.set_index('Customer Number', inplace = True)
        
        return(data)
    
    def jarak_euclidian(
        self, coord1: pandas.DataFrame, coord2: pandas.DataFrame
    ) -> float :
        
        try:
            jarak = (coord1['Coord. X'].values[0] - coord2['Coord. X'].values[0])**2 + (coord1['Coord. Y'].values[0] - coord2['Coord. Y'].values[0])**2
        except:
            jarak = (coord1['Coord. X'] - coord2['Coord. X'])**2 + (coord1['Coord. Y'] - coord2['Coord. Y'])**2
        
        jarak = round(math.sqrt(jarak), 2)
        
        return(jarak)

    def waktu_perjalanan(
        self, jarak: float
    ) -> float :
        
        waktu = (jarak / 40) * 60
        return (waktu)
    
    def data_jarak_waktu(
        self, data: pandas.DataFrame
    ) -> pandas.DataFrame :
        
        data = data.reset_index()
        data_jarak = pd.DataFrame(columns=['Customer Number'] + list(data['Customer Number']))
        
        for i in range(len(data)):
            row = {'Customer Number': data.loc[i, 'Customer Number']}
            for j in range(len(data)):
                distance = jarak_euclidian(data[data['Customer Number'] == i], data[data['Customer Number'] == j])
                row[data.loc[j, 'Customer Number']] = round(distance, 2)
            data_jarak = data_jarak.append(row, ignore_index=True)

        data_jarak['Customer Number'] = data_jarak['Customer Number'].astype(int)
        data_jarak = data_jarak.set_index(['Customer Number'])

        data_waktu = data_jarak
        for i in data_jarak.columns:
            data_waktu[i] = data_jarak[i]/40*60

        return(data_jarak, data_waktu)
    
   
