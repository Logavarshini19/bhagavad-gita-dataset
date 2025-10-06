import streamlit as st
import pandas as pd
from gita_advisor import GitaAdvisor

# Configure the app
st.set_page_config(
    page_title="Bhagavad Gita AI Advisor",
    page_icon="🕉️",
    layout="wide"
)

# Initialize advisor
@st.cache_resource
def load_advisor():
    return GitaAdvisor("bhagavad-gita-populated.ttl")

advisor = load_advisor()

# App header
st.title("🕉️ Bhagavad Gita AI Advisor")
st.markdown("""
Get personalized guidance from the timeless wisdom of the Bhagavad Gita using AI and Semantic Reasoning.
""")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Describe Your Situation")
    user_query = st.text_area(
        "What challenge or question are you facing?",
        placeholder="e.g., I'm feeling anxious about my career decisions and confused about my duties...",
        height=100
    )
    
    if st.button("Get Guidance", type="primary"):
        if user_query.strip():
            with st.spinner("Consulting the Bhagavad Gita..."):
                result = advisor.get_advice(user_query)
            
            st.subheader("🎯 Guidance")
            st.write(result['advice'])
            
            st.subheader("🔍 How This Guidance Was Derived")
            st.write(result['explanation'])
            
            st.subheader("📖 Relevant Verses")
            st.write(f"Verses referenced: {', '.join(result['relevant_verses'])}")
            
            st.subheader("🏛️ Philosophical Concepts Applied")
            concepts = result['concepts_used']
            if concepts['themes']:
                st.write(f"Themes: {', '.join(concepts['themes'])}")
            if concepts['frameworks']:
                st.write(f"Frameworks: {', '.join(concepts['frameworks'])}")
            if concepts['emotions']:
                st.write(f"Emotions addressed: {', '.join(concepts['emotions'])}")
                
        else:
            st.warning("Please describe your situation to get guidance.")

with col2:
    st.subheader("Quick Guidance")
    
    common_scenarios = {
        "Work Stress": "Feeling overwhelmed with work responsibilities",
        "Life Purpose": "Searching for meaning and direction in life", 
        "Relationship Conflict": "Dealing with difficult relationships",
        "Decision Making": "Facing a tough ethical decision",
        "Fear & Anxiety": "Managing fear and anxiety about future",
        "Leadership Challenge": "Leading others through difficult times"
    }
    
    for scenario, query in common_scenarios.items():
        if st.button(scenario):
            st.session_state.quick_query = query
    
    if 'quick_query' in st.session_state:
        st.text_area("Edit your query:", value=st.session_state.quick_query, key="quick_query_box")
        if st.button("Get Guidance for This"):
            with st.spinner("Consulting the Bhagavad Gita..."):
                result = advisor.get_advice(st.session_state.quick_query)
            
            st.subheader("Guidance")
            st.write(result['advice'])

# Footer
st.markdown("---")
st.markdown("""
**About this App**: This AI advisor uses Semantic Web technologies and a structured knowledge graph of the Bhagavad Gita to provide interpretable, philosophically-grounded guidance.
""")