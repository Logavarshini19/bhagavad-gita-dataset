import json

# Define keyword mappings
emotion_keywords = {
    "fear": "Fear",
    "joy": "Joy",
    "surrender": "Surrender",
    "confusion": "Confusion",
    "peace": "Peace",
    "grief": "Grief",
    "devotion": "Devotion",
    "happiness": "Joy",
    "distress": "Confusion",
    "angry": "Anger",
    "calm": "Calm"
}

verse_type_keywords = {
    "must": "Directive",
    "should": "Directive",
    "do": "Directive",
    "perform": "Directive",
    "why": "Question",
    "how": "Question",
    "explain": "Question",
    "think": "Philosophical",
    "understand": "Philosophical",
    "know": "Philosophical",
    "says": "Descriptive",
    "describes": "Descriptive"
}

# Load the JSON file
try:
    with open("gita_output.json", "r", encoding="utf-8") as f:
        verses = json.load(f)
except Exception as e:
    print("❌ Error loading gita_output.json:", e)
    verses = []

# Auto-tag each verse
for verse in verses:
    text = verse["english_translation"].lower()

    # Tag emotion
    for word, emotion in emotion_keywords.items():
        if word in text:
            verse["emotion"] = emotion
            verse["emotion_intensity"] = 0.7 if word in ["fear", "grief", "surrender"] else 0.3
            break

    # Tag verse type
    for word, vtype in verse_type_keywords.items():
        if word in text:
            verse["verse_type"] = vtype
            break

# Debug print
if verses:
    print("🧠 First tagged verse preview:")
    print(json.dumps(verses[0], indent=4, ensure_ascii=False))

# Save enriched output
with open("gita_tagged.json", "w", encoding="utf-8") as f:
    json.dump(verses, f, indent=4, ensure_ascii=False)

print(f"✅ Done. Tagged emotions and types for {len(verses)} verses.")
