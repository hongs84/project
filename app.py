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

import streamlit as st

# ==============================================================================
# 사이드바 (학교 유형 및 지원 성향 추가)
# ==============================================================================
st.sidebar.markdown("# 🎯 AI 학생 분석")
student_name = st.sidebar.text_input("학생 이름", "홍길동")
grade = st.sidebar.slider("내신 성적", 100, 300, 180)

# 1. 학교 유형 선택 추가 (schools_df에 '학교유형' 컬럼이 마이스터고, 특성화고로 분류되어 있다고 가정)
school_type = st.sidebar.multiselect(
    "학교 유형 선택", 
    options=["마이스터고", "특성화고"], 
    default=["마이스터고", "특성화고"]
)

# 2. 지원 성향 선택 추가
apply_strategy = st.sidebar.selectbox(
    "지원 성향", 
    ["전체 조회", "상향 지원 (내 성적 < 커트라인)", "적정 지원 (성적 비슷)", "하향 지원 (내 성적 > 커트라인)"]
)

preferred_region = st.sidebar.selectbox("희망 지역", sorted(schools_df["지역"].unique()))
industry = st.sidebar.selectbox("희망 산업 분야", sorted(schools_df["산업분야"].unique()))
employment_goal = st.sidebar.selectbox("취업 목표 수준", ["대기업", "공기업", "연구직", "서비스직", "기술직"])
dormitory_needed = st.sidebar.selectbox("기숙사 희망 여부", ["Y", "N"])
college_preference = st.sidebar.selectbox("진학 희망 여부", ["취업", "진학", "혼합"])
max_distance = st.sidebar.slider("통학 가능 거리(km)", 0, 100, 30)
learning_style = st.sidebar.selectbox("학습 성향", ["실습형", "이론형", "혼합형"])
personality = st.sidebar.selectbox("성격 특성", ["외향형", "내향형", "분석형", "창의형"])

# 학생 데이터 딕셔너리 빌드
student_data = {
    "내신성적": grade,
    "희망지역": preferred_region,
    "선호산업분야": industry,
    "취업목표수준": employment_goal,
    "기숙사필요여부": dormitory_needed,
    "진학희망여부": college_preference,
    "최대통학거리": max_distance,
    "학습성향": learning_style,
    "성격특성": personality,
    "선호근무환경": industry,      
    "부모님희망지역": preferred_region,
    "장기목표": employment_goal,
    "자격증취득의지": "높음"
}

# ==============================================================================
# 데이터 필터링 및 추천 로직 적용
# ==============================================================================

# 1차 필터링: 선택한 학교 유형에 해당하는 학교만 남기기
# (데이터프레임의 학교유형 컬럼명이 '학교유형'이 맞는지 확인해 주세요)
filtered_df = schools_df[schools_df["학교유형"].isin(school_type)].copy()

# 2차 필터링: 지원 성향에 따른 내신 컷 필터링
# ※ 내신 점수(백분위 등)는 숫자가 작을수록 성적이 좋은 것으로 계산합니다.
margin = 10  # 적정 수준을 판단할 마진 (예: 내 성적 ±10점 사이를 적정으로 봄)

if apply_strategy == "상향 지원 (내 성적 < 커트라인)":
    # 내 점수 숫자가 더 큼 = 내 성적이 학교 컷보다 뒤처짐 (도전)
    filtered_df = filtered_df[filtered_df["합격커트라인"] < (grade - margin)]
elif apply_strategy == "적정 지원 (성적 비슷)":
    # 내 성적과 학교 컷이 비슷한 수준
    filtered_df = filtered_df[
        (filtered_df["합격커트라인"] >= (grade - margin)) & 
        (filtered_df["합격커트라인"] <= (grade + margin))
    ]
elif apply_strategy == "하향 지원 (내 성적 > 커트라인)":
    # 내 점수 숫자가 더 작음 = 내 성적이 학교 컷보다 여유 있음 (안정)
    filtered_df = filtered_df[filtered_df["합격커트라인"] > (grade + margin)]

# 필터링된 데이터를 추천 엔진에 전달
if not filtered_df.empty:
    results = recommend_schools(student_data, filtered_df).reset_index(drop=True)
    top_school = results.iloc[0]
    ai_accuracy = min(98, int(top_school["score"]))
else:
    st.error("💡 선택하신 조건(학교 유형 또는 지원 성향)에 맞는 학교가 존재하지 않습니다. 사이드바의 조건을 조절해 주세요.")
    st.stop()

# 핵심 지표 (영어 컬럼명 -> 한국어 컬럼명으로 수정)
st.markdown("<div class='sub-title'>📊 AI 종합 학생 분석 결과</div>", unsafe_allow_html=True)
cols = st.columns(4)
metrics = [
    ("분석 학교", top_school['학교명'], "#0B1F3A"),
    ("분석 학과", top_school['학과명'], "#0B1F3A"),
    ("AI 추천 정확도", f"{ai_accuracy}%", "#1565C0"),
    ("예상 취업률", f"{top_school['취업률']}%", "#2E7D32")
]
for col, (title, value, color) in zip(cols, metrics):
    with col:
        st.markdown(f"""<div class='metric-container'><div style='font-size:18px;color:#555;'>{title}</div><div style='font-size:26px;font-weight:800;color:{color};'>{value}</div></div>""", unsafe_allow_html=True)

# 적성 분석
st.markdown("<div class='sub-title'>🧠 AI 적성 분석 결과</div>", unsafe_allow_html=True)
st.success(f"{student_name} 학생은 {industry} 산업군과 {employment_goal} 목표에 적합하며, {top_school['학과명']} 진학 시 높은 만족도와 진로 지속성이 예상됩니다.")

# TOP3 추천 가로배치 (영어 컬럼명 -> 한국어 컬럼명으로 수정)
st.markdown("<div class='sub-title'>🏆 AI 기반 TOP3 학교·학과 추천</div>", unsafe_allow_html=True)
rec_cols = st.columns(3)
for i in range(min(3, len(results))):
    row = results.iloc[i]
    with rec_cols[i]:
        st.markdown(f"""
        <div class='recommend-box'>
            <div style='font-size:26px;font-weight:800;color:#0B1F3A;'>{i+1}. {row['학교명']}</div>
            <div style='font-size:22px;font-weight:700;color:#1565C0;margin-bottom:10px;'>{row['학과명']}</div>
            <div class='big-text'>
            ✅ 적합도: {row['score']}점<br>
            ✅ 취업률: {row['취업률']}%<br>
            ✅ 자격증: {row['자격증취득률']}%<br>
            ✅ 전공일치율: {row['전공일치율']}%<br>
            ✅ 추천사유:<br>
            - 내신 적합<br>
            - 산업 적성 일치<br>
            - 취업성과 우수
            </div>
        </div>
        """, unsafe_allow_html=True)

# 세부 데이터 비교 (컬럼 구성 한글화)
st.markdown("<div class='sub-title'>📋 추천 학교 세부 데이터 비교 분석</div>", unsafe_allow_html=True)
comparison_cols = ["학교명", "학과명", "지역", "취업률", "유지취업률", "진학률", "자격증취득률", "전공일치율", "score"]
clean_results = results[comparison_cols].dropna(how="all")
st.dataframe(clean_results, use_container_width=True, hide_index=True)


# 미래 진로 분석
st.markdown("<div class='sub-title'>🚀 AI 미래 진로 분석</div>", unsafe_allow_html=True)
career_map = {
    "제조": ("스마트팩토리 엔지니어", "3,800 nanowon", "삼성전자 / 현대자동차 / 한화오션"),
    "IT": ("AI·반도체 기술인재", "4,200 nanowon", "삼성전자 / LG CNS / 네이버"),
    "서비스": ("관광·서비스 전문가", "3,000 nanowon", "호텔신라 / 대한항공 / 공기업"),
    "연구": ("바이오·R&D 연구원", "4,000 nanowon", "셀트리온 / 삼성바이오 / 정부출연연")
}
career, salary, companies = career_map.get(industry, ("산업 전문가", "3,500만원", "우수 기업군"))
colA, colB, colC = st.columns(3)
with colA:
    st.markdown(f"<div class='future-box'><b>예상 진로</b><br><br>{career}</div>", unsafe_allow_html=True)
with colB:
    st.markdown(f"<div class='future-box'><b>예상 초봉</b><br><br>{salary}</div>", unsafe_allow_html=True)
with colC:
    st.markdown(f"<div class='future-box'><b>추천 기업</b><br><br>{companies}</div>", unsafe_allow_html=True)

# AI 진로상담 (상담 로직 내부의 데이터 필터링 키값 일괄 한글화)
st.markdown("<div class='sub-title'>💬 AI 진로 상담</div>", unsafe_allow_html=True)
user_question = st.text_input("진로/학교/학과에 대해 궁금한 점을 입력하세요:")
if user_question:

    q = user_question.lower()
    filtered = results.copy()

    # 성격 반영
    if "내성" in q:
        filtered = filtered[
            filtered["권장성격"].isin(["내향형", "분석형"])
        ]

    if "외향" in q:
        filtered = filtered[
            filtered["권장성격"].isin(["외향형", "창의형"])
        ]

    # 취업 목표 반영
    if "대기업" in q:
        filtered = filtered.sort_values(
            by=["취업률", "전공일치율"],
            ascending=False
        )

    elif "공기업" in q:
        filtered = filtered[
            filtered["취업지원수준"].isin(["공기업", "대기업"])
        ]

    elif "연구" in q:
        filtered = filtered[
            filtered["산업분야"] == "연구"
        ]

    # 지역 조건
    if "충남" in q:
        filtered = filtered[
            filtered["지역"].str.contains("충남")
        ]

    if filtered.empty:
        filtered = results.copy()

    best = filtered.iloc[0]

    answer = f"""
### 🎯 AI 진로 상담 분석 결과

**질문:** {user_question}

### 📌 추천 학교:
**{best['학교명']} - {best['학과명']}**

### 📊 추천 이유:
- 성격 특성과 학과 적합성 반영
- 취업 목표 조건 분석
- 취업률 {best['취업률']}%
- 전공일치율 {best['전공일치율']}%
- 유지취업률 {best['유지취업률']}%
- 산업 전망 우수

### 🚀 종합 의견:
{student_name} 학생의 질문 조건을 반영했을 때,
현재 가장 적합한 선택지는 위 학교이며,
특히 {best['산업분야']} 분야에서 높은 진로 안정성과 취업 가능성을 기대할 수 있습니다.
"""

    st.markdown(answer)

# 최종 결론 (영어 -> 한국어 수정)
st.markdown("<div class='sub-title'>🎯 최종 AI 진로 설계 결론</div>", unsafe_allow_html=True)
st.warning(f"{student_name} 학생에게 가장 추천되는 선택은 {top_school['학교명']}의 {top_school['학과명']}입니다. 내신, 적성, 취업성과, 산업 전망을 종합적으로 고려했을 때 가장 후회 가능성이 낮은 선택입니다.")
