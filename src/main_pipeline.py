import pandas as pd
import os

from clustering import run_clustering, run_subclustering
from benchmarking import compute_cluster_benchmarks
from outlier_detection import detect_outliers, add_explanation


def main():

    print("🚀 Starting pipeline...")

    # Load data
    df = pd.read_csv("../data/zip_level_dataset.csv")

    print(f"✅ Data loaded: {df.shape}")

    # STEP 1: Clustering
    df = run_clustering(df)

    # STEP 2: Sub-clustering
    df = run_subclustering(df)

    # STEP 3: Benchmarking
    df = compute_cluster_benchmarks(df)

    # STEP 4: Outlier detection
    df = detect_outliers(df)

    # STEP 5: Explainability
    df = add_explanation(df)

    # Save output
    os.makedirs("../output", exist_ok=True)
    df.to_csv("../output/final_output.csv", index=False)

    print("🎯 PIPELINE COMPLETED!")
    print("📁 Output saved to output/final_output.csv")


if __name__ == "__main__":
    main()