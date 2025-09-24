import streamlit as st
import numpy as np 
import pandas as pd
import requests
import datetime 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns  # 追加

#データ読み込み
rating_data = pd.read_csv("rating_data_all.csv", index_col=0)
#更新日
last = rating_data["日付"].tail(1).item()
#最新年を覚えておく
latest_year = int(last[:4])
#latest_year=2023

#テキスト表示
st.write('使い方：上の「＞」を押して、会員番号と表示開始年を入力')
st.write('レイティング　比較グラフ')
st.write('羽曳野・若葉・奈良・HPC・神戸・カミ・向日市のデータのみです')
st.write('   最終更新日：',last)

#会員番号入力（6人まで）
kaiin = [1,2,3,4,5,6]
kaiin[0] = st.sidebar.number_input("1人目の会員番号",50000,3000000,1802222)
kaiin[1] = st.sidebar.number_input("2人目の会員番号",50000,3000000,1802222)
kaiin[2] = st.sidebar.number_input("3人目の会員番号",50000,3000000,1802222)
kaiin[3] = st.sidebar.number_input("4人目の会員番号",50000,3000000,1802222)
kaiin[4] = st.sidebar.number_input("5人目の会員番号",50000,3000000,1802222)
kaiin[5] = st.sidebar.number_input("6人目の会員番号",50000,3000000,1802222)
#年間まとめの計算開始と終了年の入力
year_s = st.sidebar.number_input("開始年",2000,2040,2019)
year_l = st.sidebar.number_input("終了年",2000,2040,latest_year)

#会員ごとにデータをrating[]に格納
rating = [[],[],[],[],[],[]]
for i in range(6):
    rating[i] = rating_data[rating_data["会員番号"] == kaiin[i]]
#グラフの日付の設定
date=[]
for i in range(6):
    date.append([datetime.datetime.strptime(s,'%Y-%m-%d') for s in rating[i]["日付"]])

colorlist = ["r", "g", "b", "c", "m", "y", "k", "w"]
fig, ax = plt.subplots()
for j in range(6):
    ax.plot(date[j], rating[j]["レイティング"], color=colorlist[j], marker="o", linestyle="solid",label = kaiin[j])

#グラフ書式
#plt.style.use('seaborn-dark-palette')
#plt.style.use('seaborn-darkgrid')   # 推奨（背景が暗めで補助線あり）
sns.set_style("darkgrid")   # seaborn でスタイル設定

plt.rcParams["font.size"] = 24
plt.tick_params(labelsize=18)
ax.set_title("Rating Graph", fontsize=30)
ax.set_xlabel("date", fontsize=24)
ax.set_ylabel("Rating", fontsize=24)
#ax.legend(loc=(0.1, 0.7))
ax.legend(loc="upper left")
fig.set_figheight(12)
fig.set_figwidth(18)

# 年毎の目盛
dates = mdates.YearLocator()
dates_fmt = mdates.DateFormatter('%Y')
ax.xaxis.set_major_locator(dates)
ax.xaxis.set_major_formatter(dates_fmt)
ax.set_xlim([datetime.datetime(year_s, 1, 1), datetime.datetime(year_l, 12, 31)])  # X軸の範囲を指定
# x軸に補助目盛線を設定
ax.grid(which = "major", axis = "x", color = "green", alpha = 0.8,linestyle = "--", linewidth = 2)
# y軸に目盛線を設定
ax.grid(which = "major", axis = "y", color = "green", alpha = 0.8,linestyle = "--", linewidth = 2)
st.pyplot(fig)

#年平均まとめの表
st.write('レイティング　年平均比較表')
matome=["会員番号"]
for s in range(year_s,year_l+1):
    matome.append(s)
temp=[]
for j in range(6):
    nen_heikin=[kaiin[j]]
    for k in range(year_s,year_l+1):
        try:
            nen_heikin.append(int(rating[j][pd.DatetimeIndex(rating[j]["日付"]).year == k]["レイティング"].mean()))
        except:    
            nen_heikin.append(0)
    temp.append(nen_heikin)
nen_heikin_matome = pd.DataFrame(temp,columns = matome)
st.dataframe(nen_heikin_matome)

#分析まとめの表示
st.write('分析データ')
seiseki=[]
date=[]
i=0
for i in range(6):
    seiseki.append(rating_data[rating_data["会員番号"] == kaiin[i]])
for i in range(6):
    date.append([datetime.datetime.strptime(s,'%Y-%m-%d') for s in seiseki[i]["日付"]])
stats=[]
temp =[]
for j in range(6):
    agaru = 0
    sagaru = 0
    agaruhi ='2000-01-01'
    sagaruhi ='2000-01-01'
    i=0
    for i in range (len(seiseki[j])-1):
        if -(seiseki[j]["レイティング"].iloc[i]-seiseki[j]["レイティング"].iloc[i+1])>agaru:
            agaru = -(seiseki[j]["レイティング"].iloc[i]-seiseki[j]["レイティング"].iloc[i+1])
            agaruhi = seiseki[j]["日付"].iloc[i+1]
        elif -(seiseki[j]["レイティング"].iloc[i]-seiseki[j]["レイティング"].iloc[i+1])<sagaru:
            sagaru = -(seiseki[j]["レイティング"].iloc[i]-seiseki[j]["レイティング"].iloc[i+1])
            sagaruhi = seiseki[j]["日付"].iloc[i+1]
    if  len(seiseki[j])>1:   
        temp=[seiseki[j]["会員番号"].iloc[0],len(seiseki[j]),seiseki[j]["レイティング"].min()
                ,seiseki[j][seiseki[j]["レイティング"] == seiseki[j]["レイティング"].min()]["日付"].iloc[0]
                ,seiseki[j]["レイティング"].max()
                ,seiseki[j][seiseki[j]["レイティング"] == seiseki[j]["レイティング"].max()]["日付"].iloc[0]
                ,agaru,agaruhi,sagaru,sagaruhi
            ]
    else:
        temp=[kaiin[j],0,0,'2000-01-01',0,'2000-01-01',0,'2000-01-01',0,'2000-01-01']         
    stats.append(temp)
stats_matome = pd.DataFrame(stats,columns = ["会員番号","出場回数","最低値","最低日","最高値","最高日","最大UP","UP日","最大DOWN","DOWN日"])
st.table(stats_matome)

#個人データの表示
rating_data=rating_data.set_index('場所')
rating_data = rating_data.sort_values('日付', ascending=False)

st.write('1人目の詳細データ')
st.table(rating_data[rating_data["会員番号"] == kaiin[0]])
st.write('2人目の詳細データ')
st.table(rating_data[rating_data["会員番号"] == kaiin[1]])
st.write('3人目の詳細データ')
st.table(rating_data[rating_data["会員番号"] == kaiin[2]])
st.write('4人目の詳細データ')
st.table(rating_data[rating_data["会員番号"] == kaiin[3]])
st.write('5人目の詳細データ')
st.table(rating_data[rating_data["会員番号"] == kaiin[4]])
st.write('6人目の詳細データ')
st.table(rating_data[rating_data["会員番号"] == kaiin[5]])