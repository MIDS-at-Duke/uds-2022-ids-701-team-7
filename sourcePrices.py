import requests
import pandas as pd
import numpy as np
states = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ];
# states = ['AL']
dataframe = pd.DataFrame()
for state in states:
    coal = requests.get("https://api.eia.gov/series/?api_key={}&series_id=SEDS.CLTCD.{}.A".format(apikey, state))
    coal = coal.json()
    naturalGas = requests.get("https://api.eia.gov/series/?api_key={}&series_id=SEDS.NGTCD.{}.A".format(apikey, state))
    naturalGas = naturalGas.json()
    nuclear = requests.get("https://api.eia.gov/series/?api_key={}&series_id=SEDS.NUETD.{}.A".format(apikey, state))
    nuclear = nuclear.json()
    petroleum = requests.get("https://api.eia.gov/series/?api_key={}&series_id=SEDS.PATCD.{}.A".format(apikey, state))
    petroleum = petroleum.json()
    coal = pd.DataFrame(coal['series'][0]['data'], columns=['year', 'coal'])
    naturalGas = pd.DataFrame(naturalGas['series'][0]['data'], columns=['year', 'naturalGas'])
    nuclear = pd.DataFrame(nuclear['series'][0]['data'], columns=['year', 'nuclear'])
    petroleum = pd.DataFrame(petroleum['series'][0]['data'], columns=['year', 'petroleum'])
    merge1 = pd.merge(coal, naturalGas,  how='left', left_on=['year',], right_on = ['year'])
    merge2 = pd.merge(merge1, nuclear,  how='left', left_on=['year',], right_on = ['year'])
    final = pd.merge(merge2, petroleum,  how='left', left_on=['year',], right_on = ['year'])
    final['State'] = [state]*len(final['year'])
    dataframe = pd.concat([dataframe, final])