from flask import Flask
from flask import render_template
import cov1


app = Flask(__name__, template_folder='.')

glo = cov1.get_data_global()
#cov1.data_global_pic(glo)

@app.route('/')
def index():
    return{
        "msg": "success",
        "data": "COVID-19"
    }

@app.route('/global')
def data_global():
    info = cov1.get_data_global()
    return {
        "msg": "success",
        "data": info
    }

@app.route('/global/total')
def data_global_total():
    info = cov1.get_data_global()
    cov1.data_global_pic(info)
    return render_template("global_covid.html")

@app.route('/china')
def data_china():
    info = cov1.get_data_china()
    return {
        "msg": "success",
        "data": info
    }

@app.route('/china/today')
def data_china_today():
    info = cov1.get_data_china()
    cov1.data_china_pic(info)
    return render_template("today_confirm_china.html")

@app.route('/china/today')
def data_china_total():
    info = cov1.get_data_china()
    cov1.data_china_pic(info)
    return render_template("total_confirm_china.html")

@app.route('/province')
def data_province():
    info_city, info_province = cov1.get_data_city()
    return {
        "msg": "success",
        "data": info_province
    }

@app.route('/province/total')
def data_province_total():
    info_city, info_province = cov1.get_data_city()
    cov1.data_province_pic_total(info_province)
    return render_template("total_confirm_province.html")

@app.route('/province/today')
def data_province_today():
    info_city, info_province = cov1.get_data_city()
    cov1.data_province_pic_today(info_province)
    return render_template("today_confirm_province.html")

@app.route('/city/total/<location>')
def data_city_total(location):
    info_city, info_province = cov1.get_data_city()
    cov1.data_city_pic_total(info_city, location)
    return render_template("total_confirm_city.html")

@app.route('/city/today/<location>')
def data_city_today(location):
    info_city, info_province = cov1.get_data_city()
    cov1.data_city_pic_today(info_city, location)
    return render_template("today_confirm_city.html")

if __name__ == '__main__':
    app.run(debug='True')
