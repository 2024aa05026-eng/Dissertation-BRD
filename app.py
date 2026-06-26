import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Geospatial Outlier Detection", layout="wide")

st.title("📊 Geospatial Outlier Detection Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("./output/final_output.csv")

zip_df = pd.read_csv("./data/zip_level_dataset.csv")

st.success(f"✅ Loaded data with {len(df)} rows")

# -------------------------------
# TEMP LAT / LONG (FOR MAP)
# -------------------------------
# NOTE: Replace later with real ZIP coordinates
np.random.seed(42)
df["latitude"] = np.random.uniform(25, 49, size=len(df))
df["longitude"] = np.random.uniform(-125, -66, size=len(df))

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

cluster_filter = st.sidebar.multiselect(
    "Select Cluster",
    options=sorted(df["cluster"].dropna().unique()),
    default=sorted(df["cluster"].dropna().unique())
)

show_outliers = st.sidebar.checkbox("Show Only Outliers")

# Apply filters
filtered_df = df[df["cluster"].isin(cluster_filter)].copy()

if show_outliers:
    filtered_df = filtered_df[filtered_df["is_outlier"] == True]

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total ZIPs", len(df))
col2.metric("Clusters", df["cluster"].nunique())
col3.metric("Outliers", 0)
# col3.metric("Outliers", df["is_outlier"].sum())

# -------------------------------
# PREPARE DISPLAY VALUES
# -------------------------------
filtered_df["display_cost"] = filtered_df["Avg_Mdcr_Alowd_Amt"].round(2)
filtered_df["display_avg_cost"] = filtered_df["avg_cost"].round(2)
filtered_df["display_z"] = filtered_df["cost_zscore"].round(2)

# ✅ FIX: size must be positive
filtered_df["size_value"] = filtered_df["display_z"].abs() * 4

filtered_df["outlier_label"] = filtered_df["is_outlier"].map({
    True: "Outlier",
    False: "Normal"
})

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Map",
    "📋 Data",
    "📊 Clusters",
    "⚠️ Outliers",
    "📦 ZIP Dataset"
])

# -------------------------------
# TAB 1: MAP
# -------------------------------
with tab1:
    st.subheader("🗺️ Geographic Outliers Map")

    fig = px.scatter_geo(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="outlier_label",
        scope="usa",
        size="size_value",     # ✅ FIXED
        opacity=0.6
    )

    fig.update_layout(
        geo=dict(
            scope="usa",
            showland=True,
            landcolor="rgb(229, 229, 229)"
        )
    )

    fig.update_traces(
        hovertemplate=
        "<b>ZIP:</b> %{customdata[0]}<br>" +
        "<b>Cluster:</b> %{customdata[1]}<br>" +
        "<b>Actual Cost:</b> %{customdata[2]}<br>" +
        "<b>Expected Cost:</b> %{customdata[3]}<br>" +
        "<b>Z-score:</b> %{customdata[4]}<br>" +
        "<b>Outlier:</b> %{customdata[5]}<br>" +
        "<extra></extra>",

        customdata=filtered_df[
            ["zip", "cluster", "display_cost",
             "display_avg_cost", "display_z", "is_outlier"]
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# TAB 2: DATA TABLE
# -------------------------------
with tab2:
    st.subheader("📋 TBC..")
    # st.subheader("📋 Sample Data")

    # st.dataframe(filtered_df.sample(min(200, len(filtered_df))))

# -------------------------------
# TAB 3: CLUSTER DISTRIBUTION
# -------------------------------
with tab3:
    st.subheader("📊 Cluster Distribution")

    # ✅ Bar chart
    cluster_counts = df["cluster"].value_counts().sort_index()
    st.bar_chart(cluster_counts)

    st.markdown("---")

    # ✅ Cluster selector
    selected_cluster = st.selectbox(
        "Select Cluster to View Details",
        sorted(df["cluster"].dropna().unique())
    )

    # ✅ Filter data for selected cluster
    cluster_df = df[df["cluster"] == selected_cluster].copy()

    # ✅ Select full details columns
    cluster_df = cluster_df[
        [
            "zip",
            "Tot_Srvcs",
            "Tot_Benes",
            "Avg_Mdcr_Alowd_Amt",
            "avg_cost",
            "cost_zscore",
            "is_outlier",
            "population",
            "median_income",
            "age_65_plus",
            "pct_bachelors_plus"
        ]
    ]

    # ✅ Rename columns for readability
    cluster_df = cluster_df.rename(columns={
        "zip": "ZIP Code",
        "Tot_Srvcs": "Total Services",
        "Tot_Benes": "Total Beneficiaries",
        "Avg_Mdcr_Alowd_Amt": "Actual Cost",
        "avg_cost": "Cluster Avg Cost",
        "cost_zscore": "Z-Score",
        "is_outlier": "Outlier",
        "population": "Population",
        "median_income": "Median Income",
        "age_65_plus": "Age 65+",
        "pct_bachelors_plus": "Education %"
    })

    # ✅ Clean index
    cluster_df = cluster_df.reset_index(drop=True)

    # ✅ Display table
    st.dataframe(cluster_df, hide_index=True)

    # -------------------------------
    # ✅ BONUS: Cluster Summary
    # -------------------------------
    st.markdown("---")
    st.subheader("📈 Cluster Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total ZIPs", len(cluster_df))
    col2.metric("Avg Cost", round(cluster_df["Actual Cost"].mean(), 2))
    col3.metric("Outliers", cluster_df["Outlier"].sum())


# -------------------------------
# TAB 4: OUTLIER DISTRIBUTION
# -------------------------------
with tab4:
    st.subheader("⚠️ TBC..")
    # st.subheader("⚠️ Outlier Distribution")

    # outlier_counts = df["is_outlier"].value_counts()
    # st.bar_chart(outlier_counts)

    # st.markdown("---")

    # st.subheader("📋 Outlier List")

    # outliers_df = df[df["is_outlier"] == True].copy()

    # # ✅ Select relevant columns
    # outliers_display = outliers_df[
    #     ["zip", "cluster", "Avg_Mdcr_Alowd_Amt", "avg_cost", "cost_zscore"]
    # ]

    # # ✅ Rename columns
    # outliers_display = outliers_display.rename(columns={
    #     "zip": "ZIP Code",
    #     "cluster": "Cluster",
    #     "Avg_Mdcr_Alowd_Amt": "Actual Cost",
    #     "avg_cost": "Expected Cost",
    #     "cost_zscore": "Z-Score"
    # })

    # # ✅ 🔥 FINAL FIX: remove ALL index columns
    # outliers_display = outliers_display.reset_index(drop=True)

    # # ✅ Display clean table
    # st.dataframe(outliers_display, hide_index=True)

    # -------------------------------
# TAB 5: ZIP LEVEL DATASET
# -------------------------------
with tab5:
    st.subheader("📦 ZIP Level Dataset (Merged CMS + ACS)")

    st.markdown("""
    This dataset represents the merged and aggregated data combining:
    - CMS healthcare utilization data
    - ACS demographic data
    
    It is the foundation used for clustering and outlier detection.
    """)

    # Sample view
    st.dataframe(zip_df.sample(200), hide_index=True)

    st.markdown("---")

    # Optional: show dataset summary
    st.subheader("📊 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total ZIPs", len(zip_df))
    col2.metric("Columns", len(zip_df.columns))
    col3.metric("Avg Cost (Mean)", round(zip_df["Avg_Mdcr_Alowd_Amt"].mean(), 2))

    # Optional: download button
    csv = zip_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download ZIP Dataset",
        data=csv,
        file_name="zip_level_dataset.csv",
        mime="text/csv"
    )
