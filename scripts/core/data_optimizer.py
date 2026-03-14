import json
import os
import math

SCHEMA_FILE = "09_app/public/data/APP_READY_SCHEMA_COMPLETE_V1.json"
OUTPUT_DIR = "09_app/public/data/chunks"
CHUNK_SIZE = 1000

def run():
    print("📦 데이터 최적화(Chunking)를 시작합니다...")
    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ {SCHEMA_FILE}을 찾을 수 없습니다.")
        return

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 단어 ID 리스트
    all_ids = list(data.keys())
    total_count = len(all_ids)
    num_chunks = math.ceil(total_count / CHUNK_SIZE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    manifest = {}
    
    for i in range(num_chunks):
        start = i * CHUNK_SIZE
        end = min((i + 1) * CHUNK_SIZE, total_count)
        chunk_ids = all_ids[start:end]
        
        chunk_data = {cid: data[cid] for cid in chunk_ids}
        chunk_filename = f"APP_READY_CHUNK_{i+1:03d}.json"
        chunk_path = os.path.join(OUTPUT_DIR, chunk_filename)
        
        with open(chunk_path, "w", encoding="utf-8") as f:
            json.dump(chunk_data, f, ensure_ascii=False)
        
        # Manifest에 매핑 정보 기록 (어느 ID가 어느 Chunk에 있는지)
        for cid in chunk_ids:
            manifest[cid] = chunk_filename
            
        print(f"  - Chunk {i+1} 생성 완료: {chunk_filename} ({len(chunk_ids)}단어)")

    # Manifest 저장
    with open(os.path.join(OUTPUT_DIR, "CHUNK_MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 최적화 완료! 총 {total_count}개 단어가 {num_chunks}개 조각으로 분리되었습니다.")

if __name__ == "__main__":
    run()
