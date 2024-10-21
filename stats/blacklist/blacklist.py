# Players not signed to a team #

from thefuzz import process

from nba_api.stats.library import data
from nba_api.stats.endpoints import commonteamroster, playerprofilev2
from nba_api.stats.static import teams

import pandas as pd

query = 'Shai'

players_df = pd.DataFrame(data.players)
players_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
players_df = players_df[players_df['is_active'] == True]
players_df.drop('is_active', axis=1)


search_list = process.extract(query, players_df['full_name'], limit=5)

player_name = search_list[0][0]
player_row = players_df[players_df['full_name'] == player_name]
player_id = player_row['ids'].iloc[0]

playerprofile = playerprofilev2.PlayerProfileV2(player_id=player_id).get_data_frames()[0]

print(playerprofile.head)


teams_df = pd.DataFrame(teams.get_teams())

#team_roster = commonteamroster.CommonTeamRoster(team_id).get_data_frames()






