# ============================================================
# STEP 2: DATA CLEANING
# Indian Job Market Trend Analysis
# ============================================================
# This is the most important step. Clean data = clean analysis.
# Every recruiter knows messy data is real — show you can handle it.
# ============================================================

import pandas as pd
import numpy as np
import re

# ---- LOAD RAW DATA ----
df = pd.read_csv(r"C:\Users\yesas\Desktop\India-job-market\data\raw_jobs.csv.csv")
print(f"Raw data shape: {df.shape}")

# ============================================================
# STEP 2A: UNDERSTAND YOUR DATA FIRST
# Run this block and read the output carefully before cleaning.
# ============================================================

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- SAMPLE VALUES per column ---")
for col in df.columns:
    print(f"\n{col}: {df[col].dropna().unique()[:5]}")


# ============================================================
# STEP 2B: STANDARDIZE COLUMN NAMES
# Rename columns to something consistent and lowercase.
# Adjust the mapping below based on YOUR dataset's actual column names.
# ============================================================

# --- ADJUST THIS MAPPING to match your CSV's actual column names ---
column_mapping = {
    # "Original Name in CSV"  : "new_clean_name"
    "Job Title"               : "job_title",
    "Location"                : "location",
    "Industry"                : "industry",
    "Key Skills"              : "skills",
    "Role Category"           : "role_category",
    "Functional Area"         : "functional_area",
    "Job Experience Required"              : "experience_raw",
    "Job Salary"                  : "salary_raw",
    "Role"                    : "role"      
}

# Only rename columns that exist in your dataframe
cols_present = {k: v for k, v in column_mapping.items() if k in df.columns}
df = df.rename(columns=cols_present)
print(f"\n✓ Renamed {len(cols_present)} columns")


# ============================================================
# STEP 2C: CLEAN JOB TITLES
# Standardize "Data Analyst", "data analyst", "Data analyst" → same
# ============================================================

def clean_job_title(title):
    if pd.isna(title):
        return None
    title = str(title).strip().lower()
    # Standardize common variations
    if "data analyst" in title:
        return "Data Analyst"
    elif "business analyst" in title:
        return "Business Analyst"
    elif "data scientist" in title:
        return "Data Scientist"
    elif "data engineer" in title:
        return "Data Engineer"
    elif "machine learning" in title or "ml engineer" in title:
        return "ML Engineer"
    elif "python" in title and "developer" in title:
        return "Python Developer"
    elif "sql" in title:
        return "SQL Analyst"
    elif "tableau" in title or "power bi" in title:
        return "BI Analyst"
    else:
        return title.title()  # Title case everything else

if "job_title" in df.columns:
    df["job_title_clean"] = df["job_title"].apply(clean_job_title)
    print(f"\n✓ Top 10 job titles after cleaning:")
    print(df["job_title_clean"].value_counts().head(10))


# ============================================================
# STEP 2D: EXTRACT EXPERIENCE (in years)
# Convert "2-5 Yrs" or "3 to 7 Years" → numeric min/max
# ============================================================

def extract_experience(exp_str):
    """Returns (min_exp, max_exp) tuple in years."""
    if pd.isna(exp_str):
        return None, None
    exp_str = str(exp_str).lower()
    numbers = re.findall(r'\d+\.?\d*', exp_str)
    if len(numbers) >= 2:
        return float(numbers[0]), float(numbers[1])
    elif len(numbers) == 1:
        return float(numbers[0]), float(numbers[0])
    elif "fresher" in exp_str or "0" in exp_str:
        return 0.0, 1.0
    return None, None

if "experience_raw" in df.columns:
    df[["exp_min", "exp_max"]] = df["experience_raw"].apply(
        lambda x: pd.Series(extract_experience(x))
    )
    df["exp_avg"] = (df["exp_min"] + df["exp_max"]) / 2
    print(f"\n✓ Experience range: {df['exp_min'].min()} to {df['exp_max'].max()} years")


# ============================================================
# STEP 2E: EXTRACT SALARY (in LPA)
# Convert "3,00,000 - 5,00,000 PA" or "3-5 Lacs" → numeric
# ============================================================

def extract_salary_lpa(salary_str):
    """Returns average salary in Lakhs Per Annum (LPA)."""
    if pd.isna(salary_str):
        return None
    s = str(salary_str).lower().replace(",", "")
    
    # Already in lakhs format: "3-5 lacs" or "3.5-6 lpa"
    if "lac" in s or "lpa" in s or "lakh" in s:
        numbers = re.findall(r'\d+\.?\d*', s)
        if len(numbers) >= 2:
            return (float(numbers[0]) + float(numbers[1])) / 2
        elif len(numbers) == 1:
            return float(numbers[0])
    
    # In rupees format: "300000 - 600000"
    numbers = re.findall(r'\d+\.?\d*', s)
    if len(numbers) >= 2:
        avg = (float(numbers[0]) + float(numbers[1])) / 2
        return round(avg / 100000, 2)  # Convert to LPA
    elif len(numbers) == 1:
        return round(float(numbers[0]) / 100000, 2)
    
    return None

if "salary_raw" in df.columns:
    df["salary_lpa"] = df["salary_raw"].apply(extract_salary_lpa)
    df_with_salary = df[df["salary_lpa"].notna()]
    print(f"\n✓ Salary extracted for {len(df_with_salary)} rows")
    print(f"   Average salary: ₹{df['salary_lpa'].mean():.1f} LPA")


# ============================================================
# STEP 2F: CLEAN LOCATION → EXTRACT CITY
# "Chennai, Tamil Nadu" → "Chennai"
# ============================================================

MAJOR_CITIES = [
    "chennai", "hyderabad", "bangalore", "bengaluru", "mumbai",
    "delhi", "pune", "kolkata", "ahmedabad", "noida", "gurugram",
    "gurgaon", "coimbatore", "kochi", "thiruvananthapuram", "vizag",
    "visakhapatnam", "vijayawada", "tirupati"
]

def extract_city(location_str):
    if pd.isna(location_str):
        return "Unknown"
    loc = str(location_str).lower()
    for city in MAJOR_CITIES:
        if city in loc:
            # Normalize
            if city == "bengaluru":
                return "Bangalore"
            if city == "gurgaon":
                return "Gurugram"
            if city == "vizag" or city == "visakhapatnam":
                return "Vizag"
            return city.title()
    # Check for "Remote"
    if "remote" in loc:
        return "Remote"
    return "Other"

if "location" in df.columns:
    df["city"] = df["location"].apply(extract_city)
    print(f"\n✓ Top cities in dataset:")
    print(df["city"].value_counts().head(10))


# ============================================================
# STEP 2G: EXTRACT SKILLS from job descriptions
# Build a skills column by checking for keyword presence
# ============================================================

SKILL_KEYWORDS = [
    "python", "sql", "excel", "power bi", "tableau", "r",
    "machine learning", "statistics", "data visualization",
    "pandas", "numpy", "spark", "hadoop", "mysql", "postgresql",
    "looker", "google analytics", "sas", "spss", "nlp", "deep learning"
]

def extract_skills_list(text):
    """Return list of found skills from a text blob."""
    if pd.isna(text):
        return []
    text = str(text).lower()
    found = [skill for skill in SKILL_KEYWORDS if skill in text]
    return found

# Apply to skills column OR description column (whichever exists)
skill_source = "skills" if "skills" in df.columns else "description"
if skill_source in df.columns:
    df["skills_list"] = df[skill_source].apply(extract_skills_list)
    df["skill_count"] = df["skills_list"].apply(len)
    print(f"\n✓ Skills extracted from '{skill_source}' column")


# ============================================================
# STEP 2H: HANDLE MISSING VALUES
# ============================================================

print(f"\n--- MISSING VALUES BEFORE CLEANUP ---")
print(df.isnull().sum())

# Drop rows where ALL key fields are missing
df = df.dropna(how="all")

# Fill missing cities
if "city" in df.columns:
    df["city"] = df["city"].fillna("Unknown")

# Fill missing experience with median
if "exp_avg" in df.columns:
    median_exp = df["exp_avg"].median()
    df["exp_avg"] = df["exp_avg"].fillna(median_exp)

print(f"\n--- MISSING VALUES AFTER CLEANUP ---")
print(df.isnull().sum())


# ============================================================
# STEP 2I: REMOVE DUPLICATES
# ============================================================

before = len(df)
df = df.drop_duplicates(subset=["job_title", "location"], keep="first")
after = len(df)
print(f"\n✓ Removed {before - after} duplicate rows. Remaining: {after}")


# ============================================================
# STEP 2J: SAVE CLEAN DATA
# ============================================================

clean_path = r"C:\Users\yesas\Desktop\India-job-market\data\clean_jobs.csv"
df.to_csv(clean_path, index=False)
print(f"\n✓ Clean data saved to: {clean_path}")
print(f"Final shape: {df.shape}")
print("\n→ Move to step3_analysis.py")
