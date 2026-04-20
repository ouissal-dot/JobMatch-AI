import streamlit as st
from jobs_data import jobs

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="JobMatch AI",
    page_icon="💼",
    layout="centered",
)

# ── Header ─────────────────────────────────────────────────────────
st.title("💼 JobMatch AI")
st.markdown("Find jobs that match your skills and experience level.")
st.divider()

# ── Collect ALL unique skills from the dataset ──────────────────────
all_skills = sorted({s.lower() for job in jobs for s in job["skills"]})

# ── Inputs ─────────────────────────────────────────────────────────
selected_skills = st.multiselect(
    "🛠️ Select your skills",
    options=all_skills,
    placeholder="Start typing or choose from the list…",
)

level = st.selectbox(
    "📊 Your experience level",
    options=["beginner", "intermediate", "advanced"],
    index=0,
)

# ── Search button ───────────────────────────────────────────────────
search = st.button("🔍 Find Jobs", use_container_width=True, type="primary")

# ── Results ─────────────────────────────────────────────────────────
if search:
    if not selected_skills:
        st.warning("Please select at least one skill before searching.")
    else:
        user_skills = set(s.lower() for s in selected_skills)
        results = []

        for job in jobs:
            if job["level"].lower() != level:
                continue
            job_skills = {s.lower() for s in job["skills"]}
            matches = sorted(user_skills & job_skills)
            if matches:
                total = len(job["skills"])
                count = len(matches)
                results.append({
                    "title":   job["title"],
                    "matches": matches,
                    "count":   count,
                    "total":   total,
                    "pct":     round(count / total * 100),
                    "missing": sorted(job_skills - user_skills),
                })

        results.sort(key=lambda x: x["count"], reverse=True)

        st.divider()

        if not results:
            st.error("😕 No matches found for your skills and level.")
            st.info("Try selecting more skills or switching your experience level.")
        else:
            st.success(f"✅ Found **{len(results)}** matching job(s) for **{level}** level")

            for r in results:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(r["title"])
                    with col2:
                        st.metric("Match", f"{r['pct']}%")

                    st.progress(r["pct"] / 100)

                    # Matched skills
                    st.markdown("**✅ Your matching skills:**")
                    st.markdown(" ".join(
                        f"`{s}`" for s in r["matches"]
                    ))

                    # Missing skills
                    if r["missing"]:
                        st.markdown("**📚 Skills to learn:**")
                        st.markdown(" ".join(
                            f"`{s}`" for s in r["missing"]
                        ))
