#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# url = 'http://opendata.mkrf.ru/opendata/7705851331-register_movies/data-14-structure-3.json'
#
# import requests
# rs = requests.get(url, stream=True)
# with open('data-14-structure-3.json', mode='wb') as f:
#     for chunk in rs.iter_content(chunk_size=1024):
#         if chunk:
#             f.write(chunk)


import json
json_data = json.load(open('data-14-structure-3.json', 'r', encoding='utf-8'))
# print(len(json_data))
# print(json.dumps(json_data[0], indent=4, ensure_ascii=False))
for film in json_data:
    print(film)
    info = film['data']['general']
    
    print('Название фильма:', info.get('filmname'))
    print('Наименование на иностранном языке:', info.get('foreignName'))
    print('Режиссер:', info.get('director'))
    print('Жанр:', info.get('viewMovie'))
    print('Студия-производитель:', info.get('studio'))
    print('Год производства:', info.get('crYearOfProduction'))
    print('Количество серий:', info.get('numberOfSeries'))
    print('Продолжительность показа, минуты:', info.get('durationMinute'))
    print('Цвет:', info['color'])
    print('Возрастная категория зрительской аудитории:', info.get('ageCategory'))
    print('Аннотация:', info.get('annotation'))
    print('Страна производства:', info.get('countryOfProduction'))
    print()
