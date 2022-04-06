from numpy import float64
import pandas as pd
import subprocess as sp
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
import os
import folium

def data_get():
    sp.call('wget https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv',shell=True)
    
d = pd.read_csv('all_month.csv')
def country_name(df):
    for i in range(len(df)):
        if not  ', ' in df.loc[i,'place']:
          df.loc[i,'country']=df.loc[i,'place']
        else:
          target = ', '
          s=df.loc[i,'place']
          idx = s.find(target)
          r = s[idx+2:]
          df.loc[i,'country']=r
    dfd=df[~df.duplicated(subset='country')] 
    country_list = list(dfd.country)
    return country_list

def earthquake(ecountry="India",magp=1.0,magl=7.0):
    #sp.call('wget https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv',shell=True)
    df = pd.read_csv('all_month.csv')

    for i in range(len(df)):
      if not  ', ' in df.loc[i,'place']:
        df.loc[i,'country']=df.loc[i,'place']
      else:
        target = ', '
        s=df.loc[i,'place']
        idx = s.find(target)
        r = s[idx+2:]
        df.loc[i,'country']=r

    list_dt=[]
    for i in range(len(df)):
        dt=datetime.datetime(int(str(df['time'][i])[0:4]),int(str(df['time'][i])[5:7]),int(str(df['time'][i])[8:10]))
        list_dt.append(dt)
    df['today']=list_dt
    df['year'] = df['today'].dt.year
    df['month'] = df['today'].dt.month
    df['day'] = df['today'].dt.day

    dfd=df[~df.duplicated(subset='country')]
    country_list = list(dfd.country)

    df=df[df.country==ecountry]
    magl=float64(magl)
    magp=float64(magp)                             # error20220314:ValueError: could not convert string to float: 'magl'
    df=df[(df['mag']  >  magp) & (df['mag'] < magl)] # error20220314:TypeError: Invalid comparison between dtype=float64 and str
    
    last_month_min = df[(df['month']==df['month'].min())].day.min()
    last_month_max = df[(df['month']==df['month'].min())].day.max()
    pre_month_min = df[(df['month']==df['month'].max())].day.min()
    pre_month_max = df[(df['month']==df['month'].max())].day.max()

    try:
      par_today = []
      for i in range(last_month_min, last_month_max+1):
          par_today.append(len(df.query("month=={} & day=={}".format(df.month.min(),i))))
      for i in range(pre_month_min, pre_month_max+1):
          par_today.append(len(df.query("month=={} & day=={}".format(df.month.max(),i))))
    except:
      print('データがありませんでした')
    
    # 日付のリスト生成()
    date_list = [df['today'].min() + timedelta(days=i) for i in range(len(par_today))]
    # 文字列に変換
    date_str_list = [d.strftime("%Y-%m-%d") for d in date_list]

    #print('データ数 : ', len(df))
    #display(df)

    df=df.reset_index(drop=True)

    f = folium.Figure(width=500, height=500)
    center_lat=df.latitude.median()
    center_lon=df.longitude.median()
    map = folium.Map(location=[center_lat, center_lon], zoom_start=5).add_to(f)
    for i in range(0,len(df)):
      popup='{} {} {}'.format(df['place'][i],df['mag'][i],df['today'][i])
      #folium.Marker(location=[df["latitude"][i],df["longitude"][i]],popup=popup).add_to(map)
        #popup=folium.Popup(df['mag'], max_width=1000,show=True)
      #print(df['mag'][i])
      if 6.0 <= df['mag'][i]<=10.0:
        folium.Marker(location=[df["latitude"][i],df["longitude"][i]],popup=popup,icon=folium.Icon(color='red')).add_to(map)
      if 5.0 <= df['mag'][i]<6.0:
        folium.Marker(location=[df["latitude"][i],df["longitude"][i]],popup=popup,icon=folium.Icon(color='orange')).add_to(map)
      if 0.0 <= df['mag'][i]<5.0:
        folium.Marker(location=[df["latitude"][i],df["longitude"][i]],popup=popup).add_to(map)
    map.save("templates/output.html")

    fig, axes = plt.subplots(2, 2, figsize=(20, 8))
    left = date_str_list
    height = par_today
    sns.boxplot(data=df, x='mag',ax=axes[0,0])
    sns.histplot(data=df, x='mag',ax=axes[0,1])
    sns.scatterplot(data=df, x='mag', y='depth',ax=axes[1,0])
    plt.xticks(rotation=90)
    axes[1,1].bar(left, height)
    #return country_list, map, fig
    return fig

#earthquake('Japan',1.0,7.0)

    #def earthquake_map(self, dfm):
    
#sp.call("rm all_month.csv output.html",shell=True)

#def visualization(df):
# デバックモード：export FLASK_ENV=development
