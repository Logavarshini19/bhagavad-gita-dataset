import os
import json
import re
import time
import sys
import subprocess
import hashlib
import numpy as np
from pathlib import Path
from collections import defaultdict

# Try to import FAISS
try:
    import faiss
except Exception:
    raise RuntimeError("FAISS not installed. Install with: pip install faiss-cpu")

# AUTO-LOAD ENV FILE
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Enable OpenAI if key exists
if os.getenv("OPENAI_API_KEY") and os.getenv("USE_OPENAI") is None:
    os.environ["USE_OPENAI"] = "1"

# CONFIG
DATAFILE = Path(r"d:/Bhagavad Gita/gemini_data.json")
INDEX_DIR = Path(r"d:/Bhagavad Gita/faiss_index")
EMB_MODEL = "text-embedding-4"
HASH_DIM = 1024
BATCH = 8

INDEX_DIR.mkdir(parents=True, exist_ok=True)

PRINCIPLE_KEYWORDS = {
    "duty": ["duty", "karma", "action", "work", "responsibility", "svadharma"],
    "detachment": ["detachment", "attachment", "fruit", "outcome", "result"],
    "courage": ["fear", "bravery", "courage", "doubt"],
    "clarity": ["clarity", "confusion", "wisdom", "know"],
    "self-discipline": ["discipline", "practice", "control"],
    "compassion": ["love", "compassion", "care", "kindness"]
}

_word_re = re.compile(r"\w+")

def tokenize(text):
    return _word_re.findall((text or "").lower())

def prepare_text(d):
    fields = ["english_translation", "interpretation_note", "tags",
              "real_world_example_en", "reference_commentary", "purport"]

    parts = []
    for k in fields:
        v = d.get(k)
        if isinstance(v, list): parts.append(" ".join(v))
        elif isinstance(v, str): parts.append(v)

    if not parts:
        parts = [d.get("english_translation") or d.get("verse") or ""]

    return " ".join([p for p in parts if p]).strip()


def load_documents(path=DATAFILE):
    data = json.load(open(path, "r", encoding="utf-8"))
    docs, texts, meta = [], [], []

    for d in data:
        if not isinstance(d, dict) or not d.get("verse_id"):
            continue

        txt = prepare_text(d)
        docs.append(d)
        texts.append(txt)
        meta.append({
            "verse_id": d["verse_id"],
            "chapter": d.get("chapter"),
            "verse_number": d.get("verse_number"),
            "speaker": d.get("speaker"),
            "certainty_score": d.get("certainty_score", 0.5),
            "tags": d.get("tags", [])
        })

    return docs, texts, meta


def _test_openai():
    """Check if OpenAI module is importable in a clean subprocess."""
    try:
        p = subprocess.run([sys.executable, "-c", "import openai"], timeout=4)
        return p.returncode == 0
    except:
        return False


# ------------------ EMBEDDING BACKENDS -------------------
def get_embedding_backend():
    # 1. OpenAI
    if os.getenv("USE_OPENAI", "0") == "1" and os.getenv("OPENAI_API_KEY"):
        if _test_openai():
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

                def openai_embed(texts):
                    results = []
                    for i in range(0, len(texts), BATCH):
                        batch = texts[i:i+BATCH]
                        resp = client.embeddings.create(model=EMB_MODEL, input=batch)
                        for d in resp.data:
                            results.append(np.array(d.embedding, dtype=np.float32))
                        time.sleep(0.1)
                    return np.vstack(results)

                return "openai", openai_embed
            except:
                pass

    # 2. SBERT local model
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-mpnet-base-v2")

        def sbert_embed(texts):
            arr = model.encode(texts, convert_to_numpy=True)
            return np.array(arr, dtype=np.float32)

        return "sbert", sbert_embed
    except:
        pass

    # 3. Hash-based fallback (always works)
    def hash_embed(texts, dim=HASH_DIM):
        out = np.zeros((len(texts), dim), dtype=np.float32)
        for i, t in enumerate(texts):
            for tok in tokenize(t):
                h = int.from_bytes(hashlib.md5(tok.encode()).digest(), "little")
                out[i, h % dim] += 1
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        out = out / (norms + 1e-9)
        return out

    return "hash", hash_embed


_backend_name, _embed_fn = get_embedding_backend()
print(f"Embedding backend detected: {_backend_name}")

def embed_texts(texts): return _embed_fn(texts)

def embed_query(q):
    vec = embed_texts([q])
    faiss.normalize_L2(vec)
    return vec


# =================== PRINCIPLE DETECTION ======================
def detect_principles(text):
    text_l = text.lower()
    found = set()
    for p, kws in PRINCIPLE_KEYWORDS.items():
        if any(kw in text_l for kw in kws):
            found.add(p)
    return found


def aggregate_principles(meta, scores, indices, top_k):
    agg = defaultdict(float)
    total = 0

    for s, idx in zip(scores[:top_k], indices[:top_k]):
        m = meta[idx]
        sig = " ".join([str(m["speaker"]), " ".join(m["tags"])])
        principles = detect_principles(sig)

        weight = s * max(0.01, m.get("certainty_score", 0.5))
        total += weight

        for p in principles: agg[p] += weight

    if total > 0:
        for k in agg: agg[k] /= total

    return dict(sorted(agg.items(), key=lambda x: -x[1]))


# ======================== ADVISOR LOGIC =========================
def infer_truth(query, principles):
    q = query.lower()

    if "fail" in q or "scared" in q:
        return "You're catastrophizing instead of committing to action."
    if "confus" in q:
        return "You're waiting for clarity instead of generating it."
    if "anx" in q:
        return "You're treating discomfort like danger — it's not."
    if "love" in q or "relationship" in q:
        return "You're letting someone else's reaction define your identity."
    if "career" in q or "job" in q or "startup" in q:
        return "You're obsessed with outcomes instead of building capability."

    if "detachment" in principles:
        return "You're gripping too hard to outcomes; it's shrinking your range of action."

    return "You're overestimating intentions and underestimating execution."


def gita_insight(principles):
    out = []
    if "duty" in principles:
        out.append("Act from duty; effort is what you control.")
    if "detachment" in principles:
        out.append("Detach from the fruit; it frees your execution.")
    if "courage" in principles:
        out.append("Fear doesn't disappear — you act anyway.")
    if "clarity" in principles:
        out.append("Clarity is an output, not a prerequisite.")
    if "self-discipline" in principles:
        out.append("Discipline compounds faster than motivation.")
    if "compassion" in principles:
        out.append("Compassion keeps ambition from turning self-destructive.")

    if not out:
        return "Act clearly, consistently — detach from results."

    return " ".join(out)


def build_steps(query, principles):
    q = query.lower()
    if "fear" in q or "fail" in q or "courage" in principles:
        return [
            "Pick 1 uncomfortable task and finish it in 48 hours.",
            "Track a single success metric. Review every 2 days.",
            "If fear spikes — do a 5-minute execution burst."
        ]

    if "confus" in q or "clarity" in principles:
        return [
            "Define 3 options. Choose 1. Run it as a 7-day experiment.",
            "Do a 10-minute nightly evidence review.",
            "Cut one distraction that drains attention."
        ]

    return [
        "Finish one meaningful task today.",
        "Start a 15-minute reflection habit.",
        "Track one metric that actually matters."
    ]


def punchline(principles, q):
    if "detachment" in principles:
        return "Aim at duty — forget the scoreboard."
    if "courage" in principles:
        return "Move. Fear is a terrible advisor."
    if "clarity" in principles:
        return "Clarity comes from doing."
    if "self-discipline" in principles:
        return "Discipline is freedom."

    return "Pick one task. Complete it. Today."


def format_advice(query, ranking):
    principles = set(ranking.keys())
    direct = infer_truth(query, principles)
    insight = gita_insight(principles)
    steps = build_steps(query, principles)
    punch = punchline(principles, query)

    sig = ", ".join([f"{p}: {round(w,3)}" for p,w in ranking.items()]) or "none"

    return f"""
Direct Truth —
{direct}

Gita Insight —
{insight}

Action Steps —
1. {steps[0]}
2. {steps[1]}
3. {steps[2]}

Punchline —
{punch}

Embedding Signals —
{sig}
"""


# ===================== INDEX BUILD / LOAD ======================
def build_or_load_index():
    meta_path = INDEX_DIR / "meta.json"
    index_path = INDEX_DIR / "index.faiss"

    if meta_path.exists() and index_path.exists():
        meta = json.load(open(meta_path, "r"))
        index = faiss.read_index(str(index_path))
        return meta, index

    docs, texts, meta = load_documents()

    print(f"Embedding {len(texts)} docs with {_backend_name}...")
    embs = embed_texts(texts)
    faiss.normalize_L2(embs)

    dim = embs.shape[1]
    index = faiss.IndexHNSWFlat(dim, 32)
    index.hnsw.efConstruction = 200
    index.add(embs)

    faiss.write_index(index, str(index_path))
    json.dump(meta, open(meta_path, "w"), indent=2)

    print("Index built.")
    return meta, index


# ========================== REPL LOOP ===========================
def chat(meta, index):
    print("Gita Advisor ready. Type 'quit' to exit.\n")

    while True:
        q = input("You> ").strip()
        if q.lower() == "quit": break
        if not q: continue

        qv = embed_query(q)
        D, I = index.search(qv, 6)

        ranking = aggregate_principles(meta, D[0], I[0], 6)
        print("\n" + format_advice(q, ranking))
        print("---\n")


if __name__ == "__main__":
    meta, index = build_or_load_index()
    chat(meta, index)
