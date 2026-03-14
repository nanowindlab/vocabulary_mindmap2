import json
import os
from collections import defaultdict

# -----------------------------------------------------------------------------
# 1. 파일 경로 설정
# -----------------------------------------------------------------------------
SOURCE_DIR = "05_source/extracted_corpus/snapshot_20260309"
DICT_FILE = "05_source/raw_dictionary/한국어 어휘사전(영어판)_사전.json"
OUTPUT_DIR = "09_app/public/data"

# 입력 파일들
MEANINGS_FILE = os.path.join(SOURCE_DIR, "Lemma_Meanings.jsonl")
EXAMPLES_FILE = os.path.join(SOURCE_DIR, "Lemma_Examples.jsonl")
STATS_FILE = os.path.join(SOURCE_DIR, "Z_ALL_Lemma_Stats.jsonl")

# 출력 파일들
MAPPING_OUTPUT = os.path.join(OUTPUT_DIR, "APP_READY_MAPPING_V1.json")
SCHEMA_OUTPUT = os.path.join(OUTPUT_DIR, "APP_READY_SCHEMA_COMPLETE_V1.json")

# -----------------------------------------------------------------------------
# 2. IA V4 분류 체계 및 결정 트리 정의
# -----------------------------------------------------------------------------
IA_V4 = {
    "구조와 기초": [
        "수량과 단위", "시간과 흐름", "논리와 연결", "지시와 질문"
    ],
    "마음과 표현": [
        "내면과 감정", "성격과 태도", "감각과 묘사", "의견과 가치"
    ],
    "상황과 장소": [
        "사람과 관계", "식생활", "주거와 일상", "쇼핑", "교통", 
        "학교와 공부", "직장과 업무", "여가와 취미", "여행", 
        "보건과 의료", "날씨와 자연", "공공 서비스", "문화와 사회", "상황 지시/기타"
    ]
}

# 분류용 키워드 사전 (확장 가능)
KEYWORDS = {
    # 구조와 기초 (Priority 1)
    "수량과 단위": ["개", "명", "번", "살", "시", "분", "초", "하나", "둘", "일", "이", "수량", "숫자", "단위"],
    "시간과 흐름": ["어제", "오늘", "내일", "시간", "날짜", "자주", "가끔", "항상", "계속", "미래", "과거", "현재"],
    "논리와 연결": ["그리고", "하지만", "그래서", "그런데", "매우", "가장", "특히", "정말", "혹시", "만약"],
    "지시와 질문": ["나", "너", "우리", "이것", "저것", "누구", "어디", "언제", "무엇", "어떻게", "왜"],
    
    # 마음과 표현 (Priority 2)
    "내면과 감정": ["기쁘다", "슬프다", "화나다", "걱정", "사랑", "행복", "우울", "마음", "기분", "느끼다"],
    "성격과 태도": ["착하다", "성격", "태도", "친절", "예의", "용기", "습관", "노력", "성실"],
    "감각과 묘사": ["크다", "작다", "빨갛다", "맵다", "달다", "짜다", "차갑다", "뜨겁다", "부드럽다", "단단하다"],
    "의견과 가치": ["좋다", "나쁘다", "중요", "가치", "의견", "필요", "맞다", "틀리다", "성공", "실패"],
    
    # 상황과 장소 (Priority 3 - 14개 루트 중 대표 예시)
    "식생활": ["먹다", "마시다", "밥", "식사", "음식", "채소", "고기", "카페", "식당"],
    "교통": ["가다", "오다", "타다", "버스", "지하철", "차", "도로", "운전", "길"],
    "보건과 의료": ["아프다", "병원", "의사", "약", "치료", "감기", "건강", "몸", "얼굴"],
    "사람과 관계": ["가족", "친구", "동료", "어머니", "아버지", "형", "동생", "결혼", "만나다"]
}

def classify_word(lemma, pos, meaning_kr):
    # Priority 1: 구조와 기초 (문법적 기능 및 기초 뼈대)
    if pos in ["수사", "수관형사", "대명사", "접속부사", "조사"]:
        if any(k in meaning_kr for k in ["숫자", "수량", "차례"]): return "구조와 기초", "수량과 단위"
        if any(k in meaning_kr for k in ["시간", "날", "때"]): return "구조와 기초", "시간과 흐름"
        if any(k in meaning_kr for k in ["지시", "말하다", "질문"]): return "구조와 기초", "지시와 질문"
        return "구조와 기초", "논리와 연결"
    
    # Priority 2: 마음과 표현 (형용사 및 심리 동사)
    if pos == "형용사" or any(k in meaning_kr for k in ["기분", "느낌", "생각"]):
        if any(k in meaning_kr for k in ["기쁘", "슬프", "화", "감정"]): return "마음과 표현", "내면과 감정"
        if any(k in meaning_kr for k in ["성격", "태도", "행동"]): return "마음과 표현", "성격과 태도"
        if any(k in meaning_kr for k in ["모양", "색", "맛", "냄새"]): return "마음과 표현", "감각과 묘사"
        return "마음과 표현", "의견과 가치"
    
    # Priority 3: 상황과 장소 (물리적 장면)
    # 14개 루트에 대한 키워드 매핑 (간략화된 예시, 실제로는 더 정교하게 확장 필요)
    mapping_rules = {
        "식생활": ["음식", "밥", "먹다", "마시다", "맛", "요리"],
        "교통": ["교통", "차", "버스", "타다", "가다", "오다", "이동"],
        "보건과 의료": ["병원", "아프다", "건강", "약", "치료"],
        "학교와 공부": ["학교", "공부", "배우다", "책", "시험"],
        "직장과 업무": ["회사", "일", "직업", "회의", "업무"],
        "사람과 관계": ["사람", "가족", "친구", "관계", "동료", "이름"],
        "주거와 일상": ["집", "살다", "생활", "가구", "옷"],
        "쇼핑": ["사다", "팔다", "가게", "가격", "돈", "물건"],
        "여가와 취미": ["운동", "놀이", "영화", "취미", "음악"],
        "여행": ["여행", "관광", "비행기", "숙소"],
        "날씨와 자연": ["날씨", "비", "눈", "바람", "자연", "산", "바다"],
        "공공 서비스": ["은행", "경찰", "우체국", "관공서"],
        "문화와 사회": ["사회", "문화", "역사", "정치", "뉴스"],
        "상황 지시/기타": [] # 기본값
    }
    
    for root, kws in mapping_rules.items():
        if any(kw in meaning_kr for kw in kws):
            return "상황과 장소", root
            
    return "상황과 장소", "상황 지시/기타"

# -----------------------------------------------------------------------------
# 3. 데이터 처리 로직
# -----------------------------------------------------------------------------
def run():
    print("🚀 8,139개 단어 대규모 통합 작업을 시작합니다...")
    
    # 1. 예문 로드 (단어ID별로 그룹화)
    examples_map = defaultdict(list)
    if os.path.exists(EXAMPLES_FILE):
        with open(EXAMPLES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                lemma_id = item.get("meaning_id") # Lemma_Examples.jsonl 기준
                if lemma_id:
                    examples_map[lemma_id].append({
                        "sentence": item["example_sentence"],
                        "type": item["example_type"]
                    })
    
    # 2. 통계 로드
    stats_map = {}
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                stats_map[item["lemma"]] = item.get("total_frequency", 0)

    # 3. 전수 분류 및 스키마 통합
    mapping_data = {
        "상황과 장소": {root: [] for root in IA_V4["상황과 장소"]},
        "마음과 표현": {root: [] for root in IA_V4["마음과 표현"]},
        "구조와 기초": {root: [] for root in IA_V4["구조와 기초"]}
    }
    complete_data = {}
    uncertain_queue = []
    
    stats = {"total": 0, "success": 0, "failed": 0}
    
    with open(MEANINGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            lemma_id = item["meaning_id"]
            lemma = item["lemma"]
            pos = item["pos_ko"]
            meaning_kr = item["meaning_kr"]
            
            stats["total"] += 1
            
            # IA V4 분류
            sys_name, root_name = classify_word(lemma, pos, meaning_kr)
            
            if sys_name and root_name:
                mapping_data[sys_name][root_name].append(lemma_id)
                stats["success"] += 1
            else:
                uncertain_queue.append(lemma_id)
                stats["failed"] += 1
            
            # 스키마 통합 (Hydration)
            complete_data[lemma_id] = {
                "id": lemma_id,
                "lemma": lemma,
                "pos": pos,
                "meaning_kr": meaning_kr,
                "meaning_en": item.get("e_word"),
                "phonetic": item.get("phonetic_romanization"),
                "grade": "초" if "초" in item.get("source", "") else "중", # 단순화
                "sentences": examples_map.get(lemma_id, [])[:6],
                "frequency": stats_map.get(lemma, 0),
                "classification": {"system": sys_name, "root": root_name}
            }

    # 4. 결과 저장
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(MAPPING_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, ensure_ascii=False, indent=2)
    with open(SCHEMA_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 작업 완료!")
    print(f"📊 통계:")
    print(f"  - 전체 단어: {stats['total']}")
    print(f"  - 분류 성공: {stats['success']} ({stats['success']/stats['total']*100:.1f}%)")
    print(f"  - 분류 실패: {stats['failed']}")
    print(f"📂 결과 파일 생성:")
    print(f"  - {MAPPING_OUTPUT}")
    print(f"  - {SCHEMA_OUTPUT}")

if __name__ == "__main__":
    run()
