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
import matplotlib as plt

def get_data(name):
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=329822670771'
    url1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/55.0.2883.87 Safari/537.36'}
    re = requests.get(url, headers=headers)
    re1 = requests.get(url1, headers=headers)
    js_data_g = re.json()['data']['areaTree']

    N1 = 207
    glo = []
    for i in range(N1):
        earth_data_g = js_data_g[i]
        date_g = earth_data_g['lastUpdateTime']
        name_g = earth_data_g['name']
        today_confirm_g = json.dumps(earth_data_g['today']['confirm'])
        total_confirm_g = json.dumps(earth_data_g['total']['confirm'])
        total_dead_g = json.dumps(earth_data_g['total']['dead'])
        total_heal_g = json.dumps(earth_data_g['total']['heal'])
        dic_g = {'date': date_g, 'country': name_g, 'today confirm': today_confirm_g, 'total confirm': total_confirm_g,
                'total dead': total_dead_g, 'total heal': total_heal_g}
        glo.append(dic_g)

    N2 = 60
    chi = []
    js_data_c = re.json()['data']['chinaDayList']
    for i in range(N2):
        earth_data_c = js_data_c[i]
        date_c = earth_data_c['date']
        today_confirm_c = json.dumps(earth_data_c['today']['confirm'])
        total_confirm_c = json.dumps(earth_data_c['total']['confirm'])
        total_dead_c = json.dumps(earth_data_c['total']['dead'])
        total_heal_c = json.dumps(earth_data_c['total']['heal'])
        dic_c = {'date': date_c, 'today confirm': today_confirm_c, 'total confirm': total_confirm_c,
                'total dead': total_dead_c, 'total heal': total_heal_c}
        chi.append(dic_c)

    """area = requests.get(url1).json()
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
                    pro.append(dic_p)"""

    if name == 'global':
        return glo
    elif name == 'china':
        return chi
    """elif name == 'city':
        return pro"""


def get_conn():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="cov", charset="utf8")
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def get_database():
    dic = get_data('global')
    conn, cursor = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE GLOBAL
        (ID INT PRIMARY KEY, DATE TEXT, COUNTRY TEXT, TODAY_CONFIRM TEXT, TOTAL_CONFIRM TEXT, 
            TOTAL_DEAD TEXT, TOTAL_HEAL TEXT)''')
    for i, k in enumerate(dic):
        sql = "INSERT INTO GLOBAL \
              (ID, DATE, COUNTRY, TODAY_CONFIRM, TOTAL_CONFIRM, TOTAL_DEAD, TOTAL_HEAL)\
                VALUES (%d, %s, %s, %s, %s, %s, %s);" \
              % (i+1, k.get('date'), k.get('country'), k.get('today confirm'), k.get('total confirm'),
                 k.get('total dead'), k.get('total heal'))
        c.execute(sql)
    conn.commit()
    conn.close()
