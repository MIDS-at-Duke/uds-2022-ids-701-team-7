import pandas as pd


# clean coal price data
coal = pd.read_csv("./00_source_data/coal price.csv")
coal["year"] = coal["observation_date"].str[:4].astype(int)
coal = coal[(coal["year"] >= 1990) & (coal["year"] <= 2020)].copy()
coal_yearly = coal.groupby(["year"], as_index=False).mean()
coal_yearly.to_csv("./20_intermediate_files/clean_coal.csv")


# clean natural gas data
gas = pd.read_csv("./00_source_data/natural gas price.csv")
gas["year"] = gas["date"].str[:4].astype(int)
gas_yearly = gas.groupby(["year"], as_index=False).mean()
gas_yearly.to_csv("./20_intermediate_files/clean_gas.csv")
