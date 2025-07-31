import json
from difflib import SequenceMatcher
from tqdm import tqdm

# Load English verses
with open("gita_output.json", "r", encoding="utf-8") as f:
    english_verses = json.load(f)

# Load Tamil OCR pages
with open("tamil_verses.json", "r", encoding="utf-8") as f:
    tamil_pages = json.load(f)

# Flatten Tamil text into one long string
tamil_text = " ".join([page["text"].replace("\n", " ") for page in tamil_pages])

# Preprocess function
def clean(text):
    return text.replace("\n", " ").strip().lower()

# Very naive split for demo – later you can improve with verse markers
tamil_chunks = tamil_text.split("பகவத்கீதை")[1:]  # split by word after first intro
tamil_chunks = ["பகவத்கீதை" + chunk for chunk in tamil_chunks]

# Align verses (very rough fuzzy matching)
matched_verses = []
for i, verse in tqdm(enumerate(english_verses), total=len(english_verses), desc="🔗 Matching verses"):
    eng = clean(verse["english_translation"])
    
    best_match = ""
    best_score = 0
    best_index = -1

    for j, chunk in enumerate(tamil_chunks):
        tam = clean(chunk)
        score = SequenceMatcher(None, eng[:50], tam[:200]).ratio()
        if score > best_score:
            best_score = score
            best_match = chunk
            best_index = j

    # Attach Tamil translation to verse
    verse["tamil_translation"] = best_match.strip()
    matched_verses.append(verse)

# Save enriched JSON
with open("tamil_gita.json", "w", encoding="utf-8") as f:
    json.dump(matched_verses, f, indent=2, ensure_ascii=False)

print("✅ Done. Saved Tamil-enriched Gita as 'tamil_gita.json'")
