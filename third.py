from flask import Flask
import third1
import matplotlib as plt


app = Flask(__name__)

@app.route('/')
def index():
    return{
        "msg": "success",
        "data": "COVID-19"
    }

@app.route('/<location>')
def data(location):
    info = third1.get_data(location)
    #third1.get_conn_g()
    return {
        "msg": "success",
        "data": info
    }


if __name__ == '__main__':
    app.run(debug='True')
