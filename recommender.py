from jobs_data import jobs
def get_recommendations(skills: list[str], level: str) -> list[dict]:
    """
    Return a sorted list of job recommendations based on user skills and level.

    Args:
        skills: A list of skill strings (already cleaned/lowercased).
        level:  One of 'beginner', 'intermediate', or 'advanced'.

    Returns:
        A list of dicts, each containing:
            - title      (str)  : job title
            - matches    (list) : skills that matched
            - count      (int)  : number of matched skills
            - total      (int)  : total skills required by the job
            - pct        (int)  : match percentage (count / total * 100)
        Sorted by count descending (best match first).
    """
    user_skills = set(s.strip().lower() for s in skills)
    level = level.strip().lower()

    recommendations = []

    for job in jobs:
        if job["level"].lower() != level:
            continue

        job_skills = [s.lower() for s in job["skills"]]
        matching = list(user_skills.intersection(set(job_skills)))

        if matching:
            total = len(job["skills"])
            count = len(matching)
            recommendations.append({
                "title":   job["title"],
                "matches": sorted(matching),
                "count":   count,
                "total":   total,
                "pct":     round(count / total * 100),
            })

    recommendations.sort(key=lambda x: x["count"], reverse=True)
    return recommendations


def format_recommendations(recommendations: list[dict]) -> str:
    """Return a human-readable string of the recommendation results."""
    if not recommendations:
        return (
            "No matches found for your current skill set and level.\n"
            "Try adding more skills or checking a different level!"
        )

    lines = [f"Found {len(recommendations)} potential match(es):\n"]
    for rec in recommendations:
        skills_found = ", ".join(rec["matches"])
        lines.append(f"  {rec['title']}")
        lines.append(
            f"    Matches: {skills_found} "
            f"({rec['count']}/{rec['total']} skills, {rec['pct']}%)\n"
        )
    return "\n".join(lines)