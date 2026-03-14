import json
import os

# 1. 인벤토리 및 원본 데이터 로드
with open('09_app_v2/public/data/ENGLISH_MAPPING_INVENTORY_V1.json', 'r') as f:
    inventory = json.load(f)

grade_map = inventory.get('topik_levels', {"초": "Beginner", "중": "Intermediate", "고": "Advanced"})
root_en_map = {
    "사람": "People", "식생활": "Food & Dining", "주거와 일상": "Home & Life",
    "쇼핑": "Shopping", "교통": "Transportation", "학교와 공부": "School",
    "직장과 업무": "Work", "여가와 취미": "Hobby", "여행": "Travel",
    "건강": "Health", "날씨와 자연": "Nature", "공공 서비스": "Public Services",
    "문화와 사회": "Society & Culture", "추상적 기초": "Basics"
}

# 05_source 원본 데이터를 기반으로 트리 재구축 (가장 확실한 방법)
with open('05_source/extracted_corpus/snapshot_20260309/Lemma_Meanings.jsonl', 'r') as f:
    meanings = [json.loads(line) for line in f]

# 14개 핵심 루트 키워드 (이전 스크립트 재활용)
ROOTS = {
    "1. 사람": ["person", "family", "friend", "feeling", "emotion", "personality", "job", "body", "appearance"],
    "2. 식생활": ["food", "eat", "drink", "restaurant", "cafe", "cook", "fruit", "vegetable", "meat"],
    "3. 주거와 일상": ["home", "house", "room", "furniture", "appliance", "cleaning", "daily", "life"],
    "4. 쇼핑": ["shop", "store", "buy", "price", "money", "pay", "market", "clothing", "item", "commerce"],
    "5. 교통": ["transport", "bus", "train", "subway", "car", "road", "direction", "move", "station"],
    "6. 학교와 공부": ["school", "study", "exam", "major", "teacher", "student", "class", "book"],
    "7. 직장과 업무": ["work", "company", "office", "business", "meeting", "salary", "coworker"],
    "8. 여가와 취미": ["hobby", "sports", "exercise", "movie", "music", "game", "art", "leisure"],
    "9. 여행": ["travel", "trip", "airport", "hotel", "sightseeing", "passport", "vacation"],
    "10. 건강": ["health", "hospital", "doctor", "medicine", "disease", "symptom", "pain"],
    "11. 날씨와 자연": ["weather", "nature", "season", "climate", "landscape", "animal", "plant"],
    "12. 공공 서비스": ["public", "bank", "post office", "police", "library", "government"],
    "13. 문화와 사회": ["society", "culture", "holiday", "media", "news", "problem", "traditional"],
    "14. 추상적 기초": ["number", "time", "color", "shape", "question", "very", "most", "basic"]
}

def get_root_info(e_word):
    if not e_word: return "14. 추상적 기초", "추상적 기초", "Basics"
    e_word = e_word.lower()
    for root_id, keywords in ROOTS.items():
        if any(kw in e_word for kw in keywords):
            label_ko = root_id.split(". ")[1]
            return root_id, label_ko, root_en_map.get(label_ko, "Basics")
    return "14. 추상적 기초", "추상적 기초", "Basics"

payload = []
for m in meanings:
    e_word = m.get('e_word', '')
    root_id, root_label, root_en = get_root_info(e_word)
    
    grade_ko = m.get('grade') or "초"
    
    payload.append({
        "id": m.get('meaning_id'),
        "word": m.get('lemma'),
        "pos": m.get('pos_ko', '기타'),
        "roman": m.get('phonetic_romanization') or f"({m.get('lemma')})",
        "def_kr": m.get('meaning_kr'),
        "def_en": m.get('meaning_en') or e_word,
        "hierarchy": {
            "root_id": root_id,
            "root_label": root_label,
            "root_en": root_en,
            "scene": "일반",
            "category": m.get('pos_ko', '기타'),
            "path_ko": f"{root_label} > 일반 > {m.get('pos_ko', '기타')}"
        },
        "stats": {
            "freq": m.get('frequency', 0),
            "rank": m.get('frequency_rank', 0),
            "grade": grade_ko,
            "grade_en": grade_map.get(grade_ko, "Beginner")
        }
    })

# 최종 배포 (09_app 경로 엄수)
output_path = '09_app/public/data/APP_READY_CORE_TREE_V1.json'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Final Hardened Data Deployed to {output_path}. Total: {len(payload)}")
