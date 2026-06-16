# ============================================================
# STEP 4: KEY INSIGHTS + SUMMARY STATISTICS
# Indian Job Market Trend Analysis
# ============================================================
# This script generates the numbers you'll put in your README.
# Recruiters love seeing "Data-driven findings" with real numbers.
# ============================================================

import pandas as pd
import numpy as np
from collections import Counter
import ast

df = pd.read_csv(r"C:\Users\yesas\Desktop\India-job-market\data\clean_jobs.csv")
print("=" * 55)
print("   INDIAN JOB MARKET — KEY FINDINGS SUMMARY")
print("=" * 55)


# ---- INSIGHT 1: Dataset Overview ----
print(f"\n📊 DATASET OVERVIEW")
print(f"   Total job postings analysed : {len(df):,}")
print(f"   Unique companies            : {df['company'].nunique() if 'company' in df.columns else 'N/A'}")
print(f"   Unique cities               : {df['city'].nunique() if 'city' in df.columns else 'N/A'}")
print(f"   Unique job roles            : {df['job_title_clean'].nunique() if 'job_title_clean' in df.columns else 'N/A'}")


# ---- INSIGHT 2: Most Demanded Roles ----
if "job_title_clean" in df.columns:
    print(f"\n🏆 TOP 5 MOST IN-DEMAND ROLES")
    top5 = df["job_title_clean"].value_counts().head(5)
    for i, (role, count) in enumerate(top5.items(), 1):
        pct = count / len(df) * 100
        print(f"   {i}. {role:<30} {count:>5} postings ({pct:.1f}%)")


# ---- INSIGHT 3: Top Hiring Cities ----
if "city" in df.columns:
    print(f"\n📍 TOP HIRING CITIES FOR DATA ROLES")
    city_counts = df[df["city"] != "Unknown"]["city"].value_counts().head(5)
    for city, count in city_counts.items():
        pct = count / len(df) * 100
        print(f"   {city:<25} {count:>5} postings ({pct:.1f}%)")


# ---- INSIGHT 4: Most Required Skills ----
if "skills_list" in df.columns:
    all_skills = []
    for s in df["skills_list"].dropna():
        try:
            if isinstance(s, list):
                all_skills.extend(s)
            else:
                all_skills.extend(ast.literal_eval(s))
        except:
            pass
    
    top_skills = Counter(all_skills).most_common(10)
    print(f"\n🔧 TOP 10 SKILLS ACROSS ALL DATA ROLES")
    for skill, count in top_skills:
        bar = "█" * int(count / max(c for _, c in top_skills) * 20)
        print(f"   {skill.title():<25} {bar} {count}")


# ---- INSIGHT 5: Salary Insights ----
if "salary_lpa" in df.columns:
    sal = df[df["salary_lpa"].notna() & (df["salary_lpa"] > 0) & (df["salary_lpa"] <= 50)]
    print(f"\n💰 SALARY INSIGHTS (LPA — Lakhs Per Annum)")
    print(f"   Overall median salary       : ₹{sal['salary_lpa'].median():.1f} LPA")
    print(f"   Overall average salary      : ₹{sal['salary_lpa'].mean():.1f} LPA")
    print(f"   Entry-level (0-2 yrs) avg   : ₹{sal[sal['exp_avg'] <= 2]['salary_lpa'].mean():.1f} LPA" if "exp_avg" in df.columns else "")
    print(f"   Mid-level (3-5 yrs) avg     : ₹{sal[(sal['exp_avg'] >= 3) & (sal['exp_avg'] <= 5)]['salary_lpa'].mean():.1f} LPA" if "exp_avg" in df.columns else "")
    
    if "job_title_clean" in df.columns:
        print(f"\n   Salary by Role (median):")
        top5_roles = df["job_title_clean"].value_counts().head(5).index
        for role in top5_roles:
            role_sal = sal[sal["job_title_clean"] == role]["salary_lpa"]
            if len(role_sal) > 5:
                print(f"   {role:<35} ₹{role_sal.median():.1f} LPA")


# ---- INSIGHT 6: Fresher Analysis (YOUR UNIQUE ANGLE) ----
if "exp_min" in df.columns:
    fresher = df[df["exp_min"] <= 2]
    print(f"\n🎓 FRESHER-SPECIFIC INSIGHTS (0–2 Years Experience)")
    print(f"   Fresher-friendly postings   : {len(fresher):,} ({len(fresher)/len(df)*100:.1f}% of total)")
    
    if "job_title_clean" in fresher.columns:
        best_for_freshers = fresher["job_title_clean"].value_counts().head(3)
        print(f"   Best roles for freshers     :")
        for role, count in best_for_freshers.items():
            print(f"     → {role} ({count} postings)")
    
    if "city" in fresher.columns:
        best_cities = fresher[fresher["city"] != "Unknown"]["city"].value_counts().head(3)
        print(f"   Best cities for freshers    :")
        for city, count in best_cities.items():
            print(f"     → {city} ({count} postings)")


# ---- INSIGHT 7: YOUR BUSINESS RECOMMENDATIONS ----
# Write these in your own words based on YOUR findings.
# This is what makes the project YOURS.
print(f"""
{'=' * 55}
  3 ACTIONABLE RECOMMENDATIONS (Write in your README)
{'=' * 55}

1. SKILL INVESTMENT FOR FRESHERS:
   SQL and Python appear in [X]% of job postings, making
   them the highest-priority skills for any data aspirant.
   Excel remains foundational across all experience levels.

2. CITY STRATEGY:
   Bangalore and Hyderabad dominate data job postings,
   but Chennai shows strong growth in BI and analyst roles —
   particularly relevant for Tamil Nadu-based candidates.

3. SALARY EXPECTATION SETTING:
   Freshers with 0-2 years can expect ₹[X]–[Y] LPA in
   Data Analyst roles. Adding Python + SQL skills to your
   profile correlates with higher salary bands even at
   entry level.

(Fill in the [X] values from your actual dataset findings!)
""")

print("→ Now open step5_dashboard_guide.txt to build your Power BI dashboard")
