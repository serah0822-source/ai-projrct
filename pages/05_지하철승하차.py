# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="지하철 승하차 Top10", layout="wide")

@st.cache_data
def load_data(path: str = "지하철호선별역별승하차인원정보.csv"):
    """
    기본 경로에 파일이 있으면 불러오고, 아니면 None 반환.
    Streamlit Cloud에서는 프로젝트 루트에 CSV를 넣거나 아래에서 업로드하세요.
    """
    p = Path(path)
    if p.exists():
        try:
            # 한글 인코딩 처리 (공공데이터는 보통 cp949)
            df = pd.read_csv(p, encoding='cp949')
        except Exception:
            df = pd.read_csv(p, encoding='utf-8', errors='replace')
        # 컬럼 정리 (공백이나 이상한 문자가 섞여있을 가능성 대비)
        df.columns = [c.strip() for c in df.columns]
        # 합계 컬럼 추가
        df["합계"] = df["승차총승객수"] + df["하차총승객수"]
        # 날짜 컬럼을 문자열(또는 datetime)로 다루기 쉽게 변환
        df["사용일자_str"] = df["사용일자"].astype(str)
        # YYYYMMDD 형태를 날짜로 변환 (실패하면 원본 문자열 유지)
        try:
            df["사용일자_dt"] = pd.to_datetime(df["사용일자_str"], format="%Y%m%d")
        except Exception:
            df["사용일자_dt"] = pd.to_datetime(df["사용일자_str"], errors="coerce")
        return df
    else:
        return None

def make_colors_top10(n):
    """
    첫 번째는 빨강(#ff0000).
    나머지 n-1개는 파란색 계열에서 점점 흐려지는(밝아지는) 그라데이션 생성.
    반환: hex 색 문자열 리스트 길이 n
    """
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(*[max(0,min(255,int(round(x)))) for x in rgb])

    colors = []
    # 1등 빨강
    colors.append("#ff0000")
    if n <= 1:
        return colors
    # 파란색 기본 (Plotly 기본 blue-ish)
    blue_hex = "#1f77b4"
    white_rgb = (255,255,255)
    blue_rgb = hex_to_rgb(blue_hex)
    # 나머지에 대해 0 -> 원래 파란색, 1 -> 흰색(가장 연한)
    steps = n - 1
    for i in range(steps):
        t = i / max(1, steps - 1)  # 0..1
        # t=0 -> 원래 파랑, t=1 -> 흰색
        r = blue_rgb[0] + (white_rgb[0] - blue_rgb[0]) * t
        g = blue_rgb[1] + (white_rgb[1] - blue_rgb[1]) * t
        b = blue_rgb[2] + (white_rgb[2] - blue_rgb[2]) * t
        colors.append(rgb_to_hex((r,g,b)))
    return colors

# --- UI ---
st.title("📊 지하철 호선별 역별 승·하차 Top 10 (Streamlit + Plotly)")
st.markdown("2025년 10월 데이터 중 하루를 골라, 선택한 호선에서 **승차+하차 합계**가 큰 상위 10개 역을 보여줍니다.")

# 데이터 로드 (프로젝트 루트에 파일이 있으면 자동으로 불러옴)
df = load_data()

if df is None:
    st.warning("프로젝트 루트에 `지하철호선별역별승하차인원정보.csv` 파일이 없습니다. 파일을 업로드해 주세요.")
    uploaded = st.file_uploader("CSV 파일 업로드 (인코딩: cp949 권장)", type=["csv"])
    if uploaded is not None:
        # 업로드된 파일을 판다스로 읽음
        try:
            df = pd.read_csv(uploaded, encoding='cp949')
        except Exception:
            df = pd.read_csv(uploaded, encoding='utf-8', errors='replace')
        df.columns = [c.strip() for c in df.columns]
        df["합계"] = df["승차총승객수"] + df["하차총승객수"]
        df["사용일자_str"] = df["사용일자"].astype(str)
        try:
            df["사용일자_dt"] = pd.to_datetime(df["사용일자_str"], format="%Y%m%d")
        except Exception:
            df["사용일자_dt"] = pd.to_datetime(df["사용일자_str"], errors="coerce")
    else:
        st.stop()

# 좌측 컨트롤
with st.sidebar:
    st.header("필터")
    # 사용 가능한 날짜 목록 (YYYY-MM-DD 포맷으로 표시)
    dates = df["사용일자_dt"].dropna().sort_values().unique()
    if len(dates) == 0:
        st.error("날짜 정보가 유효하지 않습니다.")
        st.stop()
    # 날짜 선택 위젯 (날짜 형식으로 표시)
    selected_date = st.date_input("날짜 선택 (2025년 10월 중 하루)", value=dates[0].date(), min_value=dates.min().date(), max_value=dates.max().date())
    # 호선 선택
    lines = sorted(df["노선명"].unique())
    selected_line = st.selectbox("호선 선택", options=lines, index=0)

# 필터 적용
# 선택된 date는 datetime.date -> 변환 비교
selected_date_str = pd.to_datetime(selected_date).strftime("%Y%m%d")
filtered = df[(df["사용일자_str"] == selected_date_str) & (df["노선명"] == selected_line)].copy()

st.markdown(f"**선택:** 날짜 `{selected_date.strftime('%Y-%m-%d')}` / 호선 `{selected_line}`")

if filtered.empty:
    st.info("선택된 날짜와 호선에 해당하는 데이터가 없습니다. 다른 날짜 또는 호선을 선택해 주세요.")
    st.stop()

# 역별 합계 집계 (역 이름 기준)
grouped = (
    filtered
    .groupby("역명", as_index=False)
    .agg({"합계":"sum"})
    .sort_values("합계", ascending=False)
)

top10 = grouped.head(10).reset_index(drop=True)

# 색상 만들기 (1등 빨강, 나머지 파랑->흰 그라데이션)
colors = make_colors_top10(len(top10))

# Plotly 막대그래프
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=top10["역명"],
        y=top10["합계"],
        marker=dict(color=colors, line=dict(width=0.5, color="rgba(0,0,0,0.1)")),
        hovertemplate="<b>%{x}</b><br>합계: %{y:,}<extra></extra>"
    )
)

fig.update_layout(
    title=f"{selected_date.strftime('%Y-%m-%d')} · {selected_line} — 승차+하차 합계 상위 10개 역",
    xaxis_title="역명",
    yaxis_title="승차+하차 합계 (명)",
    template="plotly_white",
    margin=dict(l=40, r=20, t=70, b=120),
    xaxis_tickangle=-45,
    height=600
)

# 서브텍스트: 순위 표
with st.container():
    col1, col2 = st.columns([2,1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Top 10 역 (순위)")
        # 표 스타일링 간단 출력
        st.table(top10.assign(순위=top10.index+1)[["순위","역명","합계"]].rename(columns={"역명":"역","합계":"승하차합계"}))

st.markdown("---")
st.caption("※ 데이터는 제공된 CSV 파일을 사용합니다. 날짜/호선 필터링은 CSV의 '사용일자'와 '노선명' 컬럼을 기준으로 합니다.")
