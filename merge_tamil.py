import json

# Load English verse data
with open("gita_output.json", "r", encoding="utf-8") as f:
    gita_data = json.load(f)

# Load Tamil verse translations
with open("tamil_gita.json", "r", encoding="utf-8") as f:
    tamil_data = json.load(f)

# Convert tamil data to dict for fast lookup
tamil_lookup = {item["verse_id"]: item["tamil_translation"] for item in tamil_data}

# Merge tamil translations
missing = 0
for verse in gita_data:
    verse_id = verse["verse_id"]
    if verse_id in tamil_lookup:
        verse["tamil_translation"] = tamil_lookup[verse_id]
    else:
        verse["tamil_translation"] = ""
        missing += 1

# Save enriched dataset
with open("gita_enriched.json", "w", encoding="utf-8") as f:
    json.dump(gita_data, f, ensure_ascii=False, indent=2)

print(f"✅ Merged Tamil translations into {len(gita_data)} verses.")
print(f"❌ Missing Tamil translations for {missing} verses.")
