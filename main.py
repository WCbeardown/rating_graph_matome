import streamlit as st
import numpy as np
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# =========================
# データ読み込み
# =========================
rating_data = pd.read_csv("rating_data_all.csv", index_col=0)

#Debug
st.write("CSV最終行（生データ）")
st.write(rating_data.tail(5))

st.write("CSVの日付最大値（変換前）")
st.write(rating_data["日付"].max())


# 日付区切り統一
rating_data["日付"] = (
    rating_data["日付"]
    .astype(str)
    .str.replace(r"[/-]", "-", regex=True)
)

# datetime 変換
rating_data["日付"] = pd.to_datetime(rating_data["日付"], errors="coerce")

# NaT 除外
rating_data = rating_data.dropna(subset=["日付"])

# 日付順にソート
rating_data = rating_data.sort_values("日付")

# =========================
# 更新日・最新年（ここで確定）
# =========================
last_date = rating_data["日付"].max()
last = last_date.strftime("%Y-%m-%d")
latest_year = last_date.year

# =========================
# 表示テキスト
# =========================
st.write('使い方：上の「＞」を押して、会員番号と表示開始年を入力')
st.write('レイティング　比較グラフ')
st.write('羽曳野・若葉・奈良・HPC・神戸・カミ・向日市のデータのみです')
st.write('   最終更新日：', last)

# =========================
# 会員番号入力（最大6人）
# =========================
kaiin = [None] * 6
kaiin[0] = st.sidebar.number_input("1人目の会員番号", 50000, 3000000, 1802222)
kaiin[1] = st.sidebar.number_input("2人目の会員番号", 50000, 3000000, 1802222)
kaiin[2] = st.sidebar.number_input("3人目の会員番号", 50000, 3000000, 1802222)
kaiin[3] = st.sidebar.number_input("4人目の会員番号", 50000, 3000000, 1802222)
kaiin[4] = st.sidebar.number_input("5人目の会員番号", 50000, 3000000, 1802222)
kaiin[5] = st.sidebar.number_input("6人目の会員番号", 50000, 3000000, 1802222)

# 表示年範囲
year_s = st.sidebar.number_input("開始年", 2000, 2040, 2019)
year_l = st.sidebar.number_input("終了年", 2000, 2040, latest_year)

# =========================
# 会員ごとのデータ抽出
# =========================
rating = []
for i in range(6):
    df = rating_data[rating_data["会員番号"] == kaiin[i]]
    df = df.sort_values("日付")
    rating.append(df)

# =========================
# グラフ描画
# =========================
plt.style.use('seaborn-v0_8')
plt.rcParams["font.size"] = 24

fig, ax = plt.subplots(figsize=(18, 12))
colorlist = ["r", "g", "b", "c", "m", "y"]

for j in range(6):
    if not rating[j].empty:
        ax.plot(
            rating[j]["日付"],
            rating[j]["レイティング"],
            marker="o",
            linestyle="solid",
            color=colorlist[j],
            label=str(kaiin[j])
        )

ax.set_title("Rating Graph", fontsize=30)
ax.set_xlabel("date", fontsize=24)
ax.set_ylabel("Rating", fontsize=24)
ax.legend(loc="upper left")

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_xlim(
    datetime.datetime(year_s, 1, 1),
    datetime.datetime(year_l, 12, 31)
)

ax.grid(True, which="major", axis="both", linestyle="--", alpha=0.8)
st.pyplot(fig)

# =========================
# 年平均まとめ表
# =========================
st.write('レイティング　年平均比較表')

columns = ["会員番号"] + list(range(year_s, year_l + 1))
rows = []

for j in range(6):
    if rating[j].empty:
        continue

    row = [kaiin[j]]
    for y in range(year_s, year_l + 1):
        mean_val = rating[j][rating[j]["日付"].dt.year == y]["レイティング"].mean()
        row.append(int(mean_val) if not np.isnan(mean_val) else 0)
    rows.append(row)

if rows:
    st.dataframe(pd.DataFrame(rows, columns=columns))

# =========================
# 分析データ
# =========================
st.write('分析データ')

stats = []
for j in range(6):
    if rating[j].empty:
        continue

    diffs = rating[j]["レイティング"].diff()

    max_up = diffs.max()
    max_down = diffs.min()

    up_date = rating[j].iloc[diffs.idxmax()]["日付"].strftime("%Y-%m-%d") if not np.isnan(max_up) else ""
    down_date = rating[j].iloc[diffs.idxmin()]["日付"].strftime("%Y-%m-%d") if not np.isnan(max_down) else ""

    stats.append([
        kaiin[j],
        len(rating[j]),
        rating[j]["レイティング"].min(),
        rating[j].loc[rating[j]["レイティング"].idxmin(), "日付"].strftime("%Y-%m-%d"),
        rating[j]["レイティング"].max(),
        rating[j].loc[rating[j]["レイティング"].idxmax(), "日付"].strftime("%Y-%m-%d"),
        int(max_up) if not np.isnan(max_up) else 0,
        up_date,
        int(max_down) if not np.isnan(max_down) else 0,
        down_date
    ])

if stats:
    st.table(pd.DataFrame(
        stats,
        columns=["会員番号", "出場回数", "最低値", "最低日", "最高値", "最高日", "最大UP", "UP日", "最大DOWN", "DOWN日"]
    ))

# =========================
# 個人データ表示（表示専用コピー）
# =========================
rating_data_display = rating_data.copy()
rating_data_display["日付"] = rating_data_display["日付"].dt.strftime('%Y-%m-%d')
rating_data_display = rating_data_display.set_index("場所")
rating_data_display = rating_data_display.sort_values("日付", ascending=False)

for i in range(6):
    st.write(f'{i+1}人目の詳細データ')
    df = rating_data_display[rating_data_display["会員番号"] == kaiin[i]]
    if not df.empty:
        st.table(df)

