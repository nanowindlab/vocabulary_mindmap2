import json
from pathlib import Path

def find_word(filename, target_word):
    path = Path("09_app/public/data/live") / filename
    if not path.exists(): return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            if item.get("word") == target_word:
                return item
    return None

print("--- [가방] 데이터 실측 샘플 ---")
search_item = find_word("APP_READY_SEARCH_INDEX.json", "가방")
if search_item:
    print(f"📍 통합 검색 인덱스 (Search Index):")
    print(f"  - 연관 어휘(related_vocab): {search_index_related := search_item.get('related_vocab', [])}")
    print(f"  - 연관 어휘 개수: {len(search_index_related)}")

# Tree 파일들에서도 refs.cross_links 확인
trees = ["APP_READY_SITUATIONS_TREE.json", "APP_READY_EXPRESSIONS_TREE.json", "APP_READY_BASICS_TREE.json"]
for tree in trees:
    tree_item = find_word(tree, "가방")
    if tree_item:
        print(f"\n📍 {tree}:")
        print(f"  - 횡단 링크(refs.cross_links): {tree_item.get('refs', {}).get('cross_links', [])}")
