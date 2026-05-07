import streamlit as st
from jobs_data import jobs

from logic import get_recommendations 

st.title("🚀 SkillBridge: Job Recommender")


skills_input = st.text_input("Enter your skills (comma separated):")
level_input = st.selectbox("Select your level:", ["Beginner", "Intermediate", "Advanced"])

if st.button("Find Jobs"):
    # Convert input string to list
    user_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
    
    
    results = get_recommendations(user_skills, level_input)
    
    
    if not results:
        st.warning("No matches found. Try adding more skills!")
    else:
        st.success(f"Found {len(results)} potential match(es):")
        for rec in results:
            with st.expander(f"✅ {rec['title']} ({rec['pct']}%)"):
                st.write(f"**Matched Skills:** {', '.join(rec['matches'])}")
                st.write(f"**Coverage:** {rec['count']} out of {rec['total']} required skills.")