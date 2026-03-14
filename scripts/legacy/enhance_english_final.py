import json

# 1. 인벤토리 및 원본 데이터 로드
with open('09_app_v2/public/data/ENGLISH_MAPPING_INVENTORY_V1.json', 'r') as f:
    inventory = json.load(f)

# TOPIK 등급 매핑 사전 (초/중/고)
grade_map = inventory.get('topik_levels', {"초": "Beginner", "중": "Intermediate", "고": "Advanced"})

# 14대 루트 영문 매핑 사전
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

# 기존 런타임 트리 로드 (이전 작업본)
with open('09_app_v2/public/data/APP_READY_CORE_TREE_V1.json', 'r') as f:
    core_tree = json.load(f)

# 원본 Lemma_Meanings 로드 (상세 등급 정보 등 확인용)
with open('05_source/extracted_corpus/snapshot_20260309/Lemma_Meanings.jsonl', 'r') as f:
    raw_meanings = {json.loads(line)['meaning_id']: json.loads(line) for line in f}

# 보강 작업
count = 0
for item in core_tree:
    m_id = item.get('id')
    raw_m = raw_meanings.get(m_id, {})
    
    # 1. 등급 보강 (stats.grade_en)
    # raw_dictionary 등에서 grade(초/중/고) 정보를 가져와 영문화
    # 여기서는 m_id에서 정보를 유추하거나 raw_m의 grade 정보를 활용
    # raw_m에 'grade' 필드가 없을 경우를 대비하여 기본값 설정 로직 추가
    grade_ko = raw_m.get('grade') or "초" # 기본값 초급
    item['stats']['grade'] = grade_ko
    item['stats']['grade_en'] = grade_map.get(grade_ko, "Beginner")
    
    # 2. 루트 영문 보강 (hierarchy.root_en)
    root_label_ko = item.get('hierarchy', {}).get('root_label', '')
    item['hierarchy']['root_en'] = root_en_map.get(root_label_ko, "Basics")

    # 3. 영문 정의 보강 (def_en)
    meaning_en = raw_m.get('meaning_en')
    if meaning_en and len(meaning_en) > len(item.get('def_en', '')):
        item['def_en'] = meaning_en

    count += 1

# 결과 저장
with open('09_app_v2/public/data/APP_READY_CORE_TREE_V1.json', 'w') as f:
    json.dump(core_tree, f, ensure_ascii=False, indent=2)

print(f"Final Enhancement Done: {count} records updated with grade_en and root_en.")
