# ==========================================
# 0. 메뉴 데이터 직접 작성
# ==========================================
def load_menu_db():
    """코드에 직접 작성한 메뉴 목록을 반환"""
    return [
        {"id": 1, "name": "제육볶음", "category": "한식", "ingredients": ["돼지고기", "양파", "대파", "고추장"], "spicy": 2},
        {"id": 2, "name": "등심돈까스", "category": "양식", "ingredients": ["돼지고기", "밀가루", "달걀", "빵가루"], "spicy": 0},
        {"id": 3, "name": "비빔밥", "category": "한식", "ingredients": ["밥", "소고기", "시금치", "당근", "숙주"], "spicy": 1},
        {"id": 4, "name": "된장찌개", "category": "한식", "ingredients": ["된장", "두부", "애호박", "양파", "조개"], "spicy": 0},
        {"id": 5, "name": '김치찌개', "category": '한식', "ingredients": ['돼지고기', '김치', '두부', '양파'], "spicy": 2},
        {"id": 6, "name": '순두부찌개', "category": '한식', "ingredients": ['순두부', '달걀', '애호박', '조개'], "spicy": 2},
        {"id": 7, "name": '불고기', "category": '한식', "ingredients": ['소고기', '양파', '대파', '버섯'], "spicy": 0},
        {"id": 8, "name": '닭갈비', "category": '한식', "ingredients": ['닭고기', '양배추', '고구마', '고추장'], "spicy": 2},
        {"id": 9, "name": '삼겹살', "category": '한식', "ingredients": ['돼지고기', '상추', '마늘'], "spicy": 0},
        {"id": 10, "name": '갈비탕', "category": '한식', "ingredients": ['소고기', '무', '대파', '당면'], "spicy": 0},
        {"id": 11, "name": '설렁탕', "category": '한식', "ingredients": ['소고기', '대파', '소면'], "spicy": 0},
        {"id": 12, "name": '김밥', "category": '분식', "ingredients": ['밥', '김', '달걀', '당근', '단무지'], "spicy": 0},
        {"id": 13, "name": '떡볶이', "category": '분식', "ingredients": ['떡', '어묵', '대파', '고추장'], "spicy": 2},
        {"id": 14, "name": '라면', "category": '분식', "ingredients": ['면', '달걀', '대파'], "spicy": 2},
        {"id": 15, "name": '잔치국수', "category": '한식', "ingredients": ['소면', '달걀', '애호박', '김'], "spicy": 0},
        {"id": 16, "name": '냉면', "category": '한식', "ingredients": ['메밀면', '오이', '달걀', '무'], "spicy": 0},
        {"id": 17, "name": '짜장면', "category": '중식', "ingredients": ['면', '돼지고기', '양파', '춘장'], "spicy": 0},
        {"id": 18, "name": '짬뽕', "category": '중식', "ingredients": ['면', '오징어', '홍합', '양배추'], "spicy": 3},
        {"id": 19, "name": '볶음밥', "category": '중식', "ingredients": ['밥', '달걀', '당근', '대파'], "spicy": 0},
        {"id": 20, "name": '마파두부', "category": '중식', "ingredients": ['두부', '돼지고기', '대파', '두반장'], "spicy": 2},
        {"id": 21, "name": '초밥', "category": '일식', "ingredients": ['밥', '연어', '새우', '김'], "spicy": 0},
        {"id": 22, "name": '우동', "category": '일식', "ingredients": ['우동면', '어묵', '대파'], "spicy": 0},
        {"id": 23, "name": '카레라이스', "category": '일식', "ingredients": ['밥', '돼지고기', '감자', '당근', '카레'], "spicy": 1},
        {"id": 24, "name": '오므라이스', "category": '양식', "ingredients": ['밥', '달걀', '양파', '토마토'], "spicy": 0},
        {"id": 25, "name": '토마토파스타', "category": '양식', "ingredients": ['파스타면', '토마토', '마늘', '양파'], "spicy": 0},
        {"id": 26, "name": '크림파스타', "category": '양식', "ingredients": ['파스타면', '우유', '베이컨', '버섯'], "spicy": 0},
        {"id": 27, "name": '피자', "category": '양식', "ingredients": ['밀가루', '치즈', '토마토', '양파'], "spicy": 0},
        {"id": 28, "name": '햄버거', "category": '양식', "ingredients": ['빵', '소고기', '양상추', '토마토', '치즈'], "spicy": 0},
        {"id": 29, "name": '쌀국수', "category": '베트남식', "ingredients": ['쌀국수면', '소고기', '숙주', '양파'], "spicy": 0},
        {"id": 30, "name": '팟타이', "category": '태국식', "ingredients": ['쌀국수면', '새우', '달걀', '숙주', '땅콩'], "spicy": 1},
    ]


# ==========================================
# 공통 패턴: Blacklist 포함 여부 검사
# ==========================================
def blacklist(item_ingredients, blacklist_set):
    """[패턴] 특정 메뉴 재료에 기피 재료가 1개라도 포함되어 있는지 검사"""
    return bool(set(item_ingredients) & blacklist_set)


# ==========================================
# C1. 취향 수집기
# ==========================================
def collect(user_inputs):
    """참여자 입력값 정규화 (비선호 식재료 세트 + 선호 메뉴 득표 집계)"""
    group_dislikes = set()
    vote_counts = {}

    for user in user_inputs:
        # 비선호 식재료 최대 3개 수집 및 정제
        dislikes = user.get("dislikes", [])[:3]
        for item in dislikes:
            clean_item = item.strip()
            if clean_item:
                group_dislikes.add(clean_item)

        # 선호 메뉴 최대 2개 수집 및 득표수 누적
        likes = user.get("likes", [])[:2]
        for menu in likes:
            clean_menu = menu.strip()
            if clean_menu:
                vote_counts[clean_menu] = vote_counts.get(clean_menu, 0) + 1

    return {
        "blacklist": group_dislikes,
        "votes": vote_counts
    }


# ==========================================
# C2. 메뉴 필터기
# ==========================================
def filter_menu(group_profile, menu_db):
    """비선호 재료 배제 및 후보 0개 고갈 시 차선책 3종 복구"""
    target_blacklist = group_profile["blacklist"]
    safe_candidates = []

    # 1차 필터링: blacklist 함수를 활용해 안전 후보군 선별
    for menu in menu_db:
        if not blacklist(menu["ingredients"], target_blacklist):
            safe_candidates.append(menu)

    # 예외 처리: 남은 메뉴가 0개일 때 불호 중복도 최저 3종 복구
    is_fallback = False
    if not safe_candidates:
        is_fallback = True
        scored_menus = []
        for menu in menu_db:
            overlap_count = len(set(menu["ingredients"]) & target_blacklist)
            scored_menus.append((overlap_count, menu))
        
        scored_menus.sort(key=lambda x: x[0])
        safe_candidates = [m[1] for m in scored_menus[:3]]

    return safe_candidates, is_fallback


# ==========================================
# C3. 최종 추천기
# ==========================================
def final_menu(candidates, group_profile, is_fallback=False):
    """안전 후보군 중 최다 득표 메뉴 1개 선정 및 추천 사유 생성"""
    votes = group_profile["votes"]

    # 선호 득표수 기준 내림차순 정렬
    ranked = sorted(candidates, key=lambda m: votes.get(m["name"], 0), reverse=True)
    top_menu = ranked[0]
    top_votes = votes.get(top_menu["name"], 0)

    # 추천 사유 분기
    if is_fallback:
        reason = "전원 비선호 조건을 100% 만족하는 메뉴가 없어, 기피 재료 겹침이 가장 적은 차선책 메뉴 중 최적안으로 선정되었습니다."
    else:
        if top_votes > 0:
            reason = f"참여자 전원의 비선호 재료를 배제하였으며, 그룹 내 선호 투표 최다 득표({top_votes}표)를 얻어 선정되었습니다."
        else:
            reason = "참여자 전원의 비선호 재료가 완전히 배제된 안전 후보군 중 균형 있는 기본 메뉴로 선정되었습니다."

    return {
        "menu_name": top_menu["name"],
        "category": top_menu["category"],
        "ingredients": top_menu["ingredients"],
        "reason": reason
    }


# ==========================================
# 파이프라인 테스트 실행
# ==========================================
if __name__ == "__main__":
    # 1. 코드에 작성한 메뉴 데이터 로드
    menu_db = load_menu_db()

    # 2. 테스트 참여자 데이터 (선호 2개, 비선호 3개 이하)
    sample_users = [
        {"user": "학생A", "likes": ["제육볶음", "등심돈까스"], "dislikes": ["오이", "조개"]},
        {"user": "학생B", "likes": ["등심돈까스", "비빔밥"], "dislikes": ["땅콩", "오징어"]},
        {"user": "학생C", "likes": ["제육볶음", "된장찌개"], "dislikes": ["홍합", "숙주"]}
    ]

    # 3. 파이프라인 단계별 호출 (collect -> filter_menu -> final_menu)
    profile = collect(sample_users)
    safe_list, fallback_flag = filter_menu(profile, menu_db)
    result = final_menu(safe_list, profile, is_fallback=fallback_flag)

    # 4. 결과 출력
    print("==========================================")
    print("데이터 소스: 코드에 직접 작성한 메뉴 목록")
    print(f"추천 메뉴: {result['menu_name']} ({result['category']})")
    print("주재료:", ", ".join(result["ingredients"]))
    print("추천 사유:", result["reason"])
    print("==========================================")