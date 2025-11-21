import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import random
import math

# ============================
# 데이터 로드
# ============================
@st.cache_data
def load_data():
    df = pd.read_csv("서울시 지정·인증업소 현황.csv", encoding="cp949")
    return df

df = load_data()

st.title("📍 서울특별시 지정·인증업소 지도 및 업소 리스트")

# ============================
# 자치구 UI
# ============================
gu_list = df["자치구 명"].dropna().unique()
selected_gu = st.selectbox("자치구를 선택하세요", ["전체"] + sorted(gu_list))

# ============================
# 자치구 필터링
# ============================
filtered_df = df if selected_gu == "전체" else df[df["자치구 명"] == selected_gu]

st.write(f"### 🔎 조회된 업소 수: {len(filtered_df)}개")


# ============================
# 임시 좌표 생성 함수 (고정 난수)
# ============================
def generate_fixed_coord(seed_value):
    random.seed(seed_value)
    lat = 37.55 + random.uniform(-0.03, 0.03)
    lon = 126.98 + random.uniform(-0.03, 0.03)
    return lat, lon


# ============================
# 서울 주요 지하철역 위치 (간단 버전)
# ============================
subway_stations = {
    "서울역": (37.5551, 126.9707),
    "시청": (37.5656, 126.9767),
    "종각": (37.5702, 126.9820),
    "종로3가": (37.5725, 126.9910),
    "강남": (37.4979, 127.0276),
    "신촌": (37.5553, 126.9368),
    "홍대입구": (37.5575, 126.9240),
    "건대입구": (37.5407, 127.0703),
    "삼성": (37.5087, 127.0631),
    "여의도": (37.5218, 126.9246)
}


# ============================
# 거리 계산 함수
# ============================
def calc_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)


# ============================
# 가장 가까운 지하철역 찾기
# ============================
def find_nearest_station(lat, lon):
    min_dist = float("inf")
    nearest = None
    for station, (s_lat, s_lon) in subway_stations.items():
        dist = calc_distance(lat, lon, s_lat, s_lon)
        if dist < min_dist:
            min_dist = dist
            nearest = station
    return nearest


# ============================
# 지도 생성
# ============================
seoul_center = [37.5665, 126.9780]
m = folium.Map(location=seoul_center, zoom_start=11)

colors = [
    "red", "blue", "green", "purple", "orange", "darkred", "lightred",
    "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple",
    "white", "pink", "lightblue", "lightgreen", "gray", "black"
]
gu_color_map = {gu: colors[i % len(colors)] for i, gu in enumerate(gu_list)}

marker_info_list = []  # 리스트 출력용 정보 저장


# ============================
# 마커 추가 + 리스트 정보 저장
# ============================
for idx, row in filtered_df.iterrows():
    gu = row["자치구 명"]
    shop = row["업소 명"]
    address = row["도로명주소"]

    # 고정 좌표 생성
    seed_value = row["식품인증업소 관리 일련번호"]
    lat, lon = generate_fixed_coord(seed_value)

    nearest_station = find_nearest_station(lat, lon)

    tooltip = f"{shop} ({gu})"
    popup = folium.Popup(
        f"<b>업소명:</b> {shop}<br>"
        f"<b>주소:</b> {address}<br>"
        f"<b>가장 가까운 지하철역:</b> {nearest_station}",
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

    # 리스트용 정보 저장
    marker_info_list.append({
        "업소명": shop,
        "주소": address,
        "가까운 지하철역": nearest_station
    })


# ============================
# 지도 렌더링
# ============================
st_folium(m, width=800, height=600)


# ============================
# 지도 아래 업소 리스트 출력
# ============================
st.write("## 📋 업소 상세 리스트")
st.dataframe(pd.DataFrame(marker_info_list))

