import pandas as pd

df = pd.read_csv("./output/final_output.csv")

# Check size
print("Shape:", df.shape)

# Check columns
print("\nColumns:\n", df.columns)

# Check first rows
print("\nSample Data:\n", df.head())

# Check cluster distribution
print("\nClusters:\n", df['cluster'].value_counts())

# Check outliers
print("\nOutliers:\n", df['is_outlier'].value_counts())
