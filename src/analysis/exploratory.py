import polars as pl
import matplotlib.pyplot as plt

df = pl.read_csv("data/survey_data.csv")
df = df.filter(pl.col("year") == 2024)
df = df.with_columns(pl.col("LIKERT.AGE").fill_null("No Response"))
df = df.with_columns(pl.col("LIKERT.AGE").replace("Prefer not say", "No Response"))
age_df = df["LIKERT.AGE"].value_counts()

age_df = age_df.sort("LIKERT.AGE")
age_df = age_df.filter(pl.col("LIKERT.AGE") != "No Response")


fig, ax = plt.subplots()

bg_color = "#2d2d2d"
fig.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.barh(age_df["LIKERT.AGE"], age_df["count"], color="#A4BED5")
ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
ax.tick_params(size=0, labelcolor="white")
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
    ax.text(x=value + adjustment, y=i, s=f"{value}", va="center", color=color, ha=ha)

text_style = dict(color="white", va="top", size=5)
fig.text(
    x=0.9, y=0.8, s="Age repartition of respondants", ha="right", size=16, color="white"
)
fig.text(x=0.1, y=0.1, s="The Open Source Survey - 2024", **text_style)
fig.text(
    x=0.9, y=0.1, s="Data: Github\nGraph: Joseph Barbier", ha="right", **text_style
)

fig.savefig("img/age-repartition.png", dpi=300, bbox_inches="tight")
