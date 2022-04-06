# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_excel(r"/Users/weilianghu/Downloads/annual_generation_state.xls")
df

# %%
new_header = df.iloc[0]  # grab the first row for the header
df = df[1:]  # take the data less the header row
df.columns = new_header  # set the header row as the df header
df

# %%
df["STATE"].unique()

# %% [markdown]
# It seems there are missing data, in addition we do not need US-total

# %%
df_missing_state = df[df["STATE"] == "  "]
df_missing_state

# %%
# Eliminate missing states and the US total
df = df[
    (df["STATE"] != "  ") & (df["STATE"] != "US-TOTAL") & (df["STATE"] != "US-Total")
]
df["STATE"].unique()

# %%
# Check for years
df["YEAR"].unique()
# There is no missing year

# %%
# Check for missing values
print(df["TYPE OF PRODUCER"].isnull().all())
print(df["ENERGY SOURCE"].isnull().all())
print(df["GENERATION (Megawatthours)"].isnull().all())

# %%
df["ENERGY SOURCE"].value_counts()

# %%
# Total is for the total energy generation for each producer
# We do not need that
df1 = df[df["ENERGY SOURCE"] != "Total"]
df1["ENERGY SOURCE"].value_counts()

# %%
df1

# %%
df2 = df1.copy()
# df2['energy_total'] = df2.groupby(['YEAR', "STATE"])['GENERATION (Megawatthours)'].transform(sum)

df2 = (
    df2.groupby(["YEAR", "STATE"])
    .agg({"GENERATION (Megawatthours)": sum})
    .reset_index()
)
df2 = df2.rename(columns={"GENERATION (Megawatthours)": "total energy generation"})
df2
# grouped_df = df.groupby('A')
# for key, item in df2:
#    print(df2.get_group(key), "\n\n")

# %%
df_clean_energy = df1[
    df1["ENERGY SOURCE"].isin(
        [
            "Other Biomass",
            "Hydroelectric Conventional",
            "Wind",
            "Solar Thermal and Photovoltaic",
            "Geothermal",
            "Pumped Storage",
        ]
    )
]
df_clean_energy

# %%
# df_clean_energy['clean_total'] = df_clean_energy.groupby(['YEAR', "STATE"], as_index = False)['GENERATION (Megawatthours)'].transform(sum)
df_clean_energy = (
    df_clean_energy.groupby(["YEAR", "STATE"])
    .agg({"GENERATION (Megawatthours)": sum})
    .reset_index()
)
df_clean_energy = df_clean_energy.rename(
    columns={"GENERATION (Megawatthours)": "clean energy generation"}
)
df_clean_energy

# %%
df_final = pd.merge(df2, df_clean_energy, on=["YEAR", "STATE"], how="left")
df_final


# %%
df_final["clean_energy_percent"] = (
    df_final["clean energy generation"] / df_final["total energy generation"]
)
df_final

# %%
df_final = df_final[df_final["STATE"] != "DC"]
df_final

# %%
df_final.to_csv("/Users/weilianghu/Downloads/clean_energy_percent_processed.csv")
