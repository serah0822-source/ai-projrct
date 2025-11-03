import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
st.write('안녕하세요, 만나서 반갑습니다!')
name=st.text_input('이름을 입력해주세요!')
if st.button('인사말 생성'):
  st.write(name+'님! 반갑습니다!')
  st.balloons()
# mbti_career_app.py
import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천 🌱", layout="centered")

st.title("✨ MBTI 진로 추천기 (청소년 친화적) ✨")
st.write("자기 MBTI를 골라봐! 각 유형에 맞는 **진로 2가지**와 추천 학과, 잘 맞는 성격을 알려줄게 😊")

MBTI_LIST = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

CAREER_DB = {
    "ISTJ": [
        {"job":"회계사 / 세무사 📊",
         "majors":"회계학, 경영학, 세무학",
         "personality":"정확하고 책임감 강함, 규칙·절차 잘 지킴, 꼼꼼한 실무형"},
        {"job":"품질관리 엔지니어 🧪",
         "majors":"화학공학, 기계공학, 산업공학",
         "personality":"디테일 중시, 계획 따라 안정적으로 일함"}
    ],
    "ISFJ": [
        {"job":"간호사 / 보건관리자 🩺",
         "majors":"간호학, 보건학, 사회복지학",
         "personality":"타인을 돌보는 성향, 책임감 있고 신뢰감 줌"},
        {"job":"초등교사 / 유아교육자 🎒",
         "majors":"유아교육학, 교육학",
         "personality":"차분하고 헌신적, 안정적인 환경에서 강함"}
    ],
    "INFJ": [
        {"job":"상담사 / 임상심리사 💬",
         "majors":"심리학, 상담심리학",
         "personality":"사람의 감정에 공감 잘함, 의미 있는 일을 추구"},
        {"job":"작가 / 콘텐츠 크리에이터 ✍️",
         "majors":"문예창작, 커뮤니케이션, 미디어학",
         "personality":"창의적이고 통찰력 있음, 메시지 전달에 강함"}
    ],
    "INTJ": [
        {"job":"연구원 (R&D) 🔬",
         "majors":"물리/화학/생명공학, 컴퓨터공학",
         "personality":"전략적 사고, 계획 세워 목표 달성 좋아함"},
        {"job":"데이터 사이언티스트 📈",
         "majors":"통계학, 컴퓨터공학, 산업공학",
         "personality":"논리적 분석, 복잡한 문제 풀기 즐김"}
    ],
    "ISTP": [
        {"job":"기계 정비사 / 엔지니어 🔧",
         "majors":"기계공학, 전기공학",
         "personality":"실무 중심, 손재주 좋고 즉각 해결 능력"},
        {"job":"UX 엔지니어 / 프로토타입 제작자 🛠️",
         "majors":"디자인공학, 산업디자인, 컴퓨터공학",
         "personality":"현장감각 좋고 실험적 시도 선호"}
    ],
    "ISFP": [
        {"job":"셰프 / 제과제빵사 🍰",
         "majors":"조리학과, 제과제빵학",
         "personality":"감각적이고 손으로 만드는 일에 행복함, 섬세함"},
        {"job":"그래픽 디자이너 🎨",
         "majors":"시각디자인, 산업디자인",
         "personality":"창의적이고 감성적, 미적 감각 우수"}
    ],
    "INFP": [
        {"job":"문예창작가 / 시나리오 작가 📚",
         "majors":"문예창작, 국문학, 영화학",
         "personality":"가치 중심, 상상력 풍부, 감정 표현에 능함"},
        {"job":"NGO / 사회적기업 활동가 🌱",
         "majors":"사회복지학, 국제학, 환경학",
         "personality":"이상 추구, 사람과 사회를 개선하려는 열정"}
    ],
    "INTP": [
        {"job":"소프트웨어 개발자 💻",
         "majors":"컴퓨터공학, 전산학, 수학",
         "personality":"논리적이고 문제 해결을 즐김, 독립적 탐구 선호"},
        {"job":"연구 과학자 🔭",
         "majors":"물리학, 수학, 컴퓨터과학",
         "personality":"이론적 호기심, 복잡한 아이디어에 빠짐"}
    ],
    "ESTP": [
        {"job":"영업 / 마케팅 전문가 💼",
         "majors":"경영학, 광고·홍보학",
         "personality":"사교적이고 행동력이 빠름, 결과 지향적"},
        {"job":"응급구조사 / 소방관 🚒",
         "majors":"응급구조학, 소방안전학",
         "personality":"위기 상황에서 침착하고 실전 능력 좋음"}
    ],
    "ESFP": [
        {"job":"연예·공연 산업 (배우·MC) 🎤",
         "majors":"연극영화과, 방송연예학",
         "personality":"사교적이고 무대 적응력 뛰어남, 즉흥적 매력"},
        {"job":"이벤트 플래너 / 호스피탈리티 🌟",
         "majors":"호텔관광, 이벤트경영",
         "personality":"사람을 즐겁게 하는 일에 기쁨을 느낌"}
    ],
    "ENFP": [
        {"job":"광고카피라이터 / 콘텐츠 기획자 ✨",
         "majors":"커뮤니케이션, 광고홍보학, 문예창작",
         "personality":"아이디어 뿜뿜, 사람과의 연결을 즐김"},
        {"job":"창업가 / 스타트업 기획자 🚀",
         "majors":"경영학, 창업학, ICT 관련 학과",
         "personality":"창의적이고 도전적, 다양한 일에 흥미"}
    ],
    "ENTP": [
        {"job":"제품 기획자 / 혁신 컨설턴트 🧠",
         "majors":"경영학, 산업공학, 디자인경영",
         "personality":"논쟁을 즐기고 새로운 발상으로 문제 해결"},
        {"job":"변호사 / 논리 기반 직업 ⚖️",
         "majors":"법학, 국제법",
         "personality":"논리적 설득력, 빠른 아이디어 전환"}
    ],
    "ESTJ": [
        {"job":"공무원 / 행정가 🏛️",
         "majors":"행정학, 정치외교학, 법학",
         "personality":"조직 운영·관리 능력, 책임감 강함"},
        {"job":"프로젝트 매니저 (PM) 📋",
         "majors":"경영학, 산업공학, 정보시스템",
         "personality":"실행력 있고 조직화에 능숙함"}
    ],
    "ESFJ": [
        {"job":"홍보·고객서비스 매니저 💬",
         "majors":"커뮤니케이션, 호텔관광, 경영학",
         "personality":"사교적이고 배려심 많음, 팀워크에 강함"},
        {"job":"보건행정 / 의료코디네이터 🏥",
         "majors":"보건행정, 간호학, 의료경영",
         "personality":"사람 돕기 좋아하고 안정감 주는 성격"}
    ],
    "ENFJ": [
        {"job":"교사 / 교육 컨설턴트 🌟",
         "majors":"교육학, 상담교육, 사회복지학",
         "personality":"사람의 성장 돕는 걸 좋아함, 리더십 있음"},
        {"job":"HR / 조직문화 기획자 🤝",
         "majors":"인사·조직학, 경영학, 심리학",
         "personality":"타인 이해 능력, 조직 조율에 능함"}
    ],
    "ENTJ": [
        {"job":"경영자 / 전략 컨설턴트 📈",
         "majors":"경영학, 경제학, 산업공학",
         "personality":"목표 지향적·리더십 강함, 전략적 사고"},
        {"job":"투자분석가 / 금융전문가 💹",
         "majors":"경제학, 금융학, 통계학",
         "personality":"결단력 있고 숫자 이해도 높음"}
    ],
}

def show_career(mbti: str):
    st.markdown(f"### 😎 선택한 MBTI: **{mbti}**")
    careers = CAREER_DB.get(mbti, [])
    for idx, c in enumerate(careers, 1):
        st.markdown(f"---")
        st.markdown(f"#### {idx}. {c['job']}")
        st.markdown(f"- **추천 학과:** {c['majors']}")
        st.markdown(f"- **어떤 성격이 잘 맞을까?** {c['personality']}")
        # 한 줄 요약 감성 멘트
        if idx == 1:
            st.info("첫 번째 제안은 너의 강점을 바로 살릴 수 있는 실전형 진로야. 🌱")
        else:
            st.success("두 번째 제안은 관심을 넓히거나 다른 장점을 살릴 수 있는 옵션이야. ✨")

st.sidebar.header("설정")
st.sidebar.write("MBTI를 골라주세요")

selected = st.sidebar.selectbox("MBTI 선택", MBTI_LIST, index=10)

st.sidebar.write(" ")
st.sidebar.write("👉 결과를 보고 마음에 들면 진로 노트에 적어봐!")

show_career(selected)

st.markdown("---")
st.markdown("### 팁 한마디 💡")
st.markdown(
    "- 관심 있는 진로가 보이면 관련 학과 수업, 동아리, 체험처(현장실습 등)를 직접 경험해 봐.  
- MBTI는 성향을 알려주는 도구일 뿐 절대 '운명'이 아니야 — 네가 좋아하고 노력하면 뭐든 잘할 수 있어! 💪"
)

st.markdown("### 더 해보고 싶은 기능?")
st.markdown("- 학교 과목과 연결한 맞춤 진로 추천, 심층 성격 분석, 진로별 실제 직업 인터뷰 요약 등도 만들어줄게 — 원하면 말해줘! 😊")

st.caption("앱 제작: MBTI 진로 추천기 · Streamlit 버전")
