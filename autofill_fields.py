import json
import spacy
from tqdm import tqdm
from pathlib import Path

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Load your dataset
INPUT_FILE = "gita_dataset_filled.json"
OUTPUT_FILE = "gita_dataset_final.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Helper functions
def extract_themes(text):
    doc = nlp(text.lower())
    themes = []
    keywords = {
        "duty": "Duty",
        "soul": "Self-realization",
        "devotion": "Devotion",
        "action": "Action",
        "karma": "Karma Yoga",
        "knowledge": "Jnana Yoga",
        "renunciation": "Renunciation",
        "mind": "Mental Discipline",
        "fear": "Fearlessness",
        "detachment": "Detachment"
    }
    for token in doc:
        for k in keywords:
            if k in token.text and keywords[k] not in themes:
                themes.append(keywords[k])
    return themes

def extract_interpretation(text):
    if "duty" in text.lower():
        return "Emphasizes the importance of performing one's duty."
    elif "soul" in text.lower():
        return "Reflects on the immortality of the soul."
    elif "action" in text.lower():
        return "Stresses detached action without attachment to results."
    return ""

def extract_real_world_example(text):
    if "duty" in text.lower():
        return "Like a soldier protecting the nation without desire for reward."
    elif "detachment" in text.lower():
        return "Like a monk renouncing worldly pleasures to pursue truth."
    elif "knowledge" in text.lower():
        return "Like a scientist relentlessly seeking the truth without bias."
    return ""

# Process and fill missing fields
for verse in tqdm(data, desc="🔍 Filling fields"):
    purport = verse.get("purport", "")
    english = verse.get("english_translation", "")

    # Theme
    if not verse["theme"]:
        verse["theme"] = extract_themes(purport or english)

    # Subthemes
    if not verse["subthemes"]:
        verse["subthemes"] = []

    # Interpretation Note
    if not verse["interpretation_note"]:
        verse["interpretation_note"] = extract_interpretation(purport or english)

    # Real-world Examples
    if not verse["real_world_example_en"]:
        verse["real_world_example_en"] = extract_real_world_example(purport or english)
    if not verse["real_world_example_ta"]:
        verse["real_world_example_ta"] = ""  # Manual later or via translation

    # Sanskrit Verse
    if not verse["sanskrit_verse"]:
        verse["sanskrit_verse"] = ""  # This needs separate script/manual curation

# Save the updated dataset
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Saved enriched dataset to {OUTPUT_FILE}")
