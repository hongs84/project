def calculate_score(student, school):
    """
    학생 조건과 학교 데이터를 기반으로 적합도 점수 계산
    중요도 높은 요소를 상위 가중치로 반영
    """

    score = 0

    # 1. 내신 성적 (가장 중요)
    if student["grade"] <= school["cutoff_grade"]:
        score += 20

    # 2. 희망 지역
    if student["preferred_region"] == school["region"]:
        score += 15

    # 3. 선호 근무 환경 (예: 제조, 연구, 서비스)
    if student["work_environment"] == school["work_environment"]:
        score += 12

    # 4. 취업 목표 수준 (대기업, 공기업 등)
    if student["employment_goal"] == school["employment_support_level"]:
        score += 10

    # 5. 선호 산업 분야
    if student["industry"] == school["industry"]:
        score += 10

    # 6. 진학 희망 여부
    if student["college_preference"] == school["college_track"]:
        score += 8

    # 7. 자격증 취득 의지
    if student["certificate_will"] == "높음":
        score += school["certification_rate"] * 0.08

    # 8. 학습 성향
    if student["learning_style"] == school["learning_style"]:
        score += 5

    # 9. 성격 특성
    if student["personality"] == school["preferred_personality"]:
        score += 4

    # 10. 경제적 조건 (거리, 기숙사, 비용)
    if school["distance_km"] <= student["max_distance"]:
        score += 3

    if student["dormitory_needed"] == school["dormitory"]:
        score += 3

    # 11. 보호자 의견
    if student["parent_preference"] == school["region"]:
        score += 2

    # 12. 장기 목표
    if student["long_term_goal"] == school["career_path"]:
        score += 8

    # 추가 학교 성과 지표 반영
    performance_score = (
        school["employment_rate"] * 0.25 +
        school["retention_rate"] * 0.20 +
        school["college_rate"] * 0.10 +
        school["certification_rate"] * 0.20 +
        school["major_match_rate"] * 0.25
    ) / 100

    score += performance_score * 20

    return round(score, 2)
