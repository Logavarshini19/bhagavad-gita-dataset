import json

# Load the enriched file
with open("gita_enriched.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def get_speaker_listener(ch, v):
    if ch == 1:
        if v == 1:
            return "Dhritarashtra", "Sanjaya"
        elif 2 <= v <= 20:
            return "Sanjaya", "Dhritarashtra"
        else:
            return "Arjuna", "Krishna"
    else:
        return "Krishna", "Arjuna"

# Fill in missing speaker/listener
for verse in data:
    ch = verse["chapter"]
    v = verse["verse_number"]

    speaker, listener = get_speaker_listener(ch, v)
    verse["speaker"] = speaker
    verse["listener"] = listener

# Save updated JSON
with open("gita_enriched_with_speakers.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Done. Speaker and listener fields updated for all verses.")
