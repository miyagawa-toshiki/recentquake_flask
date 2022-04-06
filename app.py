# スクレイピングは一日時間決めて3回まで
import base64
from io import BytesIO
import numpy as np
from bdb import checkfuncname
from flask import Flask
from flask import render_template, request, redirect
from flask_bootstrap import Bootstrap
from scraping import country_name, earthquake
import pandas as pd
import subprocess as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
bootstrap = Bootstrap(app)

def fig_to_base64(fig):
    # Bytes IO に対して、エンコード結果を書き込む。
    ofs = BytesIO()
    fig.savefig(ofs, format="png")
    png_data = ofs.getvalue()

    # バイト列を base64 文字列に変換する。
    base64_data = base64.b64encode(png_data).decode()

    return base64_data

d = pd.read_csv('all_month.csv')
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        magp=request.form.get('mag1')
        magl=request.form.get('mag2')
        country=request.form.get('place')
        try:
            fig=earthquake(country,magp, magl)
        except ValueError:
            return render_template('value_error.html')
        #error20220314 : TypeError: Invalid comparison between dtype=float64 and str
        img = fig_to_base64(fig)
        
        return render_template('index.html',img=img,cnames=country_name(d))

    return render_template('index.html',cnames=country_name(d))

#sp.call("rm templates/output.html",shell=True)

@app.route('/map',methods=['GET'])
def map_display():
    #if request.method == 'GET':
    return render_template('quake_map.html')

@app.route('/data',methods=['POST'])
def data():
    sp.call('rm all_month.csv',shell=True)
    sp.call('wget https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv',shell=True)
    return render_template('new_data.html')



