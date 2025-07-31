import json
from tqdm import tqdm

# Keywords for inference
verse_types = {"Krishna": "instructional", "Arjuna": "emotional", "Sanjaya": "narrative", "Dhritarashtra": "inquisitive"}
shastra_keywords = {
    "karma": "Karma Shastra", "action": "Karma Shastra", "duty": "Karma Shastra",
    "jnana": "Jnana Shastra", "wisdom": "Jnana Shastra", "knowledge": "Jnana Shastra",
    "bhakti": "Bhakti Shastra", "devotion": "Bhakti Shastra"
}
emotions = {
    "fear": "Fear", "grief": "Grief", "joy": "Joy", "anger": "Anger",
    "confidence": "Confidence", "resolve": "Resolve", "doubt": "Doubt", "peace": "Peace"
}
themes_catalog = ["Duty", "Self-realization", "Devotion", "Sacrifice", "Discipline", "Detachment"]

def infer_shastra(purport):
    text = purport.lower()
    for k, v in shastra_keywords.items():
        if k in text:
            return v
    return "General Philosophy"

def infer_emotion(purport):
    text = purport.lower()
    for k, v in emotions.items():
        if k in text:
            return v
    return "Contemplative"

def infer_theme(purport):
    matched = []
    for theme in themes_catalog:
        if theme.lower() in purport.lower():
            matched.append(theme)
    return matched

def generate_example(ethical_value):
    if ethical_value.lower() == "duty":
        return (
            "A soldier who defends the country even when afraid, driven by duty.",
            "ஒரு வீரன், பயத்துடன் கூட நாட்டை பாதுகாக்கின்றான் – இது கடமை உணர்வு."
        )
    elif ethical_value.lower() == "fearlessness":
        return (
            "A fireman rushing into danger to save others despite risks.",
            "ஆபத்தைக் கண்டு பயப்படாமல் பனிக்காரர் மற்றவர்களை காப்பாற்ற செல்கிறார்."
        )
    return ("", "")

def fill_attributes(verse):
    purport = verse.get("purport", "")
    
    # Fill verse_type
    if not verse.get("verse_type"):
        verse["verse_type"] = verse_types.get(verse["speaker"], "narrative")

    # Fill shastra_category
    if not verse.get("shastra_category"):
        verse["shastra_category"] = infer_shastra(purport)

    # Fill dialogue_context
    if not verse.get("dialogue_context"):
        verse["dialogue_context"] = f'{verse["speaker"]} addressing {verse["listener"]}'

    # Fill theme/subthemes
    if not verse.get("theme") or not isinstance(verse["theme"], list) or not verse["theme"]:
        verse["theme"] = infer_theme(purport)

    if not verse.get("subthemes"):
        verse["subthemes"] = []

    # Fill emotion
    if not verse.get("emotion"):
        verse["emotion"] = infer_emotion(purport)
        verse["emotion_intensity"] = 0.6

    # Fill real world examples
    if not verse.get("real_world_example_en"):
        en, ta = generate_example(verse.get("ethical_value", ""))
        verse["real_world_example_en"] = en
        verse["real_world_example_ta"] = ta

    # Fill tags
    if not verse.get("tags"):
        tags = [verse["ethical_value"], verse["emotion"], verse["shastra_category"]] + verse["theme"]
        verse["tags"] = list(set(filter(None, tags)))

    # Fill certainty_score
    if not verse.get("certainty_score"):
        verse["certainty_score"] = 0.75

    return verse

# Load, process, and save
with open("gita_dataset.json", "r", encoding="utf-8") as infile:
    verses = json.load(infile)

updated_verses = [fill_attributes(v) for v in tqdm(verses)]

with open("gita_dataset_filled.json", "w", encoding="utf-8") as outfile:
    json.dump(updated_verses, outfile, indent=4, ensure_ascii=False)

print("✅ Saved enriched dataset to gita_dataset_filled.json")
