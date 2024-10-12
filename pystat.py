from flask import url_for

from nba_api.stats.library import data
from nba_api.stats.endpoints import playerindex

from thefuzz import process

import pandas as pd

import re


players_df = pd.DataFrame(data.players)
players_df.columns = ['Ids', 'Last_Name', 'First_Name', 'Full_Name', 'Current_Player']


def get_player_name_list():
    return players_df['Full_Name']


def get_search_result_dash(user_query):
    search_results = players_df['Full_Name']
    search_results = pd.DataFrame(search_results, index=None)
    search_results.columns = ['Full_Name']
    search_results['Link_Names'] = search_results['Full_Name'].apply(lambda x: re.sub(r'\s+', '_', x))

    player_links_list = []
    for x, y in zip(search_results['Full_Name'], search_results['Link_Names']):
        player_links = f'''<a href=" { url_for('player_fullscreen', player_name={y}) } ">{x}</a>'''
        player_links_list.append(player_links)

    search_results['player_links'] = player_links_list
    
    user_search_result = process.extract(user_query, search_results['Full_Name'], limit=10)

    result_df = pd.DataFrame()
    
    print(user_search_result)

    for i in user_search_result:
        row = search_results.loc[search_results['Full_Name'] == i[0]]
        result_df = pd.concat((result_df, row), axis=0, ignore_index=True)
        
    return result_df




