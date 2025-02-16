import polars as pl
import matplotlib.pyplot as plt

from analysis import theme

df = pl.read_csv("data/survey_data.csv")
df = df.filter(pl.col("year") == 2024)
df = df.with_columns(pl.col("LIKERT.AGE").fill_null("No Response"))
df = df.with_columns(pl.col("LIKERT.AGE").replace("Prefer not say", "No Response"))
age_df = df["LIKERT.AGE"].value_counts()

n_noresponse = age_df.row(by_predicate=(pl.col("LIKERT.AGE") == "No Response"))[1]
noresponse_rate = n_noresponse / len(df) * 100

age_df = age_df.sort("LIKERT.AGE")
age_df = age_df.filter(pl.col("LIKERT.AGE") != "No Response")

theme.theme_opensource()

fig, ax = plt.subplots()

ax.barh(age_df["LIKERT.AGE"], age_df["count"], height=0.7)
ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
ax.tick_params(size=0, labelcolor="white", labelsize=7)
ax.set_xticks([])

for i, row in enumerate(age_df.iter_rows()):
    value = row[1]
    if value > 100:
        adjustment = -50
        color = "black"
        ha = "right"
    else:
        adjustment = 20
        color = "white"
        ha = "left"
    ax.text(
        x=value + adjustment,
        y=i,
        s=f"{value}",
        va="center",
        color=color,
        ha=ha,
        size=9,
    )

fig.text(
    x=0.9, y=0.8, s="Age repartition of respondants", ha="right", size=16, color="white"
)
fig.text(
    x=0.9,
    y=0.75,
    s=f"Note: no data for {noresponse_rate:.1f}% of respondents",
    ha="right",
    size=8,
    color="#838282",
)

text_style = dict(
    color="#f0f0f0",
    va="top",
    size=5,
    y=0.1,
)
fig.text(
    x=0.9,
    s="The Open Source Survey - 2024\nData by Github. Graph by Joseph Barbier",
    ha="right",
    **text_style,
)

fig.savefig("img/age-repartition.png", dpi=300, bbox_inches="tight")
