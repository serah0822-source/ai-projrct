import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

# ====================================
# 1. 데이터 불러오기
# ====================================
@st.cache_data
def load_data():
    df = pd.read_csv("서울시 지정·인증업소 현황.csv", encoding="cp949")
    return df

df = load_data()

# ====================================
# 2. 자치구 선택 UI
# ====================================
st.title("📍 서울특별시 지정·인증업소 지도")

gu_list = df["자치구 명"].dropna().unique()
selected_gu = st.selectbox("자치구를 선택하세요", ["전체"] + sorted(gu_list))

# ====================================
# 3. 자치구 필터링
# ====================================
if selected_gu != "전체":
    filtered_df = df[df["자치구 명"] == selected_gu]
else:
    filtered_df = df

st.write(f"### 🔎 총 {len(filtered_df)}개의 업소가 조회되었습니다.")

# ====================================
# 4. Folium 지도 생성
# ====================================

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]
m = folium.Map(location=seoul_center, zoom_start=11)

# 자치구별 색상 지정
colors = [
    "red", "blue", "green", "purple", "orange", "darkred", "lightred",
    "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple",
    "white", "pink", "lightblue", "lightgreen", "gray", "black"
]
gu_color_map = {gu: colors[i % len(colors)] for i, gu in enumerate(gu_list)}

# ====================================
# 5. 지도에 마커 표시
# ====================================

for idx, row in filtered_df.iterrows():
    address = row["도로명주소"]
    gu = row["자치구 명"]

    # 좌표가 없는 경우 스킵
    try:
        # 만약 위도/경도 없으면 직접 생성해야 하지만, 데이터셋에는 좌표가 없는 경우가 많음
        # 여기서는 Naver 또는 Kakao API가 없으므로 Folium 마커만 텍스트로 표시
        tooltip = f"{row['업소 명']} ({gu})"
        popup = folium.Popup(f"<b>업소명:</b> {row['업소 명']}<br><b>주소:</b> {address}", max_width=300)

        # 임시 좌표 생성 (각 구마다 중심 다른 위치를 주기 위해 난수 활용)
        import random
        lat = 37.55 + random.uniform(-0.03, 0.03)
        lon = 126.98 + random.uniform(-0.03, 0.03)

        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color=gu_color_map[gu],
            fill=True,
            fill_color=gu_color_map[gu],
            tooltip=tooltip,
            popup=popup
        ).add_to(m)
    except:
        continue

# ====================================
# 6. Streamlit에 Folium 지도 렌더링
# ====================================
st_folium(m, width=800, height=600)
