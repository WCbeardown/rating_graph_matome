import streamlit as st
import numpy as np 
import pandas as pd
import requests
import datetime 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.write('使い方：上の「＞」を押して、会員番号と年を入力')

st.write('レイティング　比較グラフ')
st.write('羽曳野・若葉・奈良・HPC (2022.2.20現在)')

rating_data = pd.read_csv("rating_data_all.csv", index_col=0)
#会員番号入力
kaiin = [1,2,3,4,5]
kaiin[0] = st.sidebar.number_input("1人目の会員番号",90000,2500000,1802222)
kaiin[1] = st.sidebar.number_input("2人目の会員番号",90000,2500000,1802222)
kaiin[2] = st.sidebar.number_input("3人目の会員番号",90000,2500000,1802222)
kaiin[3] = st.sidebar.number_input("4人目の会員番号",90000,2500000,1802222)
kaiin[4] = st.sidebar.number_input("5人目の会員番号",90000,2500000,1802222)

#年間まとめの計算開始と終了年
year_s = st.sidebar.number_input("開始年",2000,2030,2018)
year_l = st.sidebar.number_input("終了年",2000,2030,2022)

#st.write(kaiin)
rating = [[],[],[],[],[]]
for i in range(5):
    rating[i] = rating_data[rating_data["会員番号"] == kaiin[i]]
#    st.dataframe(rating[i])
date=[]
for i in range(5):
    date.append([datetime.datetime.strptime(s,'%Y-%m-%d') for s in rating[i]["日付"]])

#st.line_chart(rating[0]["レイティング"])

colorlist = ["r", "g", "b", "c", "m", "y", "k", "w"]
fig, ax = plt.subplots()
for j in range(5):
    ax.plot(date[j], rating[j]["レイティング"], color=colorlist[j], marker="o", linestyle="solid",label = kaiin[j])

#グラフ書式
plt.style.use('seaborn-dark-palette')
plt.rcParams["font.size"] = 24
plt.tick_params(labelsize=18)
ax.set_title("Rating Graph", fontsize=30)
ax.set_xlabel("date", fontsize=24)
ax.set_ylabel("Rating", fontsize=24)
ax.legend(loc=(0.1, 0.7))
fig.set_figheight(12)
fig.set_figwidth(18)

# 年毎の目盛
dates = mdates.YearLocator()
dates_fmt = mdates.DateFormatter('%Y')
ax.xaxis.set_major_locator(dates)
ax.xaxis.set_major_formatter(dates_fmt)
# x軸に補助目盛線を設定
ax.grid(which = "major", axis = "x", color = "green", alpha = 0.8,linestyle = "--", linewidth = 2)
# y軸に目盛線を設定
ax.grid(which = "major", axis = "y", color = "green", alpha = 0.8,linestyle = "--", linewidth = 2)

st.pyplot(fig)



#年間まとめの表
st.write('レイティング　年平均比較表')
#hajime=[]
#owari=[]
#for j in range(5):
#    owari.append(pd.DatetimeIndex(rating[j]["日付"]).year.max())
#    hajime.append(pd.DatetimeIndex(rating[j]["日付"]).year.min())

matome=["会員番号"]
for s in range(year_s,year_l+1):
    matome.append(s)
temp=[]
for j in range(5):
    nen_heikin=[kaiin[j]]
    for k in range(year_s,year_l+1):
        try:
            nen_heikin.append(int(rating[j][pd.DatetimeIndex(rating[j]["日付"]).year == k]["レイティング"].mean()))
        except:    
            nen_heikin.append(0)
    temp.append(nen_heikin)
nen_heikin_matome = pd.DataFrame(temp,columns = matome)
st.dataframe(nen_heikin_matome)

#個人データの表示
rating_data=rating_data.set_index('場所')

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