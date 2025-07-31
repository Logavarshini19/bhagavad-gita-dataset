import fitz  # PyMuPDF
import json
import re

# CONFIG
pdf_path = "Bhagavad-gita.pdf"
output_json = "gita_output.json"

doc = fitz.open(pdf_path)
output = []

chapter = 0
verse_number = 0
current_verse = {}
parsing_purport = False

def save_current_verse():
    if "verse_id" in current_verse:
        output.append(current_verse.copy())

for page in doc:
    text = page.get_text()

    # Check for new chapter
    chapter_match = re.search(r"CHAPTER (\w+)", text)
    if chapter_match:
        chapter += 1
        verse_number = 0

    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Start of new verse
        if line.strip().startswith("TEXT"):
            if "verse_id" in current_verse:
                save_current_verse()
            verse_number += 1
            current_verse = {
                "verse_id": f"BG_{chapter}.{verse_number}",
                "chapter": chapter,
                "verse_number": verse_number,
                "speaker": "",
                "listener": "",
                "english_translation": "",
                "tamil_translation": "",
                "sanskrit_verse": "",
                "verse_type": "",
                "theme": [],
                "subthemes": [],
                "emotion": "",
                "emotion_intensity": 0.0,
                "ethical_framework": "",
                "ethical_value": "",
                "shastra_category": "",
                "dialogue_context": "",
                "philosophical_reference": "",
                "real_world_example_en": "",
                "real_world_example_ta": "",
                "interpretation_note": "",
                "certainty_score": 0.0,
                "source_translator": "A. C. Bhaktivedanta Swami Prabhupada",
                "reference_commentary": "Prabhupada Purport",
                "reference_url": "",
                "rdf_mapping": "",
                "tags": []
            }
            parsing_purport = False

        elif line.strip() == "TRANSLATION":
            # Next line(s) is English translation
            trans_text = []
            for j in range(i + 1, len(lines)):
                if lines[j].strip() in ["PURPORT", ""]:
                    break
                trans_text.append(lines[j].strip())
            current_verse["english_translation"] = " ".join(trans_text)

        elif line.strip() == "PURPORT":
            parsing_purport = True
            current_verse["purport"] = ""

        elif parsing_purport:
            if line.strip().startswith("TEXT") or re.match(r"CHAPTER (\w+)", line):
                parsing_purport = False
            else:
                current_verse["purport"] += line.strip() + " "

# Save the last verse
if "verse_id" in current_verse:
    save_current_verse()

# Save to JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"✅ Done. Extracted {len(output)} verses.")
