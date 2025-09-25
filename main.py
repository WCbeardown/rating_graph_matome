import streamlit as st
import numpy as np 
import pandas as pd
import requests
import datetime 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# データ読み込み
rating_data = pd.read_csv("rating_data_all.csv", index_col=0)

# 【修正】日付を統一して datetime 型へ変換（/ と - 両方に対応）
rating_data["日付"] = pd.to_datetime(rating_data["日付"].astype(str), errors="coerce", infer_datetime_format=True)

# 【修正】変換できなかった行（NaT）を除外
rating_data = rating_data.dropna(subset=["日付"])

# 更新日（最後の行の日付を文字列に変換）
last = rating_data["日付"].max().strftime('%Y-%m-%d')  # max()のほうが確実
# 最新年を覚えておく
latest_year = rating_data["日付"].max().year

# テキスト表示
st.write('使い方：上の「＞」を押して、会員番号と表示開始年を入力')
st.write('レイティング　比較グラフ')
st.write('羽曳野・若葉・奈良・HPC・神戸・カミ・向日市のデータのみです')
st.write('   最終更新日：', last)

# 会員番号入力（6人まで）
kaiin = [1, 2, 3, 4, 5, 6]
kaiin[0] = st.sidebar.number_input("1人目の会員番号", 50000, 3000000, 1802222)
kaiin[1] = st.sidebar.number_input("2人目の会員番号", 50000, 3000000, 1802222)
kaiin[2] = st.sidebar.number_input("3人目の会員番号", 50000, 3000000, 1802222)
kaiin[3] = st.sidebar.number_input("4人目の会員番号", 50000, 3000000, 1802222)
kaiin[4] = st.sidebar.number_input("5人目の会員番号", 50000, 3000000, 1802222)
kaiin[5] = st.sidebar.number_input("6人目の会員番号", 50000, 3000000, 1802222)

# 年間まとめの計算開始と終了年の入力
year_s = st.sidebar.number_input("開始年", 2000, 2040, 2019)
year_l = st.sidebar.number_input("終了年", 2000, 2040, latest_year)

# 会員ごとにデータをrating[]に格納
rating = []
for i in range(6):
    df = rating_data[rating_data["会員番号"] == kaiin[i]]
    if not df.empty:
        df = df.sort_values("日付")
    rating.append(df)

# グラフ作成
colorlist = ["r", "g", "b", "c", "m", "y", "k", "w"]
fig, ax = plt.subplots()
for j in range(6):
    if not rating[j].empty:
        ax.plot(rating[j]["日付"], rating[j]["レイティング"], color=colorlist[j], marker="o", linestyle="solid", label=str(kaiin[j]))

plt.style.use('seaborn-v0_8')
plt.rcParams["font.size"] = 24
plt.tick_params(labelsize=18)
ax.set_title("Rating Graph", fontsize=30)
ax.set_xlabel("date", fontsize=24)
ax.set_ylabel("Rating", fontsize=24)
ax.legend(loc="upper left")
fig.set_figheight(12)
fig.set_figwidth(18)

dates = mdates.YearLocator()
dates_fmt = mdates.DateFormatter('%Y')
ax.xaxis.set_major_locator(dates)
ax.xaxis.set_major_formatter(dates_fmt)
ax.set_xlim([datetime.datetime(year_s, 1, 1), datetime.datetime(year_l, 12, 31)])
ax.grid(which="major", axis="x", color="green", alpha=0.8, linestyle="--", linewidth=2)
ax.grid(which="major", axis="y", color="green", alpha=0.8, linestyle="--", linewidth=2)

st.pyplot(fig)

# 年平均まとめの表
st.write('レイティング　年平均比較表')
matome = ["会員番号"]
for s in range(year_s, year_l + 1):
    matome.append(s)

temp = []
for j in range(6):
    if rating[j].empty:
        continue
    nen_heikin = [kaiin[j]]
    for k in range(year_s, year_l + 1):
        try:
            nen_heikin.append(int(rating[j][pd.DatetimeIndex(rating[j]["日付"]).year == k]["レイティング"].mean()))
        except:
            nen_heikin.append(0)
    temp.append(nen_heikin)

if temp:
    nen_heikin_matome = pd.DataFrame(temp, columns=matome)
    st.dataframe(nen_heikin_matome)

# 分析まとめの表示
st.write('分析データ')
stats = []
for j in range(6):
    if rating[j].empty:
        continue

    agaru = 0
    sagaru = 0
    agaruhi = '2000-01-01'
    sagaruhi = '2000-01-01'
    for i in range(len(rating[j]) - 1):
        diff = rating[j]["レイティング"].iloc[i+1] - rating[j]["レイティング"].iloc[i]
        if diff > agaru:
            agaru = diff
            agaruhi = rating[j]["日付"].iloc[i+1].strftime("%Y-%m-%d")
        elif diff < sagaru:
            sagaru = diff
            sagaruhi = rating[j]["日付"].iloc[i+1].strftime("%Y-%m-%d")

    temp = [
        kaiin[j],
        len(rating[j]),
        rating[j]["レイティング"].min(),
        rating[j].loc[rating[j]["レイティング"].idxmin(), "日付"].strftime("%Y-%m-%d"),
        rating[j]["レイティング"].max(),
        rating[j].loc[rating[j]["レイティング"].idxmax(), "日付"].strftime("%Y-%m-%d"),
        agaru, agaruhi, sagaru, sagaruhi
    ]
    stats.append(temp)

if stats:
    stats_matome = pd.DataFrame(stats, columns=["会員番号", "出場回数", "最低値", "最低日", "最高値", "最高日", "最大UP", "UP日", "最大DOWN", "DOWN日"])
    st.table(stats_matome)

# 個人データの表示
rating_data["日付"] = rating_data["日付"].dt.strftime('%Y-%m-%d')  # ← 全体も時刻を消しておく
rating_data = rating_data.set_index('場所')
rating_data = rating_data.sort_values('日付', ascending=False)

for i in range(6):
    st.write(f'{i+1}人目の詳細データ')
    df = rating_data[rating_data["会員番号"] == kaiin[i]]
    if not df.empty:
        st.table(df)
