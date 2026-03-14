import json

# 1. 인벤토리 로드
with open('09_app_v2/public/data/ENGLISH_MAPPING_INVENTORY_V1.json', 'r') as f:
    inventory = json.load(f)

# 2. 기존 코어 트리 로드
with open('09_app_v2/public/data/APP_READY_CORE_TREE_V1.json', 'r') as f:
    core_tree = json.load(f)

# 3. 보강 로직
grade_map = inventory.get('topik_levels', {})
meta_map = inventory.get('meta_groups', {})

for item in core_tree:
    # TOPIK 등급 영문화
    grade_ko = item.get('stats', {}).get('grade', '')
    if grade_ko in grade_map:
        item['stats']['grade_en'] = grade_map[grade_ko]
    
    # 영문 정의 품질 체크 및 보강 (현재는 e_word를 def_en으로 사용 중)
    # 만약 def_en이 너무 짧거나(2자 이하) 불분명한 경우 보강할 수 있는 구조 마련
    if not item.get('def_en') or len(item.get('def_en')) <= 2:
        # 향후 05_source의 translations 상세 데이터를 더 끌어올 수 있음
        pass

    # 루트/장면 영문 라벨 추가 (Mindmap UI 지원용)
    # 14대 루트의 영문 명칭 매핑 (임시 매핑, 추후 인벤토리에 추가 권장)
    root_en_map = {
        "사람": "People",
        "식생활": "Food & Dining",
        "주거와 일상": "Home & Life",
        "쇼핑": "Shopping",
        "교통": "Transportation",
        "학교와 공부": "School",
        "직장과 업무": "Work",
        "여가와 취미": "Hobby",
        "여행": "Travel",
        "건강": "Health",
        "날씨와 자연": "Nature",
        "공공 서비스": "Public Services",
        "문화와 사회": "Society & Culture",
        "추상적 기초": "Basics"
    }
    root_label_ko = item.get('hierarchy', {}).get('root_label', '')
    if root_label_ko in root_en_map:
        item['hierarchy']['root_en'] = root_en_map[root_label_ko]

# 4. 결과 저장
with open('09_app_v2/public/data/APP_READY_CORE_TREE_V1.json', 'w') as f:
    json.dump(core_tree, f, ensure_ascii=False, indent=2)

print(f"Enhanced {len(core_tree)} records with English mapping inventory.")
