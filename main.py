# main.py

import pandas as pd

from acs_utils import build_acs_features
from cms_utils import get_cms_data, prepare_cms


# =============================
# STEP 1: FETCH ACS DATA
# =============================
print("Fetching ACS Data...")
acs_df = build_acs_features()
print("✅ ACS loaded:", acs_df.shape)


# =============================
# STEP 2: FETCH CMS DATA
# =============================
print("\nFetching CMS Data...")

# cms_df = get_cms_data(batch_size=10)   # ✅ safe batch size
cms_df = get_cms_data("CMS_data/cms_data.csv")
cms_df = prepare_cms(cms_df)

print("✅ CMS loaded:", cms_df.shape)


# ✅ Safety check (VERY IMPORTANT)
if cms_df.empty:
    print("❌ CMS data fetch failed — stopping pipeline")
    exit()


# =============================
# STEP 3: MERGE CMS + ACS
# =============================
print("\nMerging datasets...")

merged = cms_df.merge(
    acs_df,
    left_on="Rndrng_Prvdr_Zip5",
    right_on="zip",
    how="left"
)

print("✅ Merged dataset:", merged.shape)


# =============================
# STEP 4: CREATE ZIP-LEVEL DATASET
# =============================
print("\nCreating ZIP-level dataset...")

zip_df = merged.groupby("zip").agg({
    "Tot_Srvcs": "sum",
    "Tot_Benes": "sum",
    "Avg_Mdcr_Alowd_Amt": "mean",
    "age_65_plus": "first",
    "median_income": "first",
    "population": "first",
    "pct_bachelors_plus": "first"
}).reset_index()

print("✅ ZIP-level dataset created:", zip_df.shape)


# =============================
# STEP 5: SAVE OUTPUT
# =============================
zip_df.to_csv("zip_level_dataset.csv", index=False)
print("✅ Dataset saved as zip_level_dataset.csv")


# =============================
# OPTIONAL: CLUSTERING (KEEP DISABLED FOR NOW)
# =============================
"""
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("\nStarting clustering...")

features = zip_df[[
    "age_65_plus",
    "median_income",
    "population",
    "pct_bachelors_plus"
]].dropna()

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(features)

# Apply clustering
kmeans = KMeans(n_clusters=5, random_state=42)
zip_df.loc[features.index, "cluster"] = kmeans.fit_predict(X)

zip_df.to_csv("zip_clustered.csv", index=False)

print("✅ Clustering complete and saved as zip_clustered.csv")
"""