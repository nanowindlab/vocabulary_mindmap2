import json

payload_file = "09_app/public/data/APP_READY_CORE_PAYLOAD_V1.json"
source_file = "05_source/extracted_corpus/snapshot_20260309/Lemma_Meanings.jsonl"
tree_out = "09_app/public/data/APP_READY_CORE_TREE_V1.json"
search_out = "09_app/public/data/APP_READY_SEARCH_INDEX_V1.json"

with open(payload_file, "r") as f:
    payload = json.load(f)

source_data = {}
with open(source_file, "r") as f:
    for line in f:
        item = json.loads(line)
        source_data[item["meaning_id"]] = item

new_tree = []
new_search = []

for m_id, cls_info in payload.items():
    if m_id not in source_data:
        continue
    src = source_data[m_id]
    
    # Map to the format the app expects but with new IA V4
    node = {
        "id": m_id,
        "word": src.get("lemma", ""),
        "pos": src.get("pos_ko", ""),
        "roman": src.get("phonetic_romanization", ""),
        "def_kr": src.get("meaning_kr", ""),
        "def_en": src.get("e_word", ""),
        "hierarchy": {
            "system": cls_info.get("system", ""),
            "root": cls_info.get("root", ""),
            "path_ko": f"{cls_info.get('system', '')} > {cls_info.get('root', '')}"
        },
        "stats": {
            "freq": src.get("frequency", 0),
            "rank": src.get("frequency_rank", 0),
            "grade": src.get("grade", "초"),
            "grade_en": src.get("grade_en", "Beginner")
        }
    }
    new_tree.append(node)
    
    # Search index
    search_node = {
        "id": m_id,
        "word": src.get("lemma", ""),
        "roman": src.get("phonetic_romanization", ""),
        "system": cls_info.get("system", ""),
        "root": cls_info.get("root", "")
    }
    new_search.append(search_node)

with open(tree_out, "w") as f:
    json.dump(new_tree, f, ensure_ascii=False, indent=2)

with open(search_out, "w") as f:
    json.dump(new_search, f, ensure_ascii=False, indent=2)

print(f"Generated {len(new_tree)} tree items and {len(new_search)} search items.")
