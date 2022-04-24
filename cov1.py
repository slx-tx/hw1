import requests
import json
import sqlite3
import pymysql
import sys
import xlwings as xw
import numpy as np
import pandas as pd
import os
from flask import Flask
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Line
from pyecharts.charts import Bar


def get_data_global():
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=329822670771'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/55.0.2883.87 Safari/537.36'}
    re = requests.get(url, headers=headers)
    js_data_g = re.json()['data']['areaTree']
    num_global = 207
    glo = []
    for i in range(num_global):
        earth_data_g = js_data_g[i]
        date_g = earth_data_g['lastUpdateTime']
        name_g = earth_data_g['name']
        today_confirm_g = json.dumps(earth_data_g['today']['confirm'])
        if today_confirm_g == 'null':
            today_confirm_g = '0'
        total_confirm_g = json.dumps(earth_data_g['total']['confirm'])
        total_dead_g = json.dumps(earth_data_g['total']['dead'])
        total_heal_g = json.dumps(earth_data_g['total']['heal'])
        dic_g = {'date': date_g, 'country': name_g, 'today confirm': today_confirm_g, 'total confirm': total_confirm_g,
                'total dead': total_dead_g, 'total heal': total_heal_g}
        glo.append(dic_g)

    return glo


def get_data_china():
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=329822670771'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
    re = requests.get(url, headers=headers)
    num_china = 60
    chi = []
    js_data_c = re.json()['data']['chinaDayList']
    for i in range(num_china):
        earth_data_c = js_data_c[i]
        date_c = earth_data_c['date']
        today_confirm_c = json.dumps(earth_data_c['today']['confirm'])
        total_confirm_c = json.dumps(earth_data_c['total']['confirm'])
        total_dead_c = json.dumps(earth_data_c['total']['dead'])
        total_heal_c = json.dumps(earth_data_c['total']['heal'])
        dic_c = {'date': date_c, 'today confirm': today_confirm_c, 'total confirm': total_confirm_c,
                'total dead': total_dead_c, 'total heal': total_heal_c}
        chi.append(dic_c)

    return chi


def get_data_city():
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=329822670771'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
    area = requests.get(url, headers=headers).json()
    data = area['data']
    countries = data['areaTree']
    pro = []
    cit = []
    for country in countries:
        if country['name'] == '中国':
            provinces = country['children']
            for province in provinces:
                province_name = province['name']
                cities = province['children']
                for city in cities:
                    date_city = city['lastUpdateTime']
                    city_name = city['name']
                    city_total = city['total']
                    city_today_confirm = int(city['today']['confirm'])
                    city_total_confirm = int(city_total['confirm'])
                    city_dead = int(city_total['dead'])
                    city_heal = int(city_total['heal'])
                    dic_city = {'province': province_name, 'city': city_name,
                             'date': date_city, 'today confirm': city_today_confirm,
                             'total confirm': city_total_confirm, 'total dead': city_dead,
                             'total heal': city_heal}
                    cit.append(dic_city)
                province_today_confirm = int(province['today']['confirm'])
                province_total_confirm = int(province['total']['confirm'])
                province_dead = int(province['total']['dead'])
                province_heal = int(province['total']['heal'])
                date_pro = province['lastUpdateTime']
                dic_pro = {'province': province_name,
                             'date': date_pro, 'today confirm': province_today_confirm,
                             'total confirm': province_total_confirm, 'total dead': province_dead,
                             'total heal': province_heal}
                pro.append(dic_pro)

    return cit, pro


def data_global_pic(glo):
    num_global = len(glo)
    x = np.arange(num_global)
    date = []
    country = []
    today_confirm = []
    total_confirm = []
    total_dead = []
    total_heal = []
    wb = xw.Book()
    sht = wb.sheets('sheet1')
    sht.range(f'A1').value = '编号'
    sht.range(f'B1').value = '地区'
    sht.range(f'C1').value = '新增确诊'
    sht.range(f'D1').value = '累计确诊'
    sht.range(f'E1').value = '死亡'
    sht.range(f'F1').value = '治愈'
    sht.range(f'G1').value = '更新日期'
    for k in enumerate(glo):
        date.append(k[1].get('date'))
        country.append(k[1].get('country'))
        today_confirm.append(int(k[1].get('today confirm')))
        total_confirm.append(int(k[1].get('total confirm')))
        total_dead.append(int(k[1].get('total dead')))
        total_heal.append(int(k[1].get('total heal')))
    for i in range(num_global):
        sht.range(f'A{i + 2}').value = i + 1
        sht.range(f'B{i + 2}').value = country[i]
        sht.range(f'C{i + 2}').value = today_confirm[i]
        sht.range(f'D{i + 2}').value = total_confirm[i]
        sht.range(f'E{i + 2}').value = total_dead[i]
        sht.range(f'F{i + 2}').value = total_heal[i]
        sht.range(f'G{i + 2}').value = date[i]
    #plt.bar(x, today_confirm, tick_label=country)
    #plt.show()
    wb.save('global_covid.xlsx')


def data_china_pic(chi):
    num_global = len(chi)
    x = np.arange(num_global)
    date = []
    today_confirm = []
    total_confirm = []
    total_dead = []
    total_heal = []
    for k in enumerate(chi):
        date.append(k[1].get('date'))
        today_confirm.append(int(k[1].get('today confirm')))
        total_confirm.append(int(k[1].get('total confirm')))
        total_dead.append(int(k[1].get('total dead')))
        total_heal.append(int(k[1].get('total heal')))
    plt.plot(x, today_confirm)
    plt.savefig("today_confirm_china.jpg")
    plt.close()
    plt.plot(x, total_confirm, x, total_dead, x, total_heal)
    plt.savefig("confirm_china.jpg")


def data_province_pic_total(pro):
    split = [
        {'min': 10000, 'color': '#540d0d'},
        {'max': 9999, 'min': 1000, 'color': '#9c1414'},
        {'max': 999, 'min': 100, 'color': '#ed3232'},
        {'max': 99, 'min': 10, 'color': '#f27777'},
        {'max': 9, 'min': 1, 'color': '#f7adad'},
        {'max': 0, 'color': '#f7e4e4'},
    ]
    total_confirm = []
    for k in enumerate(pro):
        province_name = k[1].get('province')
        total_confirm_p = k[1].get('total confirm')
        total_confirm.append((province_name, total_confirm_p))
    (
        Map().add(
            series_name="累计确诊",
            data_pair=total_confirm,
            maptype="china",
            is_selected=True,
            is_roam=True,
            is_map_symbol_show=False
        ).set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="中国累计确诊图"),
            visualmap_opts=opts.VisualMapOpts(
                pieces=split,
                is_piecewise=True,
                is_show=True
            )
        ).render("total_confirm_province.html")
    )


def data_province_pic_today(pro):
    split = [
        {'min': 10000, 'color': '#540d0d'},
        {'max': 9999, 'min': 1000, 'color': '#9c1414'},
        {'max': 999, 'min': 100, 'color': '#ed3232'},
        {'max': 99, 'min': 10, 'color': '#f27777'},
        {'max': 9, 'min': 1, 'color': '#f7adad'},
        {'max': 0, 'color': '#f7e4e4'},
    ]
    today_confirm = []
    for k in enumerate(pro):
        province_name = k[1].get('province')
        today_confirm_p = k[1].get('today confirm')
        today_confirm.append((province_name, today_confirm_p))
    (
        Map().add(
            series_name="当日确诊",
            data_pair=today_confirm,
            maptype="china",
            is_selected=True,
            is_roam=True,
            is_map_symbol_show=False
        ).set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="中国累计确诊图"),
            visualmap_opts=opts.VisualMapOpts(
                pieces=split,
                is_piecewise=True,
                is_show=True
            )
        ).render("today_confirm_province.html")
    )


def data_city_pic_total(cit, pro_name):
    split = [
        {'min': 10000, 'color': '#540d0d'},
        {'max': 9999, 'min': 1000, 'color': '#9c1414'},
        {'max': 999, 'min': 100, 'color': '#ed3232'},
        {'max': 99, 'min': 10, 'color': '#f27777'},
        {'max': 9, 'min': 1, 'color': '#f7adad'},
        {'max': 0, 'color': '#f7e4e4'},
    ]
    total_confirm = []
    for k in enumerate(cit):
        city_name = k[1].get('city')
        total_confirm_c = k[1].get('total confirm')
        province_name = k[1].get('province')
        if (province_name == "上海") | (province_name =="北京") | (province_name == "重庆") | (province_name == "天津"):
            if (city_name[-1] != "区") & (city_name[-1] != "县"):
                city_name = city_name + "区"
        else:
            if (city_name[-1] != "区") & (city_name[-1] != "县"):
                city_name = city_name + "市"
        if province_name == pro_name:
            total_confirm.append((city_name, total_confirm_c))
    (
        Map().add(
            series_name="累计确诊",
            data_pair=total_confirm,
            maptype=pro_name,
            is_selected=True,
            is_roam=True,
            is_map_symbol_show=False
        ).set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="省累计确诊图"),
            visualmap_opts=opts.VisualMapOpts(
                pieces=split,
                is_piecewise=True,
                is_show=True
            )
        ).render("total_confirm_city.html")
    )


def data_city_pic_today(cit, pro_name):
    split = [
        {'min': 10000, 'color': '#540d0d'},
        {'max': 9999, 'min': 1000, 'color': '#9c1414'},
        {'max': 999, 'min': 100, 'color': '#ed3232'},
        {'max': 99, 'min': 10, 'color': '#f27777'},
        {'max': 9, 'min': 1, 'color': '#f7adad'},
        {'max': 0, 'color': '#f7e4e4'},
    ]
    today_confirm = []
    for k in enumerate(cit):
        city_name = k[1].get('city')
        today_confirm_c = k[1].get('today confirm')
        province_name = k[1].get('province')
        if (province_name == "上海") | (province_name =="北京") | (province_name == "重庆") | (province_name == "天津"):
            if (city_name[-1] != "区") & (city_name[-1] != "县"):
                city_name = city_name + "区"
        else:
            if (city_name[-1] != "区") & (city_name[-1] != "县"):
                city_name = city_name + "市"
        if province_name == pro_name:
            today_confirm.append((city_name, today_confirm_c))
    (
        Map().add(
            series_name="当日确诊",
            data_pair=today_confirm,
            maptype=pro_name,
            is_selected=True,
            is_roam=True,
            is_map_symbol_show=False
        ).set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="省当日确诊图"),
            visualmap_opts=opts.VisualMapOpts(
                pieces=split,
                is_piecewise=True,
                is_show=True
            )
        ).render("today_confirm_city.html")
    )

cit, pro = get_data_city()
data_province_pic_total(pro)
"""def get_conn():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="covid", charset="utf8")
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()"""


"""def get_database():
    dic_global = get_data_global()
    conn, cursor = get_conn()"""

    #cursor.execute('''CREATE TABLE DATA_GLOBAL
        #(ID INT PRIMARY KEY, DATE TEXT, COUNTRY TEXT, TODAY_CONFIRM TEXT, TOTAL_CONFIRM TEXT,
            #TOTAL_DEAD TEXT, TOTAL_HEAL TEXT)''')"""
    #"""sql = "INSERT INTO GLOBAL \
                  #(DATE, COUNTRY, TODAY_CONFIRM, TOTAL_CONFIRM, TOTAL_DEAD, TOTAL_HEAL)\
                    #VALUES (%s, %s, %s, %s, %s, %s);" \
          #% (dic_global[k].get('date'), dic_global[k].get('country'), dic_global[k].get('today confirm'),
             #dic_global[k].get('total confirm'),
             #dic_global[k].get('total dead'), dic_global[k].get('total heal'))"""
    #"""sql = "insert into DATA_GLOBAL(date_g,country,today_confirm,total_confirm," \
          #"total_dead,total_heal) values(%s,%s,%s,%s,%s,%s)"
    #for k in dic_global:
        #cursor.execute(sql, k)
        #conn.commit()
    #close_conn(conn, cursor)


#get_database()"""
