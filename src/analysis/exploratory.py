import polars as pl
import matplotlib.pyplot as plt

df = pl.read_csv("data/survey_data.csv")
df = df.filter(pl.col("year") == 2024)
df = df.with_columns(pl.col("LIKERT.AGE").fill_null("No Response"))
df = df.with_columns(pl.col("LIKERT.AGE").replace("Prefer not say", "No Response"))

df["LIKERT.CONTRIBUTOR_TYPE.CONTRIBUTE_CODE"].value_counts()
df["POSNEG.FUTURE_CONTRIBUTION_LIKELIHOOD"].value_counts()
df["POSNEG.OSS_IDENTIFICATION"].value_counts()
df["MULT.EMPLOYMENT_STATUS"].value_counts()
