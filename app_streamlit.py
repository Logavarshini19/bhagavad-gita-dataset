import streamlit as st
import quick_retriever as qr
import faiss

st.set_page_config(page_title="Gita Advisor", page_icon="🕉️", layout="centered")

# safe lookup for aggregate-principle function (handles name mismatch)
def _find_aggregate_fn(module):
    # common expected name
    if hasattr(module, "aggregate_principles_from_matches"):
        return getattr(module, "aggregate_principles_from_matches")
    # fall back: find any exported function with 'aggregate' and 'principle' in its name
    for name in dir(module):
        lname = name.lower()
        if "aggregate" in lname and "principle" in lname:
            fn = getattr(module, name)
            if callable(fn):
                return fn
    return None

aggregate_fn = _find_aggregate_fn(qr)
if aggregate_fn is None:
    raise ImportError("Could not find an aggregate_principles function in quick_retriever.py. "
                      "Expected 'aggregate_principles_from_matches' or similar.")

@st.cache_resource
def get_index_and_meta():
    meta, index = qr.build_or_load_index()
    return meta, index

st.title("Gita Advisor — Spiritual Mentor")
st.caption("Brutally honest, Gita‑inspired guidance. Ask in English (or request Tamil/Sanskrit).")

meta, index = get_index_and_meta()

with st.form("query_form", clear_on_submit=False):
    query = st.text_area("Your question", height=140, placeholder="e.g. I'm anxious about a career decision...")
    top_k = st.slider("Retrieval top-K", min_value=3, max_value=12, value=6)
    show_signals = st.checkbox("Show embedding signals / match metadata", value=True)
    submit = st.form_submit_button("Ask the Advisor")

if submit:
    if not query.strip():
        st.warning("Type a question first.")
    else:
        with st.spinner("Thinking like a strict mentor..."):
            q_vec = qr.embed_query(query)
            D, I = index.search(q_vec, top_k)
            sims = D[0].tolist()
            ids = I[0].tolist()
            principle_ranking = aggregate_fn(meta, sims, ids, top_k)
            advice = qr.format_advice(query, principle_ranking)

        st.markdown("## Advisor")
        st.markdown(f"```\n{advice}\n```")

        if show_signals:
            st.markdown("### Embedding signals (top matches)")
            rows = []
            for sim, idx in zip(sims, ids):
                m = meta[idx]
                rows.append({
                    "similarity": round(float(sim), 4),
                    "speaker": m.get("speaker"),
                    "tags": ", ".join(m.get("tags", [])) if m.get("tags") else "",
                    "certainty": m.get("certainty_score", "")
                })
            st.table(rows)

        st.markdown("---")
        st.caption("Tip: for Tamil/Sanskrit outputs, ask explicitly in your question.")