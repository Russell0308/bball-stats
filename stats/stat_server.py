import sqlite3

from flask import url_for

from stats import stat_collector as statc

from nba_api.stats.library import data
from nba_api.stats.endpoints import playerprofilev2, commonteamroster
from nba_api.stats.static import teams

from thefuzz import process

import pandas as pd

import re


players_df = pd.DataFrame(statc.get_basic_player_df())
players_df.drop('last_name', inplace=True, axis=1)
players_df.drop('first_name', inplace=True, axis=1)
players_df = players_df[players_df['is_active'] == True]
players_df.drop('is_active', inplace=True, axis=1)

def get_player_name_list():
    return players_df['full_name']


def get_teams_data():
    teams_df = pd.DataFrame(teams.get_teams())
    return teams_df


def get_player_profile(player_id):
    playerprofile = playerprofilev2.PlayerProfileV2(player_id=player_id)
    return playerprofile


def get_team_roster(team_id):
    team_roster = commonteamroster.CommonTeamRoster(team_id=team_id)
    return team_roster

def get_search_result_dash(user_query):
    full_names_list = get_player_name_list()
    names_df = pd.DataFrame(full_names_list, index=None)
    names_df.columns = ['Full_Name']

    user_search_result = process.extract(user_query, names_df['Full_Name'], limit=5)

    result_df = pd.DataFrame()
    
    user_names_result = []
    for i in user_search_result:
        user_names_result.append(i[0])
    result_df['Full_Name'] = user_names_result
    print(result_df.head)

    player_links_list = []
    player_team_abbrev_list = []
    player_number_list = []

    for i in result_df['Full_Name']:
        result_df['Link_Names'] = result_df['Full_Name'].apply(lambda x: re.sub(r'\s+', '_', x))

      #  row = search_results.loc[search_results['Full_Name'] == player_name]
        #result_df = pd.concat((result_df, row), axis=0, ignore_index=True)

        #player_row = players_df[players_df['Full_Name'] == player_name]
        #player_id = player_row['Ids'].iloc[0]

        #player_profile = get_player_profile(player_id).get_data_frames()
        #player_team_abbrev = list(player_profile[0]['TEAM_ABBREVIATION'])[-1]
        #if player_team_abbrev == 'TOT':
        #    player_team_abbrev = list(player_profile[0]['TEAM_ABBREVIATION'])[-2]
        #player_team_abbrev_list.append(player_team_abbrev)
       

        #team_df = get_teams_data()
        #team_id = team_df[team_df['abbreviation'] == player_team_abbrev]['id']

        #team_roster = get_team_roster(team_id).get_data_frames()[0]

        #player_data = team_roster[team_roster['PLAYER'] == player_name]
        #player_number = player_data['NUM']
        #print(player_number)
        #player_number = int(player_number.iloc[0])
        #player_number_list.append(player_number)
    for x, y in zip(result_df['Full_Name'], result_df['Link_Names']):
        player_links = f'''<a href=" { url_for('player_fullscreen', player_name=y) } ">{x}</a>'''
        player_links_list.append(player_links)

    result_df['Player_Link'] = player_links_list
    #result_df['Abbreviations'] = player_team_abbrev_list
    #result_df['Player_Number'] = player_number_list
    result_df.drop('Full_Name', axis=1, inplace=True)
    result_df.drop('Link_Names', axis=1, inplace=True)
        
    return result_df





