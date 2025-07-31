import json

# Load tagged verses
with open("gita_tagged.json", "r", encoding="utf-8") as f:
    verses = json.load(f)

# Theme & subtheme keyword mapping
THEME_MAP = {
    "karma": ("Karma Yoga", "Nishkama Karma"),
    "duty": ("Karma Yoga", "Nishkama Karma"),
    "action": ("Karma Yoga", "Righteous Action"),
    "renounce": ("Renunciation", "Sannyasa"),
    "renunciation": ("Renunciation", "Tyaga"),
    "devotion": ("Bhakti Yoga", "Personal Relationship"),
    "bhakti": ("Bhakti Yoga", "Loving Surrender"),
    "love": ("Bhakti Yoga", "Personal Relationship"),
    "soul": ("Atma Tattva", "Immortality"),
    "atma": ("Atma Tattva", "Eternal Nature"),
    "knowledge": ("Jnana Yoga", "Self-realization"),
    "wisdom": ("Jnana Yoga", "Discrimination"),
    "discipline": ("Dhyana Yoga", "Mental Control"),
    "yoga": ("Dhyana Yoga", "Union"),
    "mind": ("Dhyana Yoga", "Control"),
    "equality": ("Samatva", "Non-discrimination"),
    "vision": ("Samatva", "Equanimity"),
    "desire": ("Detachment", "Sense Control"),
    "attachment": ("Detachment", "Letting Go"),
    "fear": ("Emotion", "Fear"),
    "confusion": ("Emotion", "Doubt"),
}

# Function to auto-tag theme/subtheme
def tag_theme(verse):
    text = (verse.get("english_translation", "") + " " + verse.get("purport", "")).lower()
    tags = set()

    for keyword, (theme, subtheme) in THEME_MAP.items():
        if keyword in text:
            tags.add((theme, subtheme))

    if tags:
        verse["theme"] = list(set(t[0] for t in tags))
        verse["subthemes"] = list(set(t[1] for t in tags))

    return verse

# Process each verse
tagged = [tag_theme(v) for v in verses]

# Save the enriched file
with open("gita_enriched.json", "w", encoding="utf-8") as f:
    json.dump(tagged, f, indent=4, ensure_ascii=False)

print(f"🏷️  Tagged themes and subthemes for {len(tagged)} verses.")
