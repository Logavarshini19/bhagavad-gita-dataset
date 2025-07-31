import json
from pathlib import Path

INPUT_FILE = "gita_dataset_final.json"   # Replace with your latest enriched file name if different
OUTPUT_FILE = "gita_dataset_complete.json"

# Define all possible fields in your schema
ALL_FIELDS = [
    "verse_id",
    "chapter",
    "verse_number",
    "speaker",
    "listener",
    "english_translation",
    "tamil_translation",
    "sanskrit_verse",
    "verse_type",
    "theme",
    "subthemes",
    "emotion",
    "emotion_intensity",
    "ethical_framework",
    "ethical_value",
    "shastra_category",
    "dialogue_context",
    "philosophical_reference",
    "real_world_example_en",
    "real_world_example_ta",
    "interpretation_note",
    "certainty_score",
    "source_translator",
    "reference_commentary",
    "reference_url",
    "rdf_mapping",
    "tags",
    "purport"
]

# Load your data
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalize each verse to ensure all fields are present
for verse in data:
    for field in ALL_FIELDS:
        if field not in verse:
            verse[field] = None

# Save completed dataset
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Completed: All missing fields filled with nulls. Saved as '{OUTPUT_FILE}'")
