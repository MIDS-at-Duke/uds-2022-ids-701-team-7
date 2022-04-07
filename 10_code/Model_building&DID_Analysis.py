# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_csv(
    "/Users/weilianghu/Downloads/uds-2022-ids-701-team-7/20_intermediate_files/Energy_Final.csv"
)
df

# get the states we analyze
df1 = df.copy()
df_with_useState = df1[
    df1["State"].isin(
        [
            "CO",
            "HI",
            "MD",
            "NY",
            "RI",
            "DE",
            "MT",
            "WA",
            "IL",
            "NH",
            "NC",
            "OR",
            "MI",
            "MO",
            "OH",
            "AK",
            "AL",
            "AR",
            "FL",
            "GA",
            "ID",
            "KY",
            "LA",
            "MS",
            "NE",
            "TN",
            "UT",
            "VA",
            "WV",
            "WY",
        ]
    )
]
df_fin = df_with_useState[
    (
        df_with_useState["Year"].isin(
            [2000, 2001, 2002, 2003, 2012, 2013, 2014, 2015, 2016]
        )
    )
]
df_fin["Year"].value_counts()


# subset for the states with policy change
df_fin["treated"] = np.where(
    df_fin["State"].isin(
        [
            "CO",
            "HI",
            "MD",
            "NY",
            "RI",
            "DE",
            "MT",
            "WA",
            "IL",
            "NH",
            "NC",
            "OR",
            "MI",
            "MO",
            "OH",
        ]
    ),
    1,
    0,
)
df_fin

# post treatment period
df_fin["post_treatment"] = np.where(df_fin["Year"] >= 2012, 1, 0)
df_fin

# two way fixed effects models
df_multiindex = df_fin.set_index(["State", "Year"])
from linearmodels import PanelOLS

mod = PanelOLS.from_formula(
    "CO2 ~ treated * post_treatment + Average_Temp + Percipitation + CoalPrice + NaturalGasPrice + PetroleumPrice + EntityEffects + TimeEffects",
    data=df_multiindex,
    drop_absorbed=True,
)
mod.fit(cov_type="clustered", cluster_entity=True)

# one way fixed effects model
df_multiindex = df_fin.set_index(["State", df_fin.index])
from linearmodels import PanelOLS

mod = PanelOLS.from_formula(
    "CO2 ~ treated * post_treatment + Average_Temp + Percipitation + CoalPrice + NaturalGasPrice + PetroleumPrice + EntityEffects",
    data=df_multiindex,
    drop_absorbed=True,
)
mod.fit(cov_type="clustered", cluster_entity=True)

# %%
import altair as alt


# %%
df_fin[df_fin["Enacted"] == "None"]["StateName"].unique()


# %%
import pathlib

# Where to save files
path_prefix = f"/Users/weilianghu/Downloads/uds-2022-ids-701-team-7/30_results"

# Diff-in-Diff analysis in IL
df1 = df.copy()
data = df1[df1["State"].isin(["IL", "AR", "LA", "KY"])]
data = data[
    (
        data["Year"].isin(
            [
                2000,
                2001,
                2002,
                2003,
                2004,
                2005,
                2006,
                2011,
                2012,
                2013,
                2014,
                2015,
                2016,
                2017,
                2018,
            ]
        )
    )
]

data["treated"] = np.where(data["State"] == "IL", 1, 0)
data["post_treatment"] = np.where(data["Year"] > 2007, 1, 0)

grouped_means = data.groupby(["treated", "Year"], as_index=False)[["CO2"]].mean()
scatter = (
    alt.Chart(grouped_means)
    .mark_point()
    .encode(
        x=alt.X(
            "Year:Q", scale=alt.Scale(zero=False), title="Year, policy enacted in 2007"
        ),
        y=alt.Y("CO2:Q", scale=alt.Scale(zero=False), title="CO2(million metric tons)"),
        color="treated:N",
    )
).properties(
    title="CO2 generation in Illinois before and after 2007 (Policy Enactment)"
)

df_t = df1.copy()
df_t["enact"] = 2007

loesses = []
colors = {0: "lightblue", 1: "orange"}
for t, p in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    c = (
        alt.Chart(data[(data["treated"] == t) & (data["post_treatment"] == p)])
        .encode(
            x=alt.X("Year:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("CO2:Q", scale=alt.Scale(zero=False)),
        )
        .transform_regression("Year", "CO2")
        .mark_line(color=colors[t])
    )
    loesses.append(c)

rule = (
    alt.Chart(df_t)
    .mark_rule(color="green", strokeDash=[15, 15])
    .encode(
        x="enact:Q",
    )
)

IL_fin = alt.layer(*loesses, scatter) + rule
IL_fin.save(f"{path_prefix}IL.png")
IL_fin


# Diff-in-Diff analysis in UT
df1 = df.copy()
data = df1[df1["State"].isin(["UT", "ID", "WY", "NE"])]
data = data[
    (
        data["Year"].isin(
            [
                2000,
                2001,
                2002,
                2003,
                2004,
                2005,
                2006,
                2007,
                2011,
                2012,
                2013,
                2014,
                2015,
                2016,
                2017,
                2018,
            ]
        )
    )
]

data["treated"] = np.where(data["State"] == "UT", 1, 0)
data["post_treatment"] = np.where(data["Year"] > 2008, 1, 0)

grouped_means = data.groupby(["treated", "Year"], as_index=False)[["CO2"]].mean()
scatter = (
    alt.Chart(grouped_means)
    .mark_point()
    .encode(
        x=alt.X(
            "Year:Q", scale=alt.Scale(zero=False), title="Year, policy enacted in 2008"
        ),
        y=alt.Y("CO2:Q", scale=alt.Scale(zero=False), title="CO2(million metric tons)"),
        color="treated:N",
    )
).properties(title="CO2 generation in Utah before and after 2008 (Policy Enactment)")

df_t = df1.copy()
df_t["enact"] = 2008

loesses = []
colors = {0: "lightblue", 1: "orange"}
for t, p in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    c = (
        alt.Chart(data[(data["treated"] == t) & (data["post_treatment"] == p)])
        .encode(
            x=alt.X("Year:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("CO2:Q", scale=alt.Scale(zero=False)),
        )
        .transform_regression("Year", "CO2")
        .mark_line(color=colors[t])
    )
    loesses.append(c)

rule = (
    alt.Chart(df_t)
    .mark_rule(color="green", strokeDash=[15, 15])
    .encode(
        x="enact:Q",
    )
)

UT_fin = alt.layer(*loesses, scatter) + rule
UT_fin.save(f"{path_prefix}UT.png")
UT_fin

# Diff-in-Diff analysis in NC
df1 = df.copy()
data = df1[df1["State"].isin(["NC", "GA", "FL", "VA"])]
data = data[
    (
        data["Year"].isin(
            [
                2000,
                2001,
                2002,
                2003,
                2004,
                2005,
                2006,
                2011,
                2012,
                2013,
                2014,
                2015,
                2016,
                2017,
                2018,
            ]
        )
    )
]

data["treated"] = np.where(data["State"] == "NC", 1, 0)
data["post_treatment"] = np.where(data["Year"] > 2007, 1, 0)

grouped_means = data.groupby(["treated", "Year"], as_index=False)[["CO2"]].mean()
scatter = (
    alt.Chart(grouped_means)
    .mark_point()
    .encode(
        x=alt.X(
            "Year:Q", scale=alt.Scale(zero=False), title="Year, policy enacted in 2007"
        ),
        y=alt.Y("CO2:Q", scale=alt.Scale(zero=False), title="CO2(million metric tons)"),
        color="treated:N",
    )
).properties(
    title="CO2 generation in North Carolina before and after 2007 (Policy Enactment)"
)

df_t = df1.copy()
df_t["enact"] = 2007

loesses = []
colors = {0: "lightblue", 1: "orange"}
for t, p in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    c = (
        alt.Chart(data[(data["treated"] == t) & (data["post_treatment"] == p)])
        .encode(
            x=alt.X("Year:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("CO2:Q", scale=alt.Scale(zero=False)),
        )
        .transform_regression("Year", "CO2")
        .mark_line(color=colors[t])
    )
    loesses.append(c)

rule = (
    alt.Chart(df_t)
    .mark_rule(color="green", strokeDash=[15, 15])
    .encode(
        x="enact:Q",
    )
)

NC_fin = alt.layer(*loesses, scatter) + rule
NC_fin.save(f"{path_prefix}NC.png")
NC_fin


# Diff-in-Diff analysis in NY

df1 = df.copy()
data = df1[df1["State"].isin(["NY", "WV", "KY", "TN"])]
data = data[
    (
        data["Year"].isin(
            [
                2000,
                2001,
                2002,
                2003,
                2010,
                2011,
                2012,
                2013,
                2014,
                2015,
                2016,
                2017,
                2018,
            ]
        )
    )
]

data["treated"] = np.where(data["State"] == "NY", 1, 0)
data["post_treatment"] = np.where(data["Year"] > 2004, 1, 0)

grouped_means = data.groupby(["treated", "Year"], as_index=False)[["CO2"]].mean()
scatter = (
    alt.Chart(grouped_means)
    .mark_point()
    .encode(
        x=alt.X(
            "Year:Q", scale=alt.Scale(zero=False), title="Year, policy enacted in 2004"
        ),
        y=alt.Y("CO2:Q", scale=alt.Scale(zero=False), title="CO2(million metric tons)"),
        color="treated:N",
        # title = "CO2 generation in New York before and after 2004 (Policy Enactment)",
    )
).properties(
    title="CO2 generation in New York before and after 2004 (Policy Enactment)"
)

df_t = df1.copy()
df_t["enact"] = 2004

loesses = []
colors = {0: "lightblue", 1: "orange"}
for t, p in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    c = (
        alt.Chart(data[(data["treated"] == t) & (data["post_treatment"] == p)])
        .encode(
            x=alt.X("Year:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("CO2:Q", scale=alt.Scale(zero=False)),
        )
        .transform_regression("Year", "CO2")
        .mark_line(color=colors[t])
    )
    loesses.append(c)

rule = (
    alt.Chart(df_t)
    .mark_rule(color="green", strokeDash=[15, 15])
    .encode(
        x="enact:Q",
    )
)

NY_fin = alt.layer(*loesses, scatter) + rule

NY_fin.save(f"{path_prefix}NY.png")
NY_fin


# %%
