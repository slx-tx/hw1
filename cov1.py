import requests
import json
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Line
from pyecharts.charts import Bar

class Data:
    def __init__(self, name, date, today_confirm, total_confirm, total_dead, total_heal):
        self.name = name
        self.today_confirm = today_confirm
        self.total_confirm = total_confirm
        self.total_dead = total_dead
        self.total_heal = total_heal
        self.date = date
    def write(self):
        print("\n%s:\n当日确诊: %s\n累计确诊: %s\n累计死亡: %s\n累计治愈: %s\n更新日期: %s\n"
              % (self.name, self.today_confirm, self.total_confirm, self.total_dead, self.total_heal, self.date))

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
        country = Data(name_g, date_g, today_confirm_g, total_confirm_g, total_dead_g, total_heal_g)
        country.write()
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
        china = Data("中国", date_c, today_confirm_c, total_confirm_c, total_dead_c, total_heal_c)
        china.write()
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
                country = Data(province_name, date_pro, province_today_confirm,
                               province_total_confirm, province_dead, province_heal)
                country.write()
                pro.append(dic_pro)

    return cit, pro


def data_global_pic(glo):
    num_global = len(glo)
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
    bar = (
        Bar(init_opts=opts.InitOpts(width="50000px",
                                    height="700px"))
        .add_xaxis(country)
        .add_yaxis("当日确诊", today_confirm)
        .add_yaxis("累计确诊", total_confirm)
        .add_yaxis("累计死亡", total_dead)
        .add_yaxis("累计治愈", total_heal)
    ).render("global_covid.html")


def data_china_pic(chi):
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
    line1 = (
        Line(
            init_opts=opts.InitOpts(width="3500px",
                                    height="700px")
        )
        .add_xaxis(xaxis_data=date)
        .add_yaxis(series_name="当日确诊",
                   y_axis=today_confirm,
                   is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="当日确诊图"))
    ).render("today_confirm_china.html")
    line2 = (
        Line(
            init_opts=opts.InitOpts(width="3500px",
                                    height="700px")
        )
        .add_xaxis(xaxis_data=date)
        .add_yaxis(series_name="累计确诊",
                   y_axis=total_confirm,
                   is_smooth=True)
        .add_yaxis(series_name="累计死亡",
                   y_axis=total_dead,
                   is_smooth=True)
        .add_yaxis(series_name="累计治愈",
                   y_axis=total_heal,
                   is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="当日确诊图"))
    ).render("total_confirm_china.html")


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
        Map(init_opts=opts.InitOpts(width="1500px",
                                    height="700px"))
            .add(
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
        Map(init_opts=opts.InitOpts(width="1500px",
                                    height="700px"))
            .add(
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
        Map(init_opts=opts.InitOpts(width="1500px",
                                    height="700px"))
            .add(
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
        Map(init_opts=opts.InitOpts(width="1500px",
                                    height="700px"))
            .add(
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
