import json
import os
import re
from collections import defaultdict

# Paths
SOURCE_DIR = "/Users/nanowind/Library/CloudStorage/SynologyDrive-Work/Project/AI/antigravity/vocabulary_mindmap2/05_source"
SNAPSHOT_DIR = os.path.join(SOURCE_DIR, "extracted_corpus/snapshot_20260309")
DICT_PATH = os.path.join(SOURCE_DIR, "raw_dictionary/한국어 어휘사전(영어판)_사전.json")
OUTPUT_DIR = "/Users/nanowind/Library/CloudStorage/SynologyDrive-Work/Project/AI/antigravity/vocabulary_mindmap2/09_app/public/data"

# Classification Rules (System -> Root -> Keywords/POS)
IA_V4 = {
    "구조와 기초": {
        "수량과 단위": {"pos": ["수사", "의존명사"], "keywords": ["개", "명", "번", "원", "살", "가지", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉", "열", "백", "천", "만", "억", "조", "하나", "둘", "셋", "넷"]},
        "시간과 흐름": {"keywords": ["시", "분", "초", "날", "월", "년", "어제", "오늘", "내일", "모레", "글피", "전", "후", "동안", "때", "아침", "점심", "저녁", "밤", "새벽", "오전", "오후", "봄", "여름", "가을", "겨울", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]},
        "논리와 연결": {"pos": ["부사", "접속사"], "keywords": ["그리고", "하지만", "그래서", "그러나", "그런데", "그렇지만", "따라서", "또는", "혹은", "및", "더구나", "게다가"]},
        "지시와 질문": {"pos": ["대명사"], "keywords": ["이", "그", "저", "무엇", "어디", "누구", "언제", "어떻게", "왜", "어느", "어떤", "무슨", "여기에", "거기에", "저기에", "나", "너", "우리", "그들", "저희"]}
    },
    "마음과 표현": {
        "내면과 감정": {"keywords": ["기쁘다", "슬프다", "화나다", "즐겁다", "행복하다", "괴롭다", "무섭다", "두렵다", "그립다", "보고 싶다", "느끼다", "생각하다", "걱정", "고민", "감동", "사랑", "미움", "싫다", "좋다", "우울", "긴장"]},
        "성격과 태도": {"keywords": ["착하다", "성실하다", "게으르다", "친절하다", "용감하다", "부드럽다", "강하다", "약하다", "겸손하다", "솔직하다", "고집", "성격", "태도", "습관", "노력", "포기", "결심"]},
        "감각과 묘사": {"keywords": ["빨갛다", "노랗다", "파랗다", "하얗다", "까맣다", "크다", "작다", "길다", "짧다", "무겁다", "가볍다", "뜨겁다", "차갑다", "시원하다", "따뜻하다", "달다", "짜다", "맵다", "쓰다", "시다", "밝다", "어둡다", "조용하다", "시끄럽다"]},
        "의견과 가치": {"keywords": ["중요하다", "필요하다", "맞다", "틀리다", "쉽다", "어렵다", "아름답다", "멋지다", "훌륭하다", "나쁘다", "유명하다", "특별하다", "비싸다", "싸다", "가치", "의미", "생각", "의견"]}
    },
    "상황과 장소": {
        "사람과 관계": {"keywords": ["어머니", "아버지", "부모", "동생", "친구", "동료", "선생님", "할아버지", "할머니", "가족", "친척", "결혼", "아이", "어른", "남자", "여자", "분", "사람", "인간"]},
        "식생활": {"keywords": ["밥", "물", "고기", "채소", "과일", "음식", "요리", "식당", "카페", "커피", "차", "술", "맛", "배고프다", "부르다", "먹다", "마시다", "끓이다", "굽다", "볶다"]},
        "주거와 일상": {"keywords": ["집", "방", "거실", "주방", "침대", "책상", "의자", "가구", "청소", "빨래", "자다", "일어나다", "씻다", "살다", "생활", "이사", "아파트", "건물"]},
        "쇼핑": {"keywords": ["가게", "상점", "시장", "백화점", "마트", "물건", "돈", "가격", "사다", "팔다", "고르다", "환불", "영수증", "계산", "카드", "현금"]},
        "교통": {"keywords": ["차", "버스", "지하철", "택시", "기차", "비행기", "길", "도로", "역", "정거장", "타다", "내리다", "걷다", "뛰다", "운전", "이동", "신호등", "횡단보도"]},
        "학교와 공부": {"keywords": ["학교", "교실", "수업", "공부", "시험", "숙제", "배우다", "가르치다", "학생", "대학교", "전공", "책", "공책", "연필", "지우개", "도서관", "성적"]},
        "직장과 업무": {"keywords": ["회사", "사무실", "일", "업무", "직원", "사장", "회의", "보고", "전화", "취직", "월급", "출근", "퇴근", "비즈니스", "동료"]},
        "여가와 취미": {"keywords": ["운동", "축구", "야구", "수영", "등산", "영화", "음악", "노래", "춤", "그림", "게임", "여행", "사진", "악기", "공연", "취미", "즐기다"]},
        "여행": {"keywords": ["여행", "관광", "지도", "숙소", "호텔", "공항", "여권", "짐", "가방", "출국", "입국", "방문", "구경", "체험"]},
        "보건과 의료": {"keywords": ["몸", "건강", "아프다", "병원", "의사", "간호사", "약", "약국", "감기", "기침", "열", "머리", "다리", "팔", "치료", "수술", "증상"]},
        "날씨와 자연": {"keywords": ["날씨", "해", "비", "눈", "바람", "구름", "하늘", "바다", "산", "강", "나무", "꽃", "숲", "봄", "여름", "가을", "겨울", "춥다", "덥다", "흐리다", "맑다"]},
        "공공 서비스": {"keywords": ["은행", "경찰서", "소방서", "우체국", "시청", "동사무소", "행정", "민원", "세금", "보험", "법", "공공"]},
        "문화와 사회": {"keywords": ["문화", "사회", "전통", "명절", "뉴스", "정치", "경제", "역사", "종교", "축제", "예술", "사건", "문제"]},
        "상황 지시/기타": {"keywords": ["색", "모양", "크기", "무늬", "종류", "부분", "전체", "위치", "방향", "위", "아래", "앞", "뒤", "왼쪽", "오른쪽", "옆", "가운데"]}
    }
}

def load_jsonl(path):
    data = []
    if not os.path.exists(path):
        return data
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data

def main():
    print("Loading data...")
    # Load Dictionary
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        dict_data = json.load(f)
    
    dict_map = {}
    for entry in dict_data:
        headword = entry["entry"]["headword_ko"]
        if headword not in dict_map:
            dict_map[headword] = entry
    
    # Load Stats
    stats_data = load_jsonl(os.path.join(SNAPSHOT_DIR, "Z_ALL_Lemma_Stats.jsonl"))
    stats_map = {s["lemma"]: s for s in stats_data}
    
    # Load AI Examples
    ai_examples_data = load_jsonl(os.path.join(SNAPSHOT_DIR, "Lemma_Examples.jsonl"))
    ai_examples_map = defaultdict(list)
    for ex in ai_examples_data:
        ai_examples_map[ex["meaning_id"]].append({
            "sentence": ex["example_sentence"],
            "type": ex["example_type"]
        })
    
    # Stream TOPIK Examples from Word_Occurrences.jsonl
    topik_examples_map = defaultdict(set)
    print("Streaming Word_Occurrences.jsonl for TOPIK examples...")
    occ_path = os.path.join(SNAPSHOT_DIR, "Word_Occurrences.jsonl")
    with open(occ_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i % 100000 == 0:
                print(f"Processed {i} occurrences...")
            occ = json.loads(line)
            lemma = occ["lemma"]
            sentence = occ["source_sentence"]
            if lemma and sentence and len(topik_examples_map[lemma]) < 5:
                # Clean sentence (limit length if too long)
                if len(sentence) < 200:
                    topik_examples_map[lemma].add(sentence)
            if i > 2000000: # Limit for efficiency in this script
                break

    # Load Meanings (Target 8,139 words)
    meanings_data = load_jsonl(os.path.join(SNAPSHOT_DIR, "Lemma_Meanings.jsonl"))
    
    schema_complete = {}
    mapping = {
        "구조와 기초": {root: [] for root in IA_V4["구조와 기초"]},
        "마음과 표현": {root: [] for root in IA_V4["마음과 표현"]},
        "상황과 장소": {root: [] for root in IA_V4["상황과 장소"]},
        "Uncertain": []
    }
    
    stats_counters = {
        "구조와 기초": 0,
        "마음과 표현": 0,
        "상황과 장소": 0,
        "Uncertain": 0
    }

    print(f"Processing {len(meanings_data)} words...")
    for item in meanings_data:
        m_id = item["meaning_id"]
        lemma = item["lemma"]
        pos_ko = item["pos_ko"]
        meaning_kr = item["meaning_kr"]
        
        # Classification
        assigned_system = None
        assigned_root = None
        
        # Priority 1: Structure & Basics
        for root, criteria in IA_V4["구조와 기초"].items():
            if ("pos" in criteria and pos_ko in criteria["pos"]) or \
               (any(kw in lemma or kw in meaning_kr for kw in criteria["keywords"])):
                assigned_system = "구조와 기초"
                assigned_root = root
                break
        
        # Priority 2: Heart & Expression
        if not assigned_system:
            for root, criteria in IA_V4["마음과 표현"].items():
                if any(kw in lemma or kw in meaning_kr for kw in criteria["keywords"]):
                    assigned_system = "마음과 표현"
                    assigned_root = root
                    break
        
        # Priority 3: Situations & Places
        if not assigned_system:
            for root, criteria in IA_V4["상황과 장소"].items():
                if any(kw in lemma or kw in meaning_kr for kw in criteria["keywords"]):
                    assigned_system = "상황과 장소"
                    assigned_root = root
                    break
        
        if assigned_system:
            mapping[assigned_system][assigned_root].append(m_id)
            stats_counters[assigned_system] += 1
        else:
            mapping["Uncertain"].append(m_id)
            stats_counters["Uncertain"] += 1

        # Hydration
        dict_entry = dict_map.get(lemma, {})
        stats_entry = stats_map.get(lemma, {})
        
        # Collect sentences
        attested = []
        # Add TOPIK (up to 3)
        topik_list = list(topik_examples_map.get(lemma, []))
        for s in topik_list[:3]:
            attested.append({"sentence": s, "type": "TOPIK"})
        
        # Add AI (up to 3)
        ai_list = ai_examples_map.get(m_id, [])
        for ex in ai_list[:3]:
            attested.append(ex)
            
        # Limit to 6
        attested = attested[:6]
        
        # English meaning from dict or item
        m_en = item.get("e_word")
        if not m_en and dict_entry:
            senses = dict_entry.get("senses", [])
            if senses:
                trans = senses[0].get("translations", [])
                if trans:
                    m_en = trans[0].get("equivalent")

        schema_complete[m_id] = {
            "lemma": lemma,
            "pos": pos_ko,
            "meaning_kr": meaning_kr,
            "meaning_en": m_en,
            "phonetic_romanization": item.get("phonetic_romanization"),
            "grade": dict_entry.get("entry", {}).get("grade", "N/A"),
            "attested_sentences": attested,
            "related_vocab": dict_entry.get("entry", {}).get("related_vocab", []),
            "stats": {
                "total_frequency": stats_entry.get("total_frequency", 0)
            }
        }

    # Save Outputs
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "APP_READY_MAPPING_V1.json"), "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, "APP_READY_SCHEMA_COMPLETE_V1.json"), "w", encoding="utf-8") as f:
        json.dump(schema_complete, f, ensure_ascii=False, indent=2)

    # Print Report
    total = len(meanings_data)
    success = total - stats_counters["Uncertain"]
    success_rate = (success / total) * 100 if total > 0 else 0
    
    print("\n" + "="*50)
    print("CLASSIFICATION REPORT")
    print("="*50)
    print(f"Total words: {total}")
    print(f"Successfully classified: {success} ({success_rate:.2f}%)")
    print("-" * 30)
    for system, count in stats_counters.items():
        print(f"{system}: {count} ({count/total*100:.2f}%)")
    
    print("\nUncertain Examples (first 10):")
    for m_id in mapping["Uncertain"][:10]:
        word = schema_complete[m_id]["lemma"]
        meaning = schema_complete[m_id]["meaning_kr"]
        print(f"- {word}: {meaning}")
    print("="*50)

if __name__ == "__main__":
    main()
