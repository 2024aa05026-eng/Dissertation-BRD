import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_clustering(df):
    features = ["population", "median_income", "age_65_plus", "pct_bachelors_plus"]

    df_clean = df[features].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    df.loc[df_clean.index, "cluster"] = clusters

    print("✅ Clustering done")
    return df


def run_subclustering(df):
    features = ["population", "median_income", "age_65_plus", "pct_bachelors_plus"]
    scaler = StandardScaler()

    df["sub_cluster"] = None

    for cl in df["cluster"].dropna().unique():
        subset = df[df["cluster"] == cl].dropna(subset=features)

        if len(subset) < 50:
            continue

        X_sub = scaler.fit_transform(subset[features])

        kmeans_sub = KMeans(n_clusters=2, random_state=42, n_init=10)
        labels = kmeans_sub.fit_predict(X_sub)

        df.loc[subset.index, "sub_cluster"] = [
            f"{int(cl)}_{int(l)}" for l in labels
        ]

    print("✅ Sub-clustering done")
    return df