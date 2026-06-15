import pandas as pd


def get_cms_data(file_path):
    print("Loading CMS CSV locally...")

    # ✅ Read in chunks (important for large file)
    chunks = []

    for chunk in pd.read_csv(file_path, chunksize=50000):
        chunks.append(chunk)

    df = pd.concat(chunks, ignore_index=True)

    print("✅ CMS Data Loaded:", df.shape)

    return df


def prepare_cms(df):

    if df.empty:
        print("⚠️ Empty CMS dataset")
        return df

    df = df.copy()

    if "Rndrng_Prvdr_Zip5" in df.columns:
        df["Rndrng_Prvdr_Zip5"] = df["Rndrng_Prvdr_Zip5"].astype(str).str[:5]

    numeric_cols = [
        "Tot_Srvcs",
        "Tot_Benes",
        "Avg_Mdcr_Alowd_Amt"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
