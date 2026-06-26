import numpy as np

def detect_outliers(df):

    # Calculate std per cluster
    std = df.groupby("cluster")["Avg_Mdcr_Alowd_Amt"].transform("std")

    # Avoid divide-by-zero
    std = std.replace(0, 1)

    df["cost_zscore"] = (
        (df["Avg_Mdcr_Alowd_Amt"] - df["avg_cost"]) / std
    )

    df["is_outlier"] = df["cost_zscore"].abs() > 2

    print("✅ Outlier detection done")
    return df


def add_explanation(df):

    def explain(row):
        if row["cost_zscore"] > 2:
            return "High cost vs cluster"
        elif row["cost_zscore"] < -2:
            return "Low cost vs cluster"
        else:
            return "Normal"

    df["explanation"] = df.apply(explain, axis=1)

    print("✅ Explainability added")
    return df