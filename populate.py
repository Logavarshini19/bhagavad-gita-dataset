import json
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, OWL, XSD

# --- 1. Define Namespaces ---
# IMPORTANT: This URI must exactly match the base URI you set in Protégé.
BG_NAMESPACE_STR = "http://www.semanticweb.org/varshini/ontologies/2025/8/Bhagavad_Gita#"
BG = Namespace(BG_NAMESPACE_STR)

# --- 2. Initialize Graph and Load Schema ---
g = Graph()
g.bind("bg", BG)
g.bind("owl", OWL)
g.bind("rdf", RDF)

# Ensure the correct file name and format are used for loading the SCHEMA
SCHEMA_FILE = "Bhagavad_Gita_Ontology.ttl"

try:
    # We use g.parse() for loading schemas (even if empty)
    # The format is set to 'turtle' as requested.
    g.parse(SCHEMA_FILE, format="turtle")
    print(f"Schema '{SCHEMA_FILE}' loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR LOADING SCHEMA: {e}")
    print("Please ensure your schema file is saved as 'Bhagavad_Gita_Ontology.ttl' and is valid Turtle/OWL.")
    exit()

# --- 3. Load Annotated JSON Data ---
JSON_FILE = "gemini_data.json"

try:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"JSON data '{JSON_FILE}' loaded successfully (Total verses in JSON: {len(data)})")
except FileNotFoundError:
    print(f"Error: JSON file '{JSON_FILE}' not found. Check the file name and path.")
    exit()

# --- 4. Function to Create Clean URIs ---
def create_uri(name):
    """Converts a string name into a clean, namespaced URI."""
    if isinstance(name, str):
        # Remove spaces, commas, and handle URI fragments
        clean_name = name.replace(" ", "").replace(",", "").replace("/", "")
        return BG[clean_name]
    return name

# --- 5. Populate the Graph with Verse Data ---
for verse in data:
    verse_id = verse.get("verse_id")
    if not verse_id:
        print(f"Warning: Skipping verse due to missing 'verse_id' field.")
        continue

    verse_uri = create_uri(verse_id)
    
    # 5.1 Declare the main individual (Verse)
    g.add((verse_uri, RDF.type, BG.Verse))

    # 5.2 Add Data Properties (Literals)
    g.add((verse_uri, BG.hasVerseId, Literal(verse_id, datatype=XSD.string)))
    g.add((verse_uri, BG.hasChapterNumber, Literal(verse.get("chapter"), datatype=XSD.integer)))
    g.add((verse_uri, BG.hasVerseNumber, Literal(verse.get("verse_number"), datatype=XSD.integer)))
    g.add((verse_uri, BG.hasSanskritVerseText, Literal(verse.get("sanskrit_verse", ""), lang="sa")))
    g.add((verse_uri, BG.hasEnglishTranslation, Literal(verse.get("english_translation", ""), lang="en")))
    g.add((verse_uri, BG.hasTamilTranslation, Literal(verse.get("tamil_translation", ""), lang="ta")))
    g.add((verse_uri, BG.hasVerseType, Literal(verse.get("verse_type", ""), datatype=XSD.string)))
    g.add((verse_uri, BG.hasInterpretationNote, Literal(verse.get("interpretation_note", ""), lang="en")))
    g.add((verse_uri, BG.hasDialogueContext, Literal(verse.get("dialogue_context", ""), lang="en")))
    g.add((verse_uri, BG.hasCertaintyScore, Literal(verse.get("certainty_score", 0.0), datatype=XSD.double)))
    g.add((verse_uri, BG.hasReferenceURL, Literal(verse.get("reference_url", ""))))
    
    # 5.3 Link Speaker/Listener and Declare them as Individuals
    # Use the specific Speaker/Listener class names (e.g., Dhritarashtra, Arjuna)
    speaker_name = verse.get("speaker")
    listener_name = verse.get("listener")

    if speaker_name:
        speaker_uri = create_uri(speaker_name)
        g.add((verse_uri, BG.isSpokenBy, speaker_uri))
        g.add((speaker_uri, RDF.type, BG[speaker_name.replace(" ", "")])) # Links individual to its class

    if listener_name:
        listener_uri = create_uri(listener_name)
        g.add((verse_uri, BG.isListenedBy, listener_uri))
        g.add((listener_uri, RDF.type, BG[listener_name.replace(" ", "")]))
    
    # 5.4 Add Object Properties (Themes, Emotions, Frameworks, Tags)

    # Theme (Can be multiple)
    for theme in verse.get("theme", []):
        g.add((verse_uri, BG.hasTheme, create_uri(theme)))

    # Emotion (Single value)
    emotion_name = verse.get("emotion")
    if emotion_name:
        emotion_uri = create_uri(emotion_name)
        g.add((verse_uri, BG.evokesEmotion, emotion_uri))
        # Add emotion intensity as a data property of the Emotion individual
        g.add((emotion_uri, BG.hasEmotionIntensity, Literal(verse.get("emotion_intensity", 0.0), datatype=XSD.double)))
    
    # Ethical Framework (Single value)
    framework_name = verse.get("ethical_framework")
    if framework_name:
        g.add((verse_uri, BG.alignsWithEthicalFramework, create_uri(framework_name)))

    # Shastra Category (Single value)
    category_name = verse.get("shastra_category")
    if category_name:
        g.add((verse_uri, BG.isCategorizedAs, create_uri(category_name)))

    # Tags (Can be multiple)
    for tag in verse.get("tags", []):
        g.add((verse_uri, BG.hasTag, create_uri(tag)))
        
    # Source Metadata
    translator_name = verse.get("source_translator")
    if translator_name:
        g.add((verse_uri, BG.hasSourceTranslator, create_uri(translator_name)))
        
    commentary_name = verse.get("reference_commentary")
    if commentary_name:
        g.add((verse_uri, BG.hasReferenceCommentary, create_uri(commentary_name)))

# --- 6. Save the Populated Ontology ---
OUTPUT_FILE = "bhagavad-gita-populated.ttl"
g.serialize(destination=OUTPUT_FILE, format="turtle")

print("\n--- POPULATION COMPLETE ---")
print(f"Knowledge Graph saved to: {OUTPUT_FILE}")
print(f"Total Triples Generated: {len(g)}")
print("You are now ready to start the AI Querying and Reasoning phase!")