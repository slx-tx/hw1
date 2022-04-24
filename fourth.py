from flask import Flask
import fourth1
import matplotlib as plt


app = Flask(__name__)

glo = fourth1.get_data_global()
#fourth1.data_global_pic(glo)

@app.route('/')
def index():
    return{
        "msg": "success",
        "data": "COVID-19"
    }

@app.route('/global')
def data_global():
    info = fourth1.get_data_global()
    return {
        "msg": "success",
        "data": info
    }

@app.route('/china')
def data_china():
    info = fourth1.get_data_china()
    return {
        "msg": "success",
        "data": info
    }

@app.route('/city')
def data_city():
    info = fourth1.get_data_city()
    return {
        "msg": "success",
        "data": info
    }


if __name__ == '__main__':
    app.run(debug='True')

fourth1.get_database()
