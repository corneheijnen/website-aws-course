from flask import Flask
from waitress import serve

app = Flask(__name__)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=80)
    serve(app, host='0.0.0.0', port=80)
