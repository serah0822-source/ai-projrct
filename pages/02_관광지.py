# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top 10 (for Foreigners)", layout="wide")

st.title("🌏 Seoul: Top 10 tourist spots loved by foreign visitors")
st.markdown(
    "지도에서 장소를 클릭하면 간단한 설명을 볼 수 있습니다. "
    "데이터 출처: TripAdvisor / VisitKorea / Klook / Viator 등."
)

# Top 10 장소 데이터 (이름, 위도, 경도, 짧은 설명)
places = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.579617,
        "lon": 126.977041,
        "desc": "조선의 대표 궁궐. 한복 체험과 수문장 교대식으로 유명."
    },
    {
        "name": "Bukchon Hanok Village (북촌 한옥마을)",
        "lat": 37.582601,
        "lon": 126.983303,
        "desc": "전통 한옥이 모여 있는 골목과 사진 명소."
    },
    {
        "name": "Changdeokgung Palace (창덕궁)",
        "lat": 37.582760,
        "lon": 126.991016,
        "desc": "유네스코 세계유산으로 지정된 궁궐과 후원(비원)."
    },
    {
        "name": "N Seoul Tower (N서울타워)",
        "lat": 37.551169,
        "lon": 126.988227,
        "desc": "도심 전망 명소 — 케이블카/야경으로 인기."
    },
    {
        "name": "Myeongdong Shopping Street (명동)",
        "lat": 37.563850,
        "lon": 126.986049,
        "desc": "쇼핑/스트리트푸드의 중심지. 뷰티 브랜드가 많음."
    },
    {
        "name": "Hongdae (홍대/홍익대학교)",
        "lat": 37.556264,
        "lon": 126.923539,
        "desc": "젊음의 거리, 스트리트 공연과 카페 문화."
    },
    {
        "name": "Insadong (인사동)",
        "lat": 37.574032,
        "lon": 126.986042,
        "desc": "전통 공예품과 찻집이 많은 문화 거리."
    },
    {
        "name": "Gwangjang Market (광장시장)",
        "lat": 37.570341,
        "lon": 126.999495,
        "desc": "전통시장 — 빈대떡, 비빔밥 등 길거리 음식 강추."
    },
    {
        "name": "Dongdaemun Design Plaza (DDP, 동대문디자인플라자)",
        "lat": 37.566295,
        "lon": 127.009394,
        "desc": "미래지향적 건축과 야간 쇼핑/야시장 명소."
    },
    {
        "name": "Hangang Park - Yeouido (한강공원 여의도)",
        "lat": 37.526014,
        "lon": 126.936822,
        "desc": "강변 산책, 피크닉, 자전거 라이딩으로 인기."
    }
]

# 기본 지도 (서울 중심)
m = folium.Map(location=[37.56, 126.98], zoom_start=12, control_scale=True)

# 마커 추가
for p in places:
    popup_html = f"""
    <b>{p['name']}</b><br>
    {p['desc']}<br>
    <i>위도: {p['lat']}, 경도: {p['lon']}</i>
    """
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=p["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 클러스터(선택사항) — 현재는 개별 마커만 사용
# folium.plugins.MarkerCluster().add_to(m)  # 필요시 활성화

# 지도 렌더링
st.subheader("Interactive map")
st_data = st_folium(m, width=1000, height=650)

# 사이드바: 장소 목록 클릭해 지도 중심 이동
st.sidebar.title("Places")
sel = st.sidebar.selectbox("Jump to", [p["name"] for p in places])
if st.sidebar.button("Center map on selected"):
    chosen = next(p for p in places if p["name"] == sel)
    # 새 지도를 만들고 선택 장소를 중심으로 이동 (st_folium는 리액티브 방식으로 작동)
    m2 = folium.Map(location=[chosen["lat"], chosen["lon"]], zoom_start=15, control_scale=True)
    for p in places:
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=f"<b>{p['name']}</b><br>{p['desc']}",
            tooltip=p["name"]
        ).add_to(m2)
    st_folium(m2, width=1000, height=650)

st.markdown("---")
st.markdown(
    "정보 출처: TripAdvisor, VisitKorea(한국관광공사), Klook, Viator 등. "
    "위치 좌표는 대표 지점을 사용했습니다."
)
st.caption("앱을 Streamlit Cloud에 배포하려면 이 저장소를 깃허브에 올리고 Streamlit Cloud에서 연결하세요.")
