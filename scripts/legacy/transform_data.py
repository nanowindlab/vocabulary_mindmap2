import json

# 14개 핵심 루트 정의
ROOTS = {
    "1. 사람": ["person", "family", "friend", "feeling", "emotion", "personality", "job", "body", "appearance"],
    "2. 식생활": ["food", "eat", "drink", "restaurant", "cafe", "cook", "fruit", "vegetable", "meat"],
    "3. 주거와 일상": ["home", "house", "room", "furniture", "appliance", "cleaning", "daily", "life"],
    "4. 쇼핑": ["shop", "store", "buy", "price", "money", "pay", "market", "clothing", "item"],
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

def get_root(e_word):
    if not e_word: return "14. 추상적 기초"
    e_word = e_word.lower()
    for root, keywords in ROOTS.items():
        if any(kw in e_word for kw in keywords):
            return root
    return "14. 추상적 기초"

# 원본 데이터 로드
with open('05_source/extracted_corpus/snapshot_20260309/Lemma_Meanings.jsonl', 'r') as f:
    meanings = [json.loads(line) for line in f]

# 런타임 JSON 생성
payload = []
for m in meanings:
    root = get_root(m.get('e_word', ''))
    payload.append({
        "id": m.get('meaning_id'),
        "word": m.get('lemma'),
        "pos": m.get('pos_ko'),
        "roman": m.get('phonetic_romanization'),
        "def_kr": m.get('meaning_kr'),
        "def_en": m.get('e_word'),
        "hierarchy": {
            "root": root,
            "scene": "General", # T1.3 단계에서는 우선 General로 통일 후 정교화
            "category": m.get('pos_ko'),
            "path_ko": f"{root} > General > {m.get('pos_ko')}"
        },
        "stats": {
            "freq": m.get('frequency', 0),
            "rank": m.get('frequency_rank', 0)
        }
    })

with open('09_app_v2/public/data/APP_READY_CORE_TREE_V1.json', 'w') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Total processed: {len(payload)}")
