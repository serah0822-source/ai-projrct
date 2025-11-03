import streamlit as st

st.set_page_config(page_title="MBTI 취향 책·영화 추천", page_icon="📚")

st.title("📚 MBTI 맞춤 책 & 영화 추천 🎬")
st.write("너의 MBTI를 골라보면 취향 저격 콘텐츠를 추천해줄게! 😎✨")

mbti_types = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

selected_mbti = st.selectbox("👇 너의 MBTI를 골라줘!", mbti_types)

recommendations = {
    "INTJ": {
        "books": ["📘 『지적 대화를 위한 넓고 얕은 지식』", "📗 『코스모스』"],
        "movies": ["🎥 인터스텔라", "🎞 인셉션"]
    },
    "INTP": {
        "books": ["📘 『생각의 탄생』", "📗 『총,균,쇠』"],
        "movies": ["🎥 소셜 네트워크", "🎞 매트릭스"]
    },
    "ENTJ": {
        "books": ["📘 『원씽』", "📗 『위대한 개츠비』"],
        "movies": ["🎥 월스트리트: 머니 네버 슬립스", "🎞 오션스 일레븐"]
    },
    "ENTP": {
        "books": ["📘 『창의성의 탄생』", "📗 『호모 데우스』"],
        "movies": ["🎥 아이언맨", "🎞 빅 쇼트"]
    },
    "INFJ": {
        "books": ["📘 『데미안』", "📗 『연금술사』"],
        "movies": ["🎥 월터의 상상은 현실이 된다", "🎞 어바웃 타임"]
    },
    "INFP": {
        "books": ["📘 『어린왕자』", "📗 『종이 여자』"],
        "movies": ["🎥 라라랜드", "🎞 조제, 호랑이 그리고 물고기들"]
    },
    "ENFJ": {
        "books": ["📘 『미움받을 용기』", "📗 『아몬드』"],
        "movies": ["🎥 인사이드 아웃", "🎞 원더"]
    },
    "ENFP": {
        "books": ["📘 『하퍼 리가 쓴 나무는 언제나 우람하게』", "📗 『나미야 잡화점의 기적』"],
        "movies": ["🎥 소울", "🎞 이터널 선샤인"]
    },
    "ISTJ": {
        "books": ["📘 『미라클 모닝』", "📗 『습관의 힘』"],
        "movies": ["🎥 셜록 홈즈", "🎞 그레이의 50가지 그림자"]
    },
    "ISFJ": {
        "books": ["📘 『마음으로부터 일곱 번』", "📗 『아가씨와 밤』"],
        "movies": ["🎥 인턴", "🎞 벤자민 버튼의 시간은 거꾸로 간다"]
    },
    "ESTJ": {
        "books": ["📘 『나는 단순하게 살기로 했다』", "📗 『포지셔닝』"],
        "movies": ["🎥 위대한 쇼맨", "🎞 머니볼"]
    },
    "ESFJ": {
        "books": ["📘 『90년생이 온다』", "📗 『작별인사』"],
        "movies": ["🎥 인사이드 아웃", "🎞 엽기적인 그녀"]
    },
    "ISTP": {
        "books": ["📘 『호모 루덴스』", "📗 『사피엔스』"],
        "movies": ["🎥 터미네이터", "🎞 젠틀맨"]
    },
    "ISFP": {
        "books": ["📘 『파리의 아파트』", "📗 『달러구트 꿈 백화점』"],
        "movies": ["🎥 콜 미 바이 유어 네임", "🎞 월터의 상상은 현실이 된다"]
    },
    "ESTP": {
        "books": ["📘 『더 해빗』", "📗 『골든 서클』"],
        "movies": ["🎥 베이비 드라이버", "🎞 분노의 질주"]
    },
    "ESFP": {
        "books": ["📘 『트렌드 코리아』", "📗 『그릿』"],
        "movies": ["🎥 싱 스트리트", "🎞 하이 스쿨 뮤지컬"]
    }
}

if st.button("📌 추천 받기!"):
    st.subheader(f"✨ {selected_mbti} 유형 추천 리스트!")
    st.write("📚 **책 추천**")
    for book in recommendations[selected_mbti]["books"]:
        st.write(f"• {book}")
    st.write("\n🎬 **영화 추천**")
    for movie in recommendations[selected_mbti]["movies"]:
        st.write(f"• {movie}")
    st.write("\n즐감·즐독 하고 와서 후기 남겨줘! 😆💬")
