import sqlite3

from flask import url_for

from stats import stat_collector as statc

from thefuzz import process

import pandas as pd

import re


players_df = pd.DataFrame(statc.get_basic_player_df())
players_df.drop('last_name', inplace=True, axis=1)
players_df.drop('first_name', inplace=True, axis=1)
players_df = players_df[players_df['is_active'] == True]
players_df.drop('is_active', inplace=True, axis=1)


def get_search_result_dash(user_query):
    user_search_result = process.extract(user_query, players_df['full_name'], limit=5)

    result_df = pd.DataFrame()

    user_names_result = []
    for i in user_search_result:
        user_names_result.append(i[0])
    result_df['full_name'] = user_names_result

    player_links_list = []
    player_team_abbrev_list = []
    player_number_list = []

    for i in result_df['full_name']:
        result_df['link_names'] = result_df['full_name'].apply(lambda x: re.sub(r'\s+', '_', x))
        player_name = i

        player_row = players_df[players_df['full_name'] == player_name]
        player_id = player_row['ids'].iloc[0]

        player_profile = statc.get_player_profile_df(player_id)
        player_team_abbrev = list(player_profile['TEAM_ABBREVIATION'])[-1]
        if player_team_abbrev == 'TOT':
            player_team_abbrev = list(player_profile['TEAM_ABBREVIATION'])[-2]
        player_team_abbrev_list.append(player_team_abbrev)
       
        team_df = statc.get_teams_df()
        team_id = team_df[team_df['abbreviation'] == player_team_abbrev]['id']

        team_roster = statc.get_teamroster_df(team_id)

        player_data = team_roster[team_roster['PLAYER'] == player_name]

        if player_data.empty == True:
            print('not in league anymore')
        
        player_number = player_data['NUM']
        print(player_number)
        #player_number = int(player_number.iloc[0])
        #player_number_list.append(player_number)

    for x, y in zip(result_df['full_name'], result_df['link_names']):
        player_links = f'''<a href=" { url_for('player_fullscreen', player_name=y) } ">{x}</a>'''
        player_links_list.append(player_links)

    result_df['player_link'] = player_links_list
    result_df['Abbreviations'] = player_team_abbrev_list
    #result_df['Player_Number'] = player_number_list
    result_df.drop('full_name', axis=1, inplace=True)
    result_df.drop('link_names', axis=1, inplace=True)
        
    return result_df





