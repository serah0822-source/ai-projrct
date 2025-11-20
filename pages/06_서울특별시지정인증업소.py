import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import random

# ====================================
# 데이터 불러오기
# ====================================
@st.cache_data
def load_data():
    df = pd.read_csv("서울시 지정·인증업소 현황.csv", encoding="cp949")
    return df

df = load_data()

st.title("📍 서울특별시 지정·인증업소 지도")

# ====================================
# 자치구 선택 UI
# ====================================
gu_list = df["자치구 명"].dropna().unique()
selected_gu = st.selectbox("자치구를 선택하세요", ["전체"] + sorted(gu_list))

# ====================================
# 필터링
# ====================================
filtered_df = df if selected_gu == "전체" else df[df["자치구 명"] == selected_gu]
st.write(f"### 🔎 조회된 업소 수: {len(filtered_df)}개")

# ====================================
# 지도 생성
# ====================================
seoul_center = [37.5665, 126.9780]
m = folium.Map(location=seoul_center, zoom_start=11)

# 자치구별 색상
colors = [
    "red", "blue", "green", "purple", "orange", "darkred", "lightred",
    "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple",
    "white", "pink", "lightblue", "lightgreen", "gray", "black"
]
gu_color_map = {gu: colors[i % len(colors)] for i, gu in enumerate(gu_list)}

# ====================================
# 마커 추가 — 고정 난수 방식으로 flicker 제거
# ====================================

for idx, row in filtered_df.iterrows():
    gu = row["자치구 명"]
    shop = row["업소 명"]
    address = row["도로명주소"]

    # 🔑 고정 난수(seed) = 행 고유 번호 기반
    random.seed(row["식품인증업소 관리 일련번호"])

    # 고정된 임시 좌표 생성 (flicker 제거됨)
    lat = 37.55 + random.uniform(-0.03, 0.03)
    lon = 126.98 + random.uniform(-0.03, 0.03)

    tooltip = f"{shop} ({gu})"
    popup = folium.Popup(
        f"<b>업소명:</b> {shop}<br><b>주소:</b> {address}",
        max_width=300
    )

    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color=gu_color_map[gu],
        fill=True,
        fill_color=gu_color_map[gu],
        tooltip=tooltip,
        popup=popup
    ).add_to(m)

# ====================================
# 렌더링
# ====================================
st_folium(m, width=800, height=600)
