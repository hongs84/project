import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.recommender import recommend_schools

st.set_page_config(
    page_title="AI 진로 네비게이터",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [class*="css"] {font-size:16px !important;}
.main-title {font-size:40px;font-weight:900;color:#0B1F3A;text-align:center;line-height:1.4;margin-bottom:30px;}
.sub-title {font-size:26px;font-weight:800;color:#1D4E89;margin-top:25px;margin-bottom:15px;}
.recommend-box {background:#FFFFFF;padding:24px;border-left:8px solid #1565C0;border-radius:16px;box-shadow:0 4px 10px rgba(0,0,0,0.08);margin-bottom:20px;height:100%;}
.big-text {font-size:18px;font-weight:500;line-height:1.8;}
.metric-container {background:linear-gradient(135deg, #EEF4FF, #FFFFFF);padding:20px;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;}
.future-box {background:#F8FBFF;padding:22px;border-radius:16px;box-shadow:0 2px 8px rgba(0,0,0,0.08);}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-title'>
직업계고 조기 진로 설정에 따른<br>
적성불일치 개선을 위한<br>
AI 진로 네비게이터 개발
</div>
""", unsafe_allow_html=True)

schools_df = pd.read_csv("schools.csv", encoding="utf-8-sig")

# 사이드바
st.sidebar.markdown("# 🎯 AI 학생 분석")
student_name = st.sidebar.text_input("학생 이름", "홍길동")
grade = st.sidebar.slider("내신 성적", 100, 300, 180)
preferred_region = st.sidebar.selectbox("희망 지역", sorted(schools_df["region"].unique()))
industry = st.sidebar.selectbox("희망 산업 분야", sorted(schools_df["industry"].unique()))
employment_goal = st.sidebar.selectbox("취업 목표 수준", ["대기업", "공기업", "연구직", "서비스직", "기술직"])
dormitory_needed = st.sidebar.selectbox("기숙사 희망 여부", ["Y", "N"])
college_preference = st.sidebar.selectbox("진학 희망 여부", ["취업", "진학", "혼합"])
max_distance = st.sidebar.slider("통학 가능 거리(km)", 0, 100, 30)
learning_style = st.sidebar.selectbox("학습 성향", ["실습형", "이론형", "혼합형"])
personality = st.sidebar.selectbox("성격 특성", ["외향형", "내향형", "분석형", "창의형"])

student_data = {
    "name": student_name,
    "grade": grade,
    "preferred_region": preferred_region,
    "industry": industry,
    "employment_goal": employment_goal,
    "dormitory_needed": dormitory_needed,
    "college_preference": college_preference,
    "max_distance": max_distance,
    "learning_style": learning_style,
    "personality": personality,
    "work_environment": industry,
    "parent_preference": preferred_region,
    "long_term_goal": employment_goal,
    "certificate_will": "높음"
}

results = recommend_schools(student_data, schools_df).reset_index(drop=True)
top_school = results.iloc[0]
ai_accuracy = min(98, int(top_school["score"]))

# 핵심 지표
st.markdown("<div class='sub-title'>📊 AI 종합 학생 분석 결과</div>", unsafe_allow_html=True)
cols = st.columns(4)
metrics = [
    ("분석 학교", top_school['school_name'], "#0B1F3A"),
    ("분석 학과", top_school['department'], "#0B1F3A"),
    ("AI 추천 정확도", f"{ai_accuracy}%", "#1565C0"),
    ("예상 취업률", f"{top_school['employment_rate']}%", "#2E7D32")
]
for col, (title, value, color) in zip(cols, metrics):
    with col:
        st.markdown(f"""<div class='metric-container'><div style='font-size:18px;color:#555;'>{title}</div><div style='font-size:26px;font-weight:800;color:{color};'>{value}</div></div>""", unsafe_allow_html=True)

# 적성 분석
st.markdown("<div class='sub-title'>🧠 AI 적성 분석 결과</div>", unsafe_allow_html=True)
st.success(f"{student_name} 학생은 {industry} 산업군과 {employment_goal} 목표에 적합하며, {top_school['department']} 진학 시 높은 만족도와 진로 지속성이 예상됩니다.")

# TOP3 추천 가로배치
st.markdown("<div class='sub-title'>🏆 AI 기반 TOP3 학교·학과 추천</div>", unsafe_allow_html=True)
rec_cols = st.columns(3)
for i in range(min(3, len(results))):
    row = results.iloc[i]
    with rec_cols[i]:
        st.markdown(f"""
        <div class='recommend-box'>
            <div style='font-size:26px;font-weight:800;color:#0B1F3A;'>{i+1}. {row['school_name']}</div>
            <div style='font-size:22px;font-weight:700;color:#1565C0;margin-bottom:10px;'>{row['department']}</div>
            <div class='big-text'>
            ✅ 적합도: {row['score']}점<br>
            ✅ 취업률: {row['employment_rate']}%<br>
            ✅ 자격증: {row['certification_rate']}%<br>
            ✅ 전공일치율: {row['major_match_rate']}%<br>
            ✅ 추천사유:<br>
            - 내신 적합<br>
            - 산업 적성 일치<br>
            - 취업성과 우수
            </div>
        </div>
        """, unsafe_allow_html=True)

# 세부 데이터 비교
st.markdown("<div class='sub-title'>📋 추천 학교 세부 데이터 비교 분석</div>", unsafe_allow_html=True)
comparison_cols = ["school_name","department","region","employment_rate","retention_rate","college_rate","certification_rate","major_match_rate","score"]
clean_results = results[comparison_cols].dropna(how="all")
st.dataframe(clean_results, use_container_width=True, hide_index=True)


# 미래 진로 분석
st.markdown("<div class='sub-title'>🚀 AI 미래 진로 분석</div>", unsafe_allow_html=True)
career_map = {
    "제조": ("스마트팩토리 엔지니어", "3,800만원", "삼성전자 / 현대자동차 / 한화오션"),
    "IT": ("AI·반도체 기술인재", "4,200만원", "삼성전자 / LG CNS / 네이버"),
    "서비스": ("관광·서비스 전문가", "3,000만원", "호텔신라 / 대한항공 / 공기업"),
    "연구": ("바이오·R&D 연구원", "4,000만원", "셀트리온 / 삼성바이오 / 정부출연연")
}
career, salary, companies = career_map.get(industry, ("산업 전문가", "3,500만원", "우수 기업군"))
colA, colB, colC = st.columns(3)
with colA:
    st.markdown(f"<div class='future-box'><b>예상 진로</b><br><br>{career}</div>", unsafe_allow_html=True)
with colB:
    st.markdown(f"<div class='future-box'><b>예상 초봉</b><br><br>{salary}</div>", unsafe_allow_html=True)
with colC:
    st.markdown(f"<div class='future-box'><b>추천 기업</b><br><br>{companies}</div>", unsafe_allow_html=True)

# AI 진로상담
st.markdown("<div class='sub-title'>💬 AI 진로 상담</div>", unsafe_allow_html=True)
user_question = st.text_input("진로/학교/학과에 대해 궁금한 점을 입력하세요:")
if user_question:

    q = user_question.lower()

    filtered = results.copy()

    # 성격 반영
    if "내성" in q:
        filtered = filtered[
            filtered["preferred_personality"].isin(["내향형", "분석형"])
        ]

    if "외향" in q:
        filtered = filtered[
            filtered["preferred_personality"].isin(["외향형", "창의형"])
        ]

    # 취업 목표 반영
    if "대기업" in q:
        filtered = filtered.sort_values(
            by=["employment_rate", "major_match_rate"],
            ascending=False
        )

    elif "공기업" in q:
        filtered = filtered[
            filtered["employment_support_level"].isin(["공기업", "대기업"])
        ]

    elif "연구" in q:
        filtered = filtered[
            filtered["industry"] == "연구"
        ]

    # 지역 조건
    if "충남" in q:
        filtered = filtered[
            filtered["region"].str.contains("충남")
        ]

    if filtered.empty:
        filtered = results.copy()

    best = filtered.iloc[0]

    answer = f"""
### 🎯 AI 진로 상담 분석 결과

**질문:** {user_question}

### 📌 추천 학교:
**{best['school_name']} - {best['department']}**

### 📊 추천 이유:
- 성격 특성과 학과 적합성 반영
- 취업 목표 조건 분석
- 취업률 {best['employment_rate']}%
- 전공일치율 {best['major_match_rate']}%
- 유지취업률 {best['retention_rate']}%
- 산업 전망 우수

### 🚀 종합 의견:
{student_name} 학생의 질문 조건을 반영했을 때,
현재 가장 적합한 선택지는 위 학교이며,
특히 {best['industry']} 분야에서 높은 진로 안정성과 취업 가능성을 기대할 수 있습니다.
"""

    st.markdown(answer)

# 최종 결론
st.markdown("<div class='sub-title'>🎯 최종 AI 진로 설계 결론</div>", unsafe_allow_html=True)
st.warning(f"{student_name} 학생에게 가장 추천되는 선택은 {top_school['school_name']}의 {top_school['department']}입니다. 내신, 적성, 취업성과, 산업 전망을 종합적으로 고려했을 때 가장 후회 가능성이 낮은 선택입니다.")
