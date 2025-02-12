import urllib.request
import pandas as pd
from fuzzywuzzy import fuzz, process


csv_url = "https://raw.githubusercontent.com/ewattudo/gradschoolcam/main/csv_files/CMGR%20All%20Fall%20Apps%20by%20Program%20-%2056-2025-02-11-18-59-13%20(1).csv"
urllib.request.urlretrieve(csv_url, "orig.csv")


columns_to_keep = [
    "Admissions Status →", "Started App", "Submitted App", "Complete App", "In Review", 
    "Admit", "Admit-Coming", "Admit-Not Coming", "Admit-Withdrawn", 
    "Deferred to Spring", "Withdrawn", "Conditional Admission", 
    "Alternative Admission", "Denied", "Total"
]

data = pd.read_csv("orig.csv", skiprows=12, usecols=columns_to_keep)


data["Admissions Status →"] = data["Admissions Status →"].astype(str).fillna("Unknown")


data["Natural"] = data["Admissions Status →"].str.split(":").str[0].str.split("-").str[0].str.strip()

# Function to group similar names using fuzzy matching
def group_similar_values(values, threshold=85):
    """Groups similar values into a dictionary using fuzzy matching."""
    grouped_values = {}
    
    for val in values:
        best_match, score = process.extractOne(val, grouped_values.keys(), scorer=fuzz.ratio) or (None, 0)
        
        if best_match is None or score < threshold:
            grouped_values[val] = val  # Create new group
        else:
            grouped_values[val] = best_match  # Merge into existing group

    return grouped_values


program_mapping = group_similar_values(data["Natural"])


data["Grouped Program"] = data["Natural"].map(program_mapping)


numeric_cols = columns_to_keep[1:]
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors="coerce")

grouped_df = data.groupby("Grouped Program", as_index=False)[numeric_cols].sum()


df = grouped_df.melt(id_vars=["Grouped Program"], var_name="Category", value_name="Count")


df.rename(columns={"Grouped Program": "Natural"}, inplace=True)
df = df[["Natural", "Category", "Count"]]


print(df.head(20))

df["Natural"] = df["Natural"].str.split(":").str[0].str.split("-").str[0].str.strip()

program_groups = {
    "Biology": ["Biology", "Biology (MS)", "Biology (NOD)"],
    "Business & Science": ["Bus and Sci", "Business and Science"],
    "Chemistry": ["Chemistry", "Chemistry (MS)", "Chemistry and Molecular Technology (MS)"],
    "Childhood Studies": ["Childhood Studies (MA)", "Childhood Studies (NOD)"],
    "Computer Science": ["Computer Science"],
    "Criminal Justice": ["Criminal Justice (MA)"],
    "Data Science": ["Data Science (MS)"],
    "English": ["English (MA)", "English (NOD)"],
    "Forensic Science": ["Forensic Science (MS)"],
    "Emerging Media": ["Emerging Media (MA)"],
    "Creative Writing": ["Creative Writing (MFA) Camden"],
}


program_mapping = {}
for key, values in program_groups.items():
    for v in values:
        program_mapping[v] = key


df["Natural"] = df["Natural"].replace(program_mapping)


numeric_cols = df.columns[1:]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")


df_grouped = df.groupby("Natural", as_index=False)[numeric_cols].sum()


print(df_grouped)
