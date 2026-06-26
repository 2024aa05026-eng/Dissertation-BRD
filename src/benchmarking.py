def compute_cluster_benchmarks(df):

    cluster_stats = df.groupby("cluster").agg({
        "Tot_Srvcs": "mean",
        "Tot_Benes": "mean",
        "Avg_Mdcr_Alowd_Amt": "mean"
    }).rename(columns={
        "Tot_Srvcs": "avg_services",
        "Tot_Benes": "avg_benes",
        "Avg_Mdcr_Alowd_Amt": "avg_cost"
    }).reset_index()

    df = df.merge(cluster_stats, on="cluster", how="left")

    print("✅ Benchmarking done")
    return df