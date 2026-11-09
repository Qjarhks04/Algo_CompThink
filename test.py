# AI 보조 : 30종 더미데이터 생성 보조
def load_menu_db():
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

# 공통 패턴: Blacklist 포함 여부 검사
def blacklist(item_ingredients, blacklist_set):
    """[패턴] 특정 메뉴 재료에 기피 재료가 1개라도 포함되어 있는지 검사"""
    return bool(set(item_ingredients) & blacklist_set)

# C1. 취향 수집기
def collect(user_inputs, menu_db):
    """참여자의 기피 재료를 모으고 유효한 선호 메뉴의 투표를 집계"""
    group_dislikes = set()
    vote_counts = {}
    group_max_spicy = 3

    valid_menu_names = {menu["name"] for menu in menu_db}

    for user in user_inputs:
        # 양쪽 공백을 제거하고 빈 입력은 제외
        dislikes = [
            item.strip()
            for item in user.get("dislikes", [])
            if item.strip()
        ]

        likes = [
            menu.strip()
            for menu in user.get("likes", [])
            if menu.strip()
        ]

        # 빈 입력을 제외한 뒤 개수 확인
        if len(dislikes) > 3:
            raise ValueError(
                "기피 재료는 한 사람당 최대 3개까지 입력할 수 있습니다."
            )

        if len(likes) > 2:
            raise ValueError(
                "선호 메뉴는 한 사람당 최대 2개까지 입력할 수 있습니다."
            )

        # 기피 재료 수집
        for item in dislikes:
            group_dislikes.add(item)

        # 선호 메뉴 투표 집계
        seen_likes = set()

        for menu in likes:
            if menu not in valid_menu_names:
                print(
                    f"'{menu}'은(는) 메뉴 DB에 없어 "
                    "투표에서 제외합니다."
                )
                continue

            # 한 사람이 같은 메뉴를 여러 번 선택해도 1표만 집계
            if menu not in seen_likes:
                seen_likes.add(menu)
                vote_counts[menu] = vote_counts.get(menu, 0) + 1

        # 입력하지 않으면 3단계까지 가능하다고 가정
        max_spicy = user.get("max_spicy", 3)

        if type(max_spicy) is not int or not 0 <= max_spicy <= 3:
            raise ValueError(
                "최대 맵기는 0부터 3까지의 정수로 입력해야 합니다."
            )

        # 참여자 중 가장 낮은 최대 맵기를 그룹 기준으로 사용
        group_max_spicy = min(group_max_spicy, max_spicy)

    return {
        "blacklist": group_dislikes,
        "votes": vote_counts,
        "max_spicy": group_max_spicy
    }

def filter_menu(group_profile, menu_db):
    """기피 재료와 맵기를 기준으로 후보 메뉴를 선택"""

    target_blacklist = group_profile["blacklist"]
    max_spicy = group_profile["max_spicy"]
    safe_candidates = []

    # 1차 필터링: 기피 재료와 최대 맵기를 모두 확인
    for menu in menu_db:
        has_disliked_ingredient = blacklist(
            menu["ingredients"],
            target_blacklist
        )

        if not has_disliked_ingredient and menu["spicy"] <= max_spicy:
            safe_candidates.append(menu)

    # 후보가 없으면 최대 맵기는 유지하고,
    # 기피 재료가 적게 겹치는 메뉴를 차선책으로 선택
    is_fallback = False

    if not safe_candidates:
        is_fallback = True
        scored_menus = []

        for menu in menu_db:
            # 최대 맵기를 넘는 메뉴는 차선책에서도 제외
            if menu["spicy"] <= max_spicy:
                overlap_count = len(
                    set(menu["ingredients"]) & target_blacklist
                )
                scored_menus.append((overlap_count, menu))

        scored_menus.sort(key=lambda item: item[0])

        # 기피 재료가 적게 겹치는 메뉴 최대 3개
        safe_candidates = [
            item[1] for item in scored_menus[:3]
        ]

    return safe_candidates, is_fallback

# ==========================================
# C3. 최종 추천기
# ==========================================
def select_menu(candidates, group_profile, is_fallback=False):
    """안전 후보군 중 최다 득표 메뉴 1개 선정 및 추천 사유 생성"""
    if not candidates:
      return {
          "menu_name": None,
          "category": None,
          "ingredients": [],
          "spicy": None,
          "reason": "설정한 최대 맵기 조건에 맞는 메뉴가 없습니다."
      }

    votes = group_profile["votes"]

    # 선호 득표수 기준 내림차순 정렬
    ranked = sorted(candidates, key=lambda m: votes.get(m["name"], 0), reverse=True)
    top_menu = ranked[0]
    top_votes = votes.get(top_menu["name"], 0)

    # 추천 사유 분기
    if is_fallback:
        overlap = sorted(
            set(top_menu["ingredients"]) & group_profile["blacklist"]
        )

        if top_votes > 0:
            reason = (
                "기피 재료가 없는 메뉴가 없어 기피 재료가 적게 겹치는 "
                "차선책 후보 중 선호 투표를 기준으로 선정되었습니다. "
                f"선택한 메뉴에 포함된 기피 재료: {', '.join(overlap)}"
            )
        else:
            reason = (
                "기피 재료가 없는 메뉴가 없어 기피 재료가 적게 겹치는 "
                "차선책 후보를 선정했습니다. 선호 투표를 받은 후보가 없어 "
                "후보 목록의 첫 번째 메뉴를 선택했습니다. "
                f"선택한 메뉴에 포함된 기피 재료: {', '.join(overlap)}"
            )

    else:
        if top_votes > 0:
            reason = (
                "선정된 메뉴의 데이터에 기피 재료가 포함되지 않았으며, "
                f"남은 후보 중 선호 투표 최다 득표({top_votes}표)로 선정되었습니다."
            )
        else:
            reason = (
                "기피 재료가 없는 후보 중 선호 투표를 받은 메뉴가 없어, "
                "목록의 첫 번째 메뉴가 선정되었습니다."
            )

    return {
      "menu_name": top_menu["name"],
      "category": top_menu["category"],
      "ingredients": top_menu["ingredients"],
      "spicy": top_menu["spicy"],
      "reason": reason
    }

# 메뉴 30종 불러오기
menu_db = load_menu_db()


def run_test(test_name, users):
    """참여자 데이터를 받아 추천 과정을 실행하고 결과를 출력"""

    profile = collect(users, menu_db)
    candidates, is_fallback = filter_menu(profile, menu_db)
    result = select_menu(candidates, profile, is_fallback)

    print("==========================================")
    print(f"테스트: {test_name}")
    print(f"참여자 수: {len(users)}명")
    print("기피 재료:", ", ".join(sorted(profile["blacklist"])) or "없음")
    print("선호 투표:", profile["votes"])
    print("그룹 최대 맵기:", profile["max_spicy"])
    print("차선책 사용:", "예" if is_fallback else "아니요")
    print("후보 메뉴:", ", ".join(menu["name"] for menu in candidates) or "없음")

    if result["menu_name"] is not None:
      print(f"추천 메뉴: {result['menu_name']} ({result['category']})")
      print("주재료:", ", ".join(result["ingredients"]))
      print("맵기 단계:", result["spicy"])

    print("추천 사유:", result["reason"])
    print("==========================================")

normal_users = [
    {
        "user": "학생A",
        "likes": ["제육볶음", "등심돈까스"],
        "dislikes": ["오이", "조개"],
        "max_spicy": 2
    },
    {
        "user": "학생B",
        "likes": ["등심돈까스", "비빔밥"],
        "dislikes": ["땅콩", "오징어"],
        "max_spicy": 1
    },
    {
        "user": "학생C",
        "likes": ["비빔밥", "된장찌개"],
        "dislikes": ["홍합", "숙주"],
        "max_spicy": 3
    }
]

run_test("정상 추천 및 맵기 확인", normal_users)

spicy_users = [
    {
        "user": "학생A",
        "likes": ["제육볶음"],
        "dislikes": [],
        "max_spicy": 1
    },
    {
        "user": "학생B",
        "likes": ["등심돈까스"],
        "dislikes": [],
        "max_spicy": 3
    }
]

run_test("맵기 때문에 선호 메뉴 제외", spicy_users)

tie_users = [
    {
        "user": "학생A",
        "likes": ["제육볶음"],
        "dislikes": []
    },
    {
        "user": "학생B",
        "likes": ["등심돈까스"],
        "dislikes": []
    }
]

run_test("동점", tie_users)

excluded_users = [
    {
        "user": "학생A",
        "likes": ["비빔밥"],
        "dislikes": ["숙주"]
    },
    {
        "user": "학생B",
        "likes": ["비빔밥"],
        "dislikes": []
    },
    {
        "user": "학생C",
        "likes": ["등심돈까스"],
        "dislikes": []
    }
]

run_test("기피 재료로 선호 메뉴 제외", excluded_users)

# 각 메뉴의 첫 번째 재료를 기피 재료로 모음
all_dislikes = sorted({
    menu["ingredients"][0]
    for menu in menu_db
})

# 한 사람당 기피 재료가 3개를 넘지 않도록 나눔
fallback_users = [
    {
        "user": f"학생{i // 3 + 1}",
        "likes": [],
        "dislikes": all_dislikes[i:i + 3]
    }
    for i in range(0, len(all_dislikes), 3)
]

run_test("후보 고갈", fallback_users)

invalid_users = [
    {
        "user": "학생A",
        "likes": ["없는메뉴", "제육볶음"],
        "dislikes": []
    }
]

run_test("DB에 없는 메뉴 입력", invalid_users)