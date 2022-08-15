import numpy as np
import pandas as pd
from tqdm import tqdm
from geopy.geocoders import Nominatim



def read(data):
    """
    Connecting the data collected 
    by parsing in parts
    Соединение данных собранных 
    парсингом по частям
    """
    df = pd.read_csv(f'df_conc_cian_house_{data}.csv')
    return df



def search(a, b, c):
    """
    Search for words in the "description" column, 
    to fill in undefined data
    Поиск слов в столбце "описание", 
    для заполнения неопределенных данных
    """
    for i in tqdm(a):
        searchType = b.str.findall(fr"\b({i})\b").str.join(", ")
        for ind, j in enumerate(c):
            if j == '':
                c.loc[ind] = searchType[ind]
    return c



def search_house_type(a, b, c):
    """
    Search for words in the "description" column, 
    to fill in the undefined data in the "house type" column 
    Поиск слов в столбце "описание", 
    для заполнения неопределенных данных столбца "тип дома" 
    """
    for word in a:
        searchType = b.str.findall(fr"\b({word})\b").str.join(", ")
        searchType = searchType.replace('', 'Неизвестно')
        for ind, i in enumerate(c):
            if i == 'Неизвестно':
                c.loc[ind] = searchType[ind]
    c = c.str.capitalize()
    return c



def search_year(a, b, c):
    """
    Search for year values in the "description" column, 
    to fill in the undefined data
    by 2 methods in the "year" column
    Поиск значений годов в столбце "описание", 
    для заполнения неопределенных данных
    2 мя методами в столбце "год"
    """
    for i in tqdm(a):
        searchType = b.str.findall(fr"\b({i})\b").str.join(", ")
        searchType = searchType.replace('', '0')
        for ind, j in enumerate(c):
            if j == '0':
                c.loc[ind] = searchType[ind]
    return c



def search_general(a, b, c):
    """
    Search for words in the "description" column using the values of the 
    "general information" to fill in the undefined data
    Поиск слов в столбце "описание" по значениям столбца 
    "общая информация" для заполнения неопределенных данных
    """
    name = b.name
    name2 = b.name.lower()
    b = c.str.partition(name)[1]
    lst = [name, name2]
    for i in lst:
        searchType = a.str.findall(fr"\b({i})\b").str.join(", ")
        for ind, j in enumerate(b):
            if j == '':
                b.loc[ind] = searchType[ind]
    b = b.str.split().str[-1:].str.join(", ").str.capitalize().replace({'':'нет', name :'есть'})
    print(pd.DataFrame({'\033[4m' + name + ' '+'%'+'\033[0m': round(b.value_counts(normalize=True),3)*100}),'\n')
    return b



def search_general_2(a, b, lst):
    """
    Search for words in the "description" column using the values of the 
    "general information" to fill in the undefined data
    Поиск слов в столбце "описание" по значениям столбца 
    "общая информация" для заполнения неопределенных данных
    """
    for i in lst:
        searchType = a.str.findall(fr"\b({i})\b").str.join(", ")
        for ind, j in enumerate(b):
            if j == '':
                b.loc[ind] = searchType[ind]
    b = b.str.capitalize()
    return b



def search_partition(a, b, lst):
    """
    Search for words in the "general information" column, 
    to fill in undefined data
    Поиск слов в столбце "общая информация", 
    для заполнения неопределенных данных
    """
    for i in lst:
        search = b.str.partition(f'{i}')[1]
        for ind, i in enumerate(a):
            if i == '':
                a.loc[ind] = search[ind]
    return a



def geo(a):
    """
    Address translation to geo data
    Перевод адреса в гео данные
    """
    geo_lat = []
    geo_lon = []
    disp_name = []
    
    nominatim = Nominatim(user_agent='user')
    for geo in tqdm(np.array(a)):
        try:
            location = nominatim.geocode(geo).raw
        except:
            location = {'lat': '0', 'lon': '0', 'display_name': '0'}
        geo_lat.append(location['lat'])
        geo_lon.append(location['lon'])
        disp_name.append(location['display_name'])
        
    return geo_lat, geo_lon, disp_name



def geo_ind(a, b):
    """
    Conversion of filled values to zero for reuse, 
    quick processing of addresses minus zeros
    Перевод заполненых значений в ноль для повторной, 
    быстрой обработки адресов за минусом нулей
    """
    for ind, geo in enumerate(b):
        if geo != '0':
            a.loc[ind] = '0'
    return a



def geo_ind_2(a, b):
    """
    Conversion of filled values to zero for reuse, 
    quick processing of addresses minus zeros
    Перевод заполненых значений в ноль для повторной, 
    быстрой обработки адресов за минусом нулей
    """
    for ind, geo in enumerate(b):
        if geo != '0':
            a.loc[ind] = '0'
    return a
           
    
    
def geo_2(a):
    """
    Re-translate the address into geo data minus the filled data, zeros
    Повторный перевод адреса в гео данные за вычетом заполненных данных, нулей
    """
    geo_lat = []
    geo_lon = []
    disp_name = []
    nominatim = Nominatim(user_agent='user')
    for geo in tqdm(a):
        try:
            if geo == '0':
                location = {'lat': '0', 'lon': '0', 'display_name': '0'}
            else:
                location = nominatim.geocode(geo).raw
        except:
            location = {'lat': '0', 'lon': '0', 'display_name': '0'}
        geo_lat.append(location['lat'])
        geo_lon.append(location['lon'])
        disp_name.append(location['display_name'])
    return geo_lat, geo_lon, disp_name



def geo_fillna(a, b, c, geo_lat, geo_lon, disp_name):
    """
    Connection of the filled geodata, 
    re-run processing with the previous part
    Соединение заполенных геоданных, 
    повторного захода обработки с предыдущей частью
    """
    for ind, geo in enumerate(a):
        if geo == '0':
            a.loc[ind] = geo_lat[ind]
    for ind, geo in enumerate(b):
        if geo == '0':
            b.loc[ind] = geo_lon[ind]
    for ind, geo in enumerate(c):
        if geo == '0':
            c.loc[ind] = disp_name[ind]
    return a, b, c