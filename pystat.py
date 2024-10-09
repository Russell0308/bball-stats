from nba_api.stats.library import data
from nba_api.stats.endpoints import playerindex

from thefuzz import process

import pandas as pd


players_df = pd.DataFrame(data.players)
players_df.columns = ['Ids', 'Last_Name', 'First_Name', 'Full_Name', 'Current_Player']


def get_search_result_dash(user_query):
    search_results = players_df['Full_Name']
    search_results = pd.DataFrame(search_results, index=None)
    search_results.columns = ['Full_Name']
    search_results['Full_Name_Links'] = search_results['Full_Name'].apply(lambda x: f'<a href="/{x}">{x}</a>')
    
    user_search_result = process.extract(user_query, search_results['Full_Name'], limit=10)

    result_df = pd.DataFrame()

    for i in user_search_result:
        row = search_results.loc[i]
        print(row)
        result_df = pd.concat((result_df, row), axis=0, ignore_index=True)
        
    return result_df
get_search_result_dash('Russell')




