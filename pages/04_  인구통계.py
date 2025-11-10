import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="인구 연령별 그래프", layout="wide")

st.title("지역구별 나이 vs 인구수 꺽은선 그래프 (Streamlit + Plotly)")
st.markdown(
    "CSV에서 0세~100세 이상 컬럼을 찾아 나이(가로)와 인구수(세로) 꺽은선 그래프를 그립니다."
)

uploaded_file = st.file_uploader("population.csv 파일 업로드 (옵션)", type=["csv"])

@st.cache_data
def load_df(uploaded):
    if uploaded is not None:
        df = pd.read_csv(uploaded, encoding='cp949', low_memory=False)
    else:
        try:
            df = pd.read_csv("population.csv", encoding='cp949', low_memory=False)
        except FileNotFoundError:
            df = None
    return df

df = load_df(uploaded_file)

if df is None:
    st.warning("population.csv 파일을 찾을 수 없습니다. 파일을 업로드해 주세요.")
    st.stop()

def clean_numeric_cols(df):
    df = df.copy()
    numeric_cols = [c for c in df.columns if re.search(r'세', c)]
    for c in numeric_cols:
        df[c] = (
            df[c].astype(str)
            .str.replace(",", "")
            .str.replace(r"[^0-9]", "", regex=True)
            .replace("", "0")
            .astype(int)
        )
    return df, numeric_cols

df_clean, age_cols = clean_numeric_cols(df)

possible_name_cols = [c for c in df.columns if any(k in c for k in ["행정구역", "지역", "행정"])]
if possible_name_cols:
    name_col = possible_name_cols[0]
else:
    name_col = df.select_dtypes(include="object").columns[0]

st.sidebar.write("## 설정")
region = st.sidebar.selectbox("지역구 선택", df_clean[name_col].tolist())

show_table = st.sidebar.checkbox("원본 연령별 표 보기", value=False)
log_scale = st.sidebar.checkbox("세로축 로그 스케일", value=False)

def extract_age_population(row, age_columns):
    records = []
    for c in age_columns:
        m = re.search(r'(\d+)[^\d]*$', c)
        if m:
            age = int(m.group(1))
        else:
            if "100" in c:
                age = 100
            else:
                continue
        pop = int(row[c])
        records.append({"age": age, "population": pop, "col": c})
    df_age = pd.DataFrame.from_records(records)
    df_age = df_age.sort_values("age").reset_index(drop=True)
    return df_age

selected_row = df_clean[df_clean[name_col] == region].iloc[0]
age_pop_df = extract_age_population(selected_row, age_cols)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"선택지역: {region}")
    if show_table:
        st.dataframe(age_pop_df[["age", "population"]].set_index("age"))

with col2:
    st.subheader("나이(가로) vs 인구수(세로) — 꺽은선 그래프")
    fig = px.line(age_pop_df, x="age", y="population", markers=True,
                  labels={"age": "나이", "population": "인구수"},
                  hover_data=["col", "population"])
    fig.update_layout(hovermode="x unified", template="plotly_white", autosize=True)
    if log_scale:
        fig.update_yaxes(type="log")
    st.plotly_chart(fig, use_container_width=True)

csv_buffer = age_pop_df.to_csv(index=False, encoding="utf-8-sig")
st.download_button("선택지역 연령별 CSV 다운로드", data=csv_buffer, file_name=f"{region}_age_population.csv", mime="text/csv")

st.markdown("---")
st.info("앱을 Streamlit Cloud(또는 Streamlit Community Cloud)에 배포하려면 app.py와 requirements.txt를 함께 업로드하세요.")
