import json
from tqdm import tqdm

# Load extracted verses
with open("gita_enriched_with_speakers.json", "r", encoding="utf-8") as f:
    verses = json.load(f)

# Define keyword mappings
philosophy_keywords = {
    "Karma Yoga": ["karma", "action", "duty", "perform", "fruits of action", "prescribed duties"],
    "Bhakti Yoga": ["bhakti", "devotion", "devotional service", "love of God", "worship", "surrender"],
    "Jnana Yoga": ["jnana", "knowledge", "wisdom", "discrimination", "brahman", "intelligence"],
    "Sankhya": ["sankhya", "analytical study", "spirit and matter", "dual nature", "body and soul"],
    "Dhyana Yoga": ["dhyana", "meditation", "concentration", "control of mind", "yogi"],
    "Raja Yoga": ["mind discipline", "sense control", "internal renunciation", "yogic control"],
    "Vedanta": ["vedanta", "conclusion of Vedas", "paramatma", "supreme knowledge"]
}

def get_philosophical_refs(text):
    found_refs = []
    text = text.lower()
    for topic, keywords in philosophy_keywords.items():
        if any(word in text for word in keywords):
            found_refs.append(topic)
    return list(set(found_refs))  # remove duplicates

# Tag each verse
for verse in tqdm(verses, desc="📖 Tagging Philosophical References"):
    combined_text = verse.get("english_translation", "") + " " + verse.get("purport", "")
    verse["philosophical_reference"] = ", ".join(get_philosophical_refs(combined_text))

# Save updated dataset
with open("gita_dataset.json", "w", encoding="utf-8") as f:
    json.dump(verses, f, ensure_ascii=False, indent=2)

print("✅ Done. Tagged philosophical_reference for all verses.")
