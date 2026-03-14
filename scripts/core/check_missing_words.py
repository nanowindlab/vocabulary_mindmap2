import json

raw_file = "05_source/raw_dictionary/한국어 어휘사전(영어판)_사전.json"
lemma_file = "05_source/extracted_corpus/snapshot_20260309/Lemma_Meanings.jsonl"

with open(raw_file, "r") as f:
    raw_data = json.load(f)

lemma_keys = set()
with open(lemma_file, "r") as f:
    for line in f:
        item = json.loads(line)
        # Reconstruct the ID format or just use lemma
        lemma_keys.add((item["lemma"], item["meaning_kr"]))

missing = []
for entry in raw_data:
    lemma = entry["entry"]["headword_ko"]
    for sense in entry["senses"]:
        meaning = sense["definition_ko"]
        if (lemma, meaning) not in lemma_keys:
            missing.append({"lemma": lemma, "meaning": meaning})

print(f"Total raw senses: {sum(len(e['senses']) for e in raw_data)}")
print(f"Total missing: {len(missing)}")
