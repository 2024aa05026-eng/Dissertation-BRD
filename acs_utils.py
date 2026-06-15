# acs_utils.py

import pandas as pd
import requests

API_KEY = "dbab6b581c27ab9af365ece85131d192b9e1e00e"
ACS_BASE = "https://api.census.gov/data/2022/acs/acs5"


def fetch_acs_data(variables):
    url = f"{ACS_BASE}?get=NAME,{','.join(variables)}&for=zip%20code%20tabulation%20area:*&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data[1:], columns=data[0])
    return df


# -------------------------------
# AGE DATA (B01001)
# -------------------------------
def get_age_data():
    vars_age = [
        "B01001_020E", "B01001_021E", "B01001_022E",
        "B01001_023E", "B01001_024E",
        "B01001_044E", "B01001_045E",
        "B01001_046E", "B01001_047E", "B01001_048E"
    ]
    df = fetch_acs_data(vars_age)

    for col in vars_age:
        df[col] = pd.to_numeric(df[col])

    df["age_65_plus"] = df[vars_age].sum(axis=1)

    return df[["zip code tabulation area", "age_65_plus"]]


# -------------------------------
# INCOME DATA (B19013)
# -------------------------------
def get_income_data():
    df = fetch_acs_data(["B19013_001E"])
    df["B19013_001E"] = pd.to_numeric(df["B19013_001E"])

    df.rename(columns={"B19013_001E": "median_income"}, inplace=True)

    return df[["zip code tabulation area", "median_income"]]


# -------------------------------
# POPULATION (B01003)
# -------------------------------
def get_population_data():
    df = fetch_acs_data(["B01003_001E"])
    df["B01003_001E"] = pd.to_numeric(df["B01003_001E"])

    df.rename(columns={"B01003_001E": "population"}, inplace=True)

    return df[["zip code tabulation area", "population"]]


# -------------------------------
# EDUCATION (B15003)
# -------------------------------
def get_education_data():
    vars_edu = [
        "B15003_001E",
        "B15003_017E", "B15003_018E",
        "B15003_019E", "B15003_020E"
    ]

    df = fetch_acs_data(vars_edu)

    for col in vars_edu:
        df[col] = pd.to_numeric(df[col])

    df["bachelors_plus"] = (
        df["B15003_017E"] +
        df["B15003_018E"] +
        df["B15003_019E"] +
        df["B15003_020E"]
    )

    df["pct_bachelors_plus"] = df["bachelors_plus"] / df["B15003_001E"]

    return df[["zip code tabulation area", "pct_bachelors_plus"]]


# -------------------------------
# MERGE ALL ACS
# -------------------------------
def build_acs_features():
    age = get_age_data()
    income = get_income_data()
    pop = get_population_data()
    edu = get_education_data()

    df = age.merge(income, on="zip code tabulation area")
    df = df.merge(pop, on="zip code tabulation area")
    df = df.merge(edu, on="zip code tabulation area")

    df.rename(columns={"zip code tabulation area": "zip"}, inplace=True)

    return df