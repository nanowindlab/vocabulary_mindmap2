import json

tree_out = "09_app/public/data/APP_READY_CORE_TREE_V1.json"

with open(tree_out, "r") as f:
    data = json.load(f)

for item in data:
    hier = item.get("hierarchy", {})
    # IA V4 체계에 맞게 강제 변환
    # 시스템 (예: 상황과 장소) -> root_id
    # 루트 (예: 쇼핑) -> scene
    # 품사 (예: 일반명사) -> category
    system = hier.get("system", "")
    root = hier.get("root", "")
    
    if system and root:
        hier["root_id"] = system
        hier["scene"] = root
        hier["category"] = item.get("pos", "기타")
        hier["path_ko"] = f"{system} > {root} > {hier['category']}"
        
with open(tree_out, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Fixed APP_READY_CORE_TREE_V1.json schema mapping for frontend.")
