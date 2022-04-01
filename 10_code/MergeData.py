# import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def merge_data(path):
    # load data files
    weather = pd.read_csv('../00_source_data/weather.csv').drop(columns = 'Unnamed: 0')
    RPS = pd.read_csv('../00_source_data/StatesRPS.csv').drop(columns = ['Percentage', 'TargetYear'])
    coal = pd.read_csv('../00_source_data/clean_coal.csv').drop(columns = 'Unnamed: 0')
    gas = pd.read_csv('../00_source_data/clean_gas.csv').drop(columns = 'Unnamed: 0')
    petroleum = pd.read_csv('../00_source_data/petroleum price.csv')
    solar = pd.read_csv('../00_source_data/solar-pv-prices.csv')
    generation = pd.read_csv('../00_source_data/clean_energy_percent_processed.csv').drop(columns = 'Unnamed: 0')

    # clean data again before merging
    # set temporal range to 1990 - present
    petroleum = petroleum.loc[petroleum['Date'] >= 1990]
    solar = solar.loc[solar['Year'] >= 1990]

    # change column names
    coal = coal.rename(columns = {'year': 'Year', 'WPS051': 'CoalPrice'})
    solar = solar.drop(columns = ['Entity', 'Code']).rename(columns = {'Solar PV Module Cost (2019 US$ per W)': 'SolarPrice'})
    petroleum = petroleum.rename(columns = {'Date': 'Year', 'U.S. Crude Oil First Purchase Price (Dollars per Barrel)':'PetroleumPrice'})
    gas = gas.rename(columns = {'year': 'Year', '\xa0value': 'GasPrice'})
    generation = generation.rename(columns = {'YEAR':'Year', 'STATE': 'Abbreviation', 
                                          'clean energy generation': 'CleanEnergyGeneration', 
                                          'clean_energy_percent': 'CleanEnergyPercent'})

    # merge energy price into a single data frame
    energy_df = coal.merge(solar, right_on = 'Year', left_on = 'Year', how = 'left')
    energy_df = energy_df.merge(petroleum, right_on = 'Year', left_on = 'Year', how = 'left')
    energy_df = energy_df.merge(gas, right_on = 'Year', left_on = 'Year', how = 'left')

    # merge by state and year
    df = weather.merge(RPS, left_on = 'State', right_on = 'State')
    df = df.merge(energy_df, right_on = 'Year', left_on = 'Year', how = 'left')
    df = df.merge(generation, right_on = ['Year', 'Abbreviation'], left_on = ['Year', 'Abbreviation'], how = 'left')

    df.to_csv(path)