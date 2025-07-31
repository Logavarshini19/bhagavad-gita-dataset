import json
from tqdm import tqdm

with open("gita_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def infer_ethical_tags(verse):
    text = (verse.get("english_translation", "") + " " + verse.get("purport", "")).lower()

    # Simple keyword-based rules
    if any(k in text for k in ["duty", "dharma", "responsibility", "action without attachment"]):
        return "Karma Yoga", "Duty"
    if any(k in text for k in ["devotion", "surrender", "krishna", "bhakti", "love of god"]):
        return "Bhakti Yoga", "Devotion"
    if any(k in text for k in ["knowledge", "wisdom", "discrimination", "discernment", "intellect"]):
        return "Jnana Yoga", "Wisdom"
    if any(k in text for k in ["fear", "worry", "courage", "arjuna scared"]):
        return "Mental Discipline", "Fearlessness"
    if any(k in text for k in ["detached", "renunciation", "not desiring", "equanimity"]):
        return "Renunciation", "Detachment"
    if any(k in text for k in ["humble", "humility", "meek", "not proud"]):
        return "Character", "Humility"
    if any(k in text for k in ["control", "restrain", "self-restraint"]):
        return "Discipline", "Self-Control"

    return "", ""  # Default if no match

for verse in tqdm(data, desc="🧭 Tagging ethical values"):
    framework, value = infer_ethical_tags(verse)
    verse["ethical_framework"] = framework
    verse["ethical_value"] = value

with open("gita_dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Tagged ethical values for all verses.")
