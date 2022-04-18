from flask import Flask
import app1


app = Flask(__name__)

@app.route('/')
def index():
    return{
        "msg": "success",
        "data": "COVID-19"
    }

@app.route('/<name>')
def data(name):
    info = app1.get_data(name)
    return {
        "msg": "success",
        "data": info
    }


if __name__ == '__main__':
    app.run(debug='True')
