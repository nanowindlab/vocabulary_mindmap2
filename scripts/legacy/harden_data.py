import json

# 14개 핵심 루트 명칭 동기화 (워크보드/리서치 기준)
ROOT_LABELS = {
    "1. 사람": "사람",
    "2. 식생활": "식생활",
    "3. 주거와 일상": "주거와 일상",
    "4. 쇼핑": "쇼핑",
    "5. 교통": "교통",
    "6. 학교와 공부": "학교와 공부",
    "7. 직장과 업무": "직장과 업무",
    "8. 여가와 취미": "여가와 취미",
    "9. 여행": "여행",
    "10. 건강": "건강",
    "11. 날씨와 자연": "날씨와 자연",
    "12. 공공 서비스": "공공 서비스",
    "13. 문화와 사회": "문화와 사회",
    "14. 추상적 기초": "추상적 기초"
}

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
    if not e_word: return "14. 추상적 기초", ROOT_LABELS["14. 추상적 기초"]
    e_word = e_word.lower()
    for root_id, keywords in ROOTS.items():
        if any(kw in e_word for kw in keywords):
            return root_id, ROOT_LABELS[root_id]
    return "14. 추상적 기초", ROOT_LABELS["14. 추상적 기초"]

# 원본 및 누락 보강용 데이터 로드
with open('05_source/extracted_corpus/snapshot_20260309/Lemma_Meanings.jsonl', 'r') as f:
    meanings = [json.loads(line) for line in f]

payload = []
for m in meanings:
    root_id, root_label = get_root_info(m.get('e_word', ''))
    
    # 발음 필드 보강 (누락 시 기본값 또는 'N/A' 방지 로직)
    roman = m.get('phonetic_romanization')
    if not roman or roman.strip() == "":
        roman = f"({m.get('lemma')})" # 최소한의 힌트 제공 또는 추후 로마자 변환기 연동 대비
        
    payload.append({
        "id": m.get('meaning_id'),
        "word": m.get('lemma'),
        "pos": m.get('pos_ko', '기타'),
        "roman": roman,
        "def_kr": m.get('meaning_kr'),
        "def_en": m.get('e_word'),
        "hierarchy": {
            "root_id": root_id,
            "root_label": root_label,
            "scene": "일반",
            "category": m.get('pos_ko', '기타'),
            "path_ko": f"{root_label} > 일반 > {m.get('pos_ko', '기타')}"
        },
        "stats": {
            "freq": m.get('frequency', 0),
            "rank": m.get('frequency_rank', 0)
        }
    })

# 최종 파일 배포
output_path = '09_app_v2/public/data/APP_READY_CORE_TREE_V1.json'
with open(output_path, 'w') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Hardened data saved to {output_path}. Total: {len(payload)}")
