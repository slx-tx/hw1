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
        #glo.append([date_g, name_g, today_confirm_g, total_confirm_g, total_dead_g, total_heal_g])

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
        #chi.append([date_c, today_confirm_c, total_confirm_c, total_dead_c, total_heal_c])

    return chi


def get_data_city():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
    area = requests.get(url, headers=headers).json()
    data_p = json.loads(area["data"])
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
                    dic_p = {'province': province_name, 'city': city_name,
                             'date': date_p, 'today confirm': city_today_confirm,
                             'total confirm': city_total_confirm, 'total dead': city_dead,
                             'total heal': city_heal}
                    pro.append(dic_p)

    return pro


def data_global_pic(glo):
    num_global = 207
    x = np.arange(num_global)
    date = []
    country = []
    today_confirm = []
    total_confirm = []
    total_dead = []
    total_heal = []
    for k in enumerate(glo):
        date.append(k[1].get('date'))
        country.append(k[1].get('country'))
        today_confirm.append(int(k[1].get('today confirm')))
        total_confirm.append(int(k[1].get('total confirm')))
        total_dead.append(int(k[1].get('total dead')))
        total_heal.append(int(k[1].get('total heal')))
    plt.bar(x, today_confirm, tick_label=country)
    plt.show()


def data_china_pic(chi):
    num_global = 60
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
    plt.bar(x, today_confirm)
    plt.show()





get_data_city()

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
