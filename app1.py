import requests
import json
import xlwings as xw
import numpy as np
import pandas as pd
import os
from flask import Flask

def get_data(name):
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=329822670771'
    url1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/55.0.2883.87 Safari/537.36'}
    re = requests.get(url, headers=headers)
    re1 = requests.get(url1, headers=headers)
    #html = open("new.html", "w")
    #wb = xw.Book()
    #sht = wb.sheets('sheet1')
    #sht.range(f'A1').value = '日期'
    #sht.range(f'B1').value = '地区'
    #sht.range(f'C1').value = '新增确诊'
    #sht.range(f'D1').value = '累计确诊'
    #sht.range(f'E1').value = '死亡'
    #sht.range(f'F1').value = '治愈'
    js_data_g = re.json()['data']['areaTree']
    N1 = 207
    glo = []
    for i in range(N1):
        earth_data_g = js_data_g[i]
        date_g = earth_data_g['lastUpdateTime']
        #print(date_g)
        #html.write(date_g)
        #html.write(' ')
        #sht.range(f'A{i + 2}').value = date_g
        name_g = earth_data_g['name']
        #print(name_g)
        #html.write(name_g)
        #html.write(' ')
        #sht.range(f'B{i + 2}').value = name_g
        today_confirm_g = json.dumps(earth_data_g['today']['confirm'])
        #print(today_confirm_g)
        #html.write(today_confirm_g)
        #html.write(' ')
        #sht.range(f'C{i + 2}').value = today_confirm_g
        total_confirm_g = json.dumps(earth_data_g['total']['confirm'])
        #print(total_confirm_g)
        #html.write(total_confirm_g)
        #html.write(' ')
        #sht.range(f'D{i + 2}').value = total_confirm_g
        total_dead_g = json.dumps(earth_data_g['total']['dead'])
        #print(total_dead_g)
        #html.write(total_dead_g)
        #html.write(' ')
        #sht.range(f'E{i + 2}').value = total_dead_g
        total_heal_g = json.dumps(earth_data_g['total']['heal'])
        #print(total_heal_g)
        #html.write(total_heal_g)
        #html.write('=====================')
        #sht.range(f'F{i + 2}').value = total_heal_g
        dic_g = {'date': date_g, 'country': name_g, 'today confirm': today_confirm_g, 'total confirm': total_confirm_g,
                'total dead': total_dead_g, 'total heal': total_heal_g}
        glo.append(dic_g)

    N2 = 60
    chi = []
    #wb = xw.Book()
    #sht = wb.sheets('sheet1')
    #sht.range(f'A1').value = '日期'
    #sht.range(f'B1').value = '新增确诊'
    #sht.range(f'C1').value = '累计确诊'
    #sht.range(f'D1').value = '死亡'
    #sht.range(f'E1').value = '治愈'
    js_data_c = re.json()['data']['chinaDayList']
    for i in range(N2):
        earth_data_c = js_data_c[i]
        date_c = earth_data_c['date']
        #print(date_c)
        #html.write(date_c)
        #sht.range(f'A{i + 2}').value = date_c
        today_confirm_c = json.dumps(earth_data_c['today']['confirm'])
        #print(today_confirm_c)
        #html.write(today_confirm_c)
        #html.write(' ')
        #sht.range(f'B{i + 2}').value = today_confirm_c
        total_confirm_c = json.dumps(earth_data_c['total']['confirm'])
        #print(total_confirm_c)
        #html.write(total_confirm_c)
        #html.write(' ')
        #sht.range(f'C{i + 2}').value = total_confirm_c
        total_dead_c = json.dumps(earth_data_c['total']['dead'])
        #print(total_dead_c)
        #html.write(' ')
        #sht.range(f'D{i + 2}').value = total_dead_c
        total_heal_c = json.dumps(earth_data_c['total']['heal'])
        #print(total_heal_c)
        #html.write(total_heal_c)
        #html.write(' ')
        #html.write('=============')
        #sht.range(f'E{i + 2}').value = total_heal_c
        dic_c = {'date': date_c, 'today confirm': today_confirm_c, 'total confirm': total_confirm_c,
                'total dead': total_dead_c, 'total heal': total_heal_c}
        glo.append(dic_c)

    area = requests.get(url1).json()
    data_p = json.loads(area['data'])
    date_p = data_p['lastUpdateTime']
    countries = data_p['areaTree']
    pro = []
    for country in countries:
        if country['name'] == '中国':
            provinces = country['children']
            for province in provinces:
                province_name = province['name']
                cities = province['children']
                for city in cities:
                    city_name = city['name']
                    city_total = city['total']
                    city_today_confirm = city['today']['confirm']
                    city_total_confirm = city_total['confirm']
                    city_dead = city_total['dead']
                    city_heal = city_total['heal']
                    dic_p = {'province': province_name, 'city': city_name, 'date': date_p, 'today confirm': city_today_confirm,
                             'total confirm': city_total_confirm, 'total dead': city_dead, 'total heal': city_heal}
                    #html.write(province_name+'--')
                    #html.write(city_name+'--')
                    #html.write(date_p+'--')
                    #html.write(str(city_today_confirm)+'--')
                    #html.write(str(city_total_confirm)+'--')
                    #html.write(str(city_dead)+'--')
                    #html.write(str(city_heal)+'==========')
                    pro.append(dic_p)

    #html.close()
    if name == 'global':
        return glo
    elif name == 'china':
        return chi
    elif name == 'city':
        return pro

