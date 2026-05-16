def calculate_score(student, school):
    """
    학생 조건과 50개 학교 한국어 데이터를 기반으로 적합도 점수 계산
    중요도 높은 요소를 상위 가중치로 반영
    """

    score = 0

    # 1. 내신 성적 (가장 중요) - 백분위는 숫자가 낮을수록 고득점
    if student["내신성적"] <= school["합격커트라인"]:
        score += 20

    # 2. 희망 지역
    if student["희망지역"] == school["지역"]:
        score += 15

    # 3. 선호 근무 환경 (예: 제조, 연구, 서비스)
    if student["선호근무환경"] == school["근무환경"]:
        score += 12

    # 4. 취업 목표 수준 (대기업, 공기업 등)
    if student["취업목표수준"] == school["취업지원수준"]:
        score += 10

    # 5. 선호 산업 분야
    if student["선호산업분야"] == school["산업분야"]:
        score += 10

    # 6. 진학 희망 여부
    if student["진학희망여부"] == school["진학경로"]:
        score += 8

    # 7. 자격증 취득 의지 (의지가 높다면 해당 학교의 실제 취득률을 비례해서 반영)
    if student["자격증취득의지"] == "높음":
        score += school["자격증취득률"] * 0.08

    # 8. 학습 성향
    if student["학습성향"] == school["학습성향"]:
        score += 5

    # 9. 성격 특성
    if student["성격특성"] == school["권장성격"]:
        score += 4

    # 10. 경제적 조건 (거리, 기숙사)
    if school["통학거리_km"] <= student["최대통학거리"]:
        score += 3

    if student["기숙사필요여부"] == school["기숙사여부"]:
        score += 3

    # 11. 보호자 의견 (예: 보호자가 바라는 지역 연동)
    if student["부모님희망지역"] == school["지역"]:
        score += 2

    # 12. 장기 목표 (진로 방향)
    if student["장기목표"] == school["진로방향"]:
        score += 8

    # 추가 학교 성과 지표 반영 (학교의 객관적 공시 지표 반영률 산출)
    performance_score = (
        school["취업률"] * 0.25 +
        school["유지취업률"] * 0.20 +
        school["진학률"] * 0.10 +
        school["자격증취득률"] * 0.20 +
        school["전공일치율"] * 0.25
    ) / 100

    score += performance_score * 20

    return round(score, 2)
