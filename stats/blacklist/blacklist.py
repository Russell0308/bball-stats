# Players not signed to a team #


from nba_api.stats.library import data
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import teams

import pandas as pd

players_df = pd.DataFrame(data.players)
players_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
players_df = players_df[players_df['is_active'] == True]
players_df.drop('is_active', axis=1)








