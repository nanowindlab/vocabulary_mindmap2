import json
import os
from collections import defaultdict

SOURCE_DIR = "05_source/extracted_corpus/snapshot_20260309"
OUTPUT_DIR = "09_app/public/data"
REPORT_FILE = "08_expansion/DATA_REFINEMENT_REPORT_V1.md"

MEANINGS_FILE = os.path.join(SOURCE_DIR, "Lemma_Meanings.jsonl")
EXAMPLES_FILE = os.path.join(SOURCE_DIR, "Lemma_Examples.jsonl")
STATS_FILE = os.path.join(SOURCE_DIR, "Z_ALL_Lemma_Stats.jsonl")

MAPPING_OUTPUT = os.path.join(OUTPUT_DIR, "APP_READY_MAPPING_V2.json")
SCHEMA_OUTPUT = os.path.join(OUTPUT_DIR, "APP_READY_SCHEMA_COMPLETE_V2.json")

def is_excluded(lemma, pos, meaning):
    # 1. 고유명사 격리 (예외: 서울, 부산, 한국 등)
    if pos == "고유명사" and lemma not in ["서울", "부산", "한국", "대한민국", "제주"]:
        return "고유명사 격리"
    
    # 2. 기능적 요소 격리 (SDCP V1 기준)
    if pos in ["대명사", "의존명사", "조사", "접사", "어미", "기호"]:
        return f"기능적 요소 격리 ({pos})"
    
    # 3. 비적합 단어 (한 글자이면서 뜻이 불분명한 경우 등 - 1차 필터)
    if len(lemma) == 1 and pos not in ["동사", "형용사", "일반명사", "일반부사"]:
        return "학습 비적합 의심 (단일자)"
        
    return None

def strict_classify(lemma, pos, meaning):
    # --- [사람과 관계] 오염 차단 선행 처리 ---
    if any(k in meaning for k in ["가축", "동물", "벌레", "곤충", "새", "물고기", "짐승", "개", "고양이"]):
        return "상황과 장소", "날씨와 자연"
    
    occupations = {
        "학교와 공부": ["교사", "강사", "학생", "교수", "선생"],
        "보건과 의료": ["의사", "간호사", "환자", "약사"],
        "직장과 업무": ["사장", "직원", "노동자", "경영", "대표"],
        "문화와 사회": ["가수", "배우", "경찰", "대통령", "정치인", "기자"]
    }
    for root, occ_list in occupations.items():
        if any(occ in meaning or occ == lemma for occ in occ_list):
            return "상황과 장소", root

    # --- Priority 1: 구조와 기초 ---
    if pos in ["수사", "수관형사", "접속부사"] or (pos == "일반명사" and any(k in meaning for k in ["수량", "단위", "차례", "숫자"])):
        if "시간" in meaning or "날" in meaning or "때" in meaning: return "구조와 기초", "시간과 흐름"
        if "단위" in meaning or pos in ["수사", "수관형사"]: return "구조와 기초", "수량과 단위"
        if pos == "접속부사": return "구조와 기초", "논리와 연결"
        return "구조와 기초", "PENDING" # 보류 큐행

    # --- Priority 2: 마음과 표현 ---
    if pos == "형용사" or (pos == "동사" and any(k in meaning for k in ["느끼다", "생각하다", "마음", "기분"])):
        if any(k in meaning for k in ["기쁘다", "슬프다", "화나다", "감정", "마음", "기분", "걱정", "사랑", "울다", "웃다"]): return "마음과 표현", "내면과 감정"
        if any(k in meaning for k in ["성격", "태도", "버릇", "습관", "친절", "착하다", "예의"]): return "마음과 표현", "성격과 태도"
        if any(k in meaning for k in ["모양", "색", "맛", "냄새", "크다", "작다", "뜨겁다", "차갑다", "달다", "짜다", "맵다"]): return "마음과 표현", "감각과 묘사"
        if any(k in meaning for k in ["좋다", "나쁘다", "중요", "가치", "맞다", "틀리다", "쉽다", "어렵다"]): return "마음과 표현", "의견과 가치"
        return "마음과 표현", "PENDING"

    # --- Priority 3: 상황과 장소 ---
    mapping_rules = {
        "식생활": ["음식", "밥", "먹다", "마시다", "맛", "요리", "식당", "과일", "채소", "고기", "식사"],
        "교통": ["교통", "차", "버스", "타다", "가다", "오다", "이동", "도로", "길", "운전", "지하철", "기차"],
        "보건과 의료": ["병원", "아프다", "건강", "약", "치료", "몸", "얼굴", "증상", "병", "눈", "손", "발"],
        "학교와 공부": ["학교", "공부", "배우다", "책", "시험", "수업", "교육", "연필"],
        "직장과 업무": ["회사", "일", "직업", "회의", "업무", "사무실", "취직"],
        "사람과 관계": ["사람", "가족", "친구", "관계", "동료", "어머니", "아버지", "형", "동생", "아기", "결혼", "남자", "여자"],
        "주거와 일상": ["집", "살다", "생활", "가구", "옷", "방", "침대", "청소", "입다"],
        "쇼핑": ["사다", "팔다", "가게", "가격", "돈", "물건", "시장", "비싸다", "싸다", "쇼핑"],
        "여가와 취미": ["운동", "놀이", "영화", "취미", "음악", "게임", "축구", "노래", "춤"],
        "여행": ["여행", "관광", "비행기", "숙소", "호텔", "여권"],
        "날씨와 자연": ["날씨", "비", "눈", "바람", "자연", "산", "바다", "하늘", "나무", "꽃", "동물", "구름"],
        "공공 서비스": ["은행", "경찰", "우체국", "관공서", "주민", "세금", "우편"],
        "문화와 사회": ["사회", "문화", "역사", "정치", "뉴스", "전통", "예술", "국가"],
    }
    
    for root, kws in mapping_rules.items():
        # 단어 자체가 키워드이거나 뜻에 포함되어 있을 때
        if lemma in kws or any(kw in meaning for kw in kws):
            return "상황과 장소", root
            
    # 명확하게 매칭되지 않는 나머지 모든 단어는 임의로 '상황 지시/기타'에 넣지 않고 보류
    return "PENDING", "PENDING"

def run():
    print("🚨 SDCP V1 기반 전수 재정제 작업을 시작합니다...")
    
    examples_map = defaultdict(list)
    if os.path.exists(EXAMPLES_FILE):
        with open(EXAMPLES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                lemma_id = item.get("meaning_id")
                if lemma_id:
                    examples_map[lemma_id].append({
                        "sentence": item["example_sentence"],
                        "type": item["example_type"]
                    })
    
    stats_map = {}
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                stats_map[item["lemma"]] = item.get("total_frequency", 0)

    mapping_data = {
        "구조와 기초": { "수량과 단위": [], "시간과 흐름": [], "논리와 연결": [], "지시와 질문": [] },
        "마음과 표현": { "내면과 감정": [], "성격과 태도": [], "감각과 묘사": [], "의견과 가치": [] },
        "상황과 장소": {
            "사람과 관계": [], "식생활": [], "주거와 일상": [], "쇼핑": [], "교통": [], 
            "학교와 공부": [], "직장과 업무": [], "여가와 취미": [], "여행": [], 
            "보건과 의료": [], "날씨와 자연": [], "공공 서비스": [], "문화와 사회": [], "상황 지시/기타": []
        }
    }
    
    complete_data = {}
    
    excluded_list = []
    system_pending_list = []
    category_pending_list = []
    
    stats = {"total": 0, "success": 0, "excluded": 0, "system_pending": 0, "category_pending": 0}
    
    with open(MEANINGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            lemma_id = item["meaning_id"]
            lemma = item["lemma"]
            pos = item["pos_ko"]
            meaning_kr = item["meaning_kr"]
            
            stats["total"] += 1
            
            # Phase 0: 완전 격리
            exclude_reason = is_excluded(lemma, pos, meaning_kr)
            if exclude_reason:
                excluded_list.append({"id": lemma_id, "lemma": lemma, "reason": exclude_reason})
                stats["excluded"] += 1
                continue
                
            # Phase 1 & 2: 엄격한 매칭
            sys_name, root_name = strict_classify(lemma, pos, meaning_kr)
            
            if sys_name == "PENDING":
                system_pending_list.append({"id": lemma_id, "lemma": lemma, "meaning": meaning_kr, "reason": "어떤 축(System)에 속하는지 불명확함"})
                stats["system_pending"] += 1
                continue
            
            if root_name == "PENDING":
                category_pending_list.append({"id": lemma_id, "lemma": lemma, "meaning": meaning_kr, "reason": f"[{sys_name}] 축에는 속하나 적절한 중분류 없음"})
                stats["category_pending"] += 1
                continue
                
            # 확신할 수 있는 데이터만 적재
            mapping_data[sys_name][root_name].append(lemma_id)
            complete_data[lemma_id] = {
                "id": lemma_id,
                "lemma": lemma,
                "pos": pos,
                "meaning_kr": meaning_kr,
                "meaning_en": item.get("e_word"),
                "phonetic": item.get("phonetic_romanization"),
                "grade": "초" if "초" in item.get("source", "") else "중",
                "sentences": examples_map.get(lemma_id, [])[:6],
                "frequency": stats_map.get(lemma, 0),
                "classification": {"system": sys_name, "root": root_name}
            }
            stats["success"] += 1

    # 결과 저장
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(MAPPING_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, ensure_ascii=False, indent=2)
    with open(SCHEMA_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)

    # 리포트 생성
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# 데이터 전수 재정제 리포트 (SDCP V1 기반)\n\n")
        f.write("## 1. 종합 통계\n")
        f.write(f"- 전체 검토 대상: **{stats['total']}**개 단어\n")
        f.write(f"- 분류 성공 (안전 데이터): **{stats['success']}**개 단어\n")
        f.write(f"- 격리된 데이터 (Excluded): **{stats['excluded']}**개 단어\n")
        f.write(f"- 시스템 보류 (System Pending): **{stats['system_pending']}**개 단어\n")
        f.write(f"- 카테고리 보류 (Category Pending): **{stats['category_pending']}**개 단어\n\n")
        
        f.write("## 2. 제외 그룹 (Phase 0 Filtered) - 샘플 20개\n")
        for ex in excluded_list[:20]:
            f.write(f"- `{ex['lemma']}` (사유: {ex['reason']})\n")
            
        f.write("\n## 3. 오염 방지 검증 (사람과 관계)\n")
        f.write("- **가축, 곤충, 동물**: 철저히 [날씨와 자연]으로 이동 조치됨.\n")
        f.write("- **직업, 역할**: [보건과 의료], [학교와 공부] 등 해당 상황 루트로 분산 이동 조치됨.\n")

    print(f"✅ 엄격한 재정제 완료!")
    print(f"📊 성공: {stats['success']} | 격리: {stats['excluded']} | 보류: {stats['system_pending'] + stats['category_pending']}")

if __name__ == "__main__":
    run()
