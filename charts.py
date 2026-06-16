# ============================================================
# STEP 3: ANALYSIS + VISUALIZATIONS
# Indian Job Market Trend Analysis
# ============================================================
# This is the most visible part — screenshots from here go 
# into your README and impress recruiters the most.
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ---- LOAD CLEAN DATA ----
df = pd.read_csv(r"C:\Users\yesas\Desktop\India-job-market\data\clean_jobs.csv")
print(f"✓ Loaded clean data: {df.shape}")

# ---- STYLE SETUP ----
# A consistent visual style makes your project look professional
plt.rcParams.update({
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor":   "#FAFAFA",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.titlesize":    14,
    "axes.titleweight":  "bold",
    "axes.titlepad":     12,
    "axes.labelsize":    11,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "font.family":       "DejaVu Sans",
})
PALETTE = ["#1D9E75", "#534AB7", "#D85A30", "#BA7517", "#185FA5",
           "#A32D2D", "#3B6D11", "#D4537E", "#888780", "#0F6E56"]


# ============================================================
# CHART 1: Top 10 Job Roles by Count
# ============================================================

if "job_title_clean" in df.columns:
    top_roles = df["job_title_clean"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top_roles.index[::-1], top_roles.values[::-1],
                   color=PALETTE[0], edgecolor="none")
    
    # Add count labels at end of each bar
    for bar, val in zip(bars, top_roles.values[::-1]):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
                f"{val:,}", va="center", fontsize=10, color="#444")
    
    ax.set_title("Top 10 Most In-Demand Job Roles in India")
    ax.set_xlabel("Number of Job Postings")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(r"C:\Users\yesas\Desktop\India-job-market\visuals\chart1_top_roles.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Chart 1 saved: top roles")


# ============================================================
# CHART 2: Top Skills Required (Word Frequency)
# ============================================================

if "skills_list" in df.columns:
    # Flatten all skills lists into one big list
    all_skills = []
    for skill_list in df["skills_list"].dropna():
        if isinstance(skill_list, list):
            all_skills.extend(skill_list)
        elif isinstance(skill_list, str):
            # Handle case where it was saved as string representation
            import ast
            try:
                all_skills.extend(ast.literal_eval(skill_list))
            except:
                pass

    skill_counts = Counter(all_skills).most_common(15)
    skills_df = pd.DataFrame(skill_counts, columns=["skill", "count"])
    skills_df["skill"] = skills_df["skill"].str.title()

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [PALETTE[0] if i < 5 else PALETTE[1] if i < 10 else PALETTE[2]
              for i in range(len(skills_df))]
    bars = ax.bar(skills_df["skill"], skills_df["count"],
                  color=colors, edgecolor="none")
    
    ax.set_title("Most In-Demand Skills Across All Data Roles")
    ax.set_xlabel("")
    ax.set_ylabel("Frequency in Job Postings")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(r"C:\Users\yesas\Desktop\India-job-market\visuals\chart2_top_skills.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Chart 2 saved: top skills")


# ============================================================
# CHART 3: City-wise Job Distribution
# ============================================================

if "city" in df.columns:
    city_counts = df[df["city"] != "Unknown"]["city"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(9, 6))
    wedges, texts, autotexts = ax.pie(
        city_counts.values,
        labels=city_counts.index,
        autopct="%1.1f%%",
        colors=PALETTE[:len(city_counts)],
        startangle=140,
        pctdistance=0.82,
        wedgeprops={"linewidth": 1.5, "edgecolor": "white"}
    )
    for text in autotexts:
        text.set_fontsize(9)
    ax.set_title("City-wise Distribution of Data Job Postings")
    plt.tight_layout()
    plt.savefig(r"C:\Users\yesas\Desktop\India-job-market\visuals\chart3_city_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Chart 3 saved: city distribution")


# ============================================================
# CHART 4: Experience Required by Role (Box Plot)
# ============================================================

if "exp_avg" in df.columns and "job_title_clean" in df.columns:
    # Focus on top 6 roles for clarity
    top6 = df["job_title_clean"].value_counts().head(6).index
    df_exp = df[df["job_title_clean"].isin(top6) & df["exp_avg"].notna()]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create box plot data
    data_by_role = [df_exp[df_exp["job_title_clean"] == role]["exp_avg"].values
                    for role in top6]
    
    bp = ax.boxplot(data_by_role, tick_labels=top6, patch_artist=True, notch=False,
                    medianprops={"color": "white", "linewidth": 2})
    
    for patch, color in zip(bp["boxes"], PALETTE[:6]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_title("Experience Required by Role (Years)")
    ax.set_ylabel("Years of Experience")
    ax.set_xlabel("")
    plt.xticks(rotation=20, ha="right")
    
    # Add "Fresher Friendly" annotation for roles with low median
    for i, role in enumerate(top6, 1):
        med = df_exp[df_exp["job_title_clean"] == role]["exp_avg"].median()
        if med <= 1.5:
            ax.annotate("Fresher\nFriendly", xy=(i, med),
                        xytext=(i + 0.3, med + 0.5),
                        fontsize=8, color=PALETTE[0],
                        arrowprops={"arrowstyle": "->", "color": PALETTE[0]})
    
    plt.tight_layout()
    plt.savefig(r"C:\Users\yesas\Desktop\India-job-market\visuals\chart4_experience_by_role.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Chart 4 saved: experience by role")


# ============================================================
# CHART 5: Salary Distribution by Role (YOUR UNIQUE ANGLE)
# Fresher-focused: Compare entry-level vs mid-level salaries
# ============================================================

if "salary_lpa" in df.columns and "job_title_clean" in df.columns:
    # Only rows with salary data
    df_sal = df[df["salary_lpa"].notna() & df["salary_lpa"] > 0]
    # Remove outliers (salary > 50 LPA is likely data error for fresh grads)
    df_sal = df_sal[df_sal["salary_lpa"] <= 50]
    
    top5 = df_sal["job_title_clean"].value_counts().head(5).index
    df_sal5 = df_sal[df_sal["job_title_clean"].isin(top5)]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, role in enumerate(top5):
        data = df_sal5[df_sal5["job_title_clean"] == role]["salary_lpa"]
        ax.scatter([i + 1] * len(data), data, alpha=0.3, s=20,
                   color=PALETTE[i], label=role)
        ax.plot([i + 0.7, i + 1.3], [data.median(), data.median()],
                color=PALETTE[i], linewidth=2.5)
        ax.text(i + 1, data.median() + 0.3, f"₹{data.median():.1f}L",
                ha="center", fontsize=9, fontweight="bold", color=PALETTE[i])
    
    ax.set_xticks(range(1, len(top5) + 1))
    ax.set_xticklabels(top5, rotation=15, ha="right")
    ax.set_ylabel("Salary (LPA)")
    ax.set_title("Salary Distribution by Role (Lines = Median)")
    ax.set_ylim(0, df_sal5["salary_lpa"].quantile(0.95) + 2)
    plt.tight_layout()
    plt.savefig(r"C:\Users\yesas\Desktop\India-job-market\visuals\chart5_salary_by_role.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Chart 5 saved: salary distribution")


# ============================================================
# CHART 6: FRESHER-FRIENDLY ROLES (Your Unique Angle)
# Roles where 0-2 years experience postings are most common
# ============================================================

if "exp_min" in df.columns and "job_title_clean" in df.columns:
    fresher_df = df[df["exp_min"] <= 2]
    fresher_counts = fresher_df["job_title_clean"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [PALETTE[0] if v > fresher_counts.median() else PALETTE[-1]
              for v in fresher_counts.values]
    bars = ax.barh(fresher_counts.index[::-1], fresher_counts.values[::-1],
                   color=colors[::-1], edgecolor="none")
    
    for bar, val in zip(bars, fresher_counts.values[::-1]):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=10, color="#444")
    
    ax.set_title("Best Entry-Level / Fresher-Friendly Roles (0–2 Years Experience)")
    ax.set_xlabel("Number of Job Postings")
    ax.axvline(x=fresher_counts.median(), linestyle="--",
               color="#888", linewidth=1, label=f"Median = {fresher_counts.median():.0f}")
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(r"C:\Users\yesas\Desktop\India-job-market\visuals\chart6_fresher_roles.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Chart 6 saved: fresher-friendly roles")

print("\n✓ All charts saved to /visuals/ folder!")
print("→ Move to step4_insights.py to write your summary stats")
