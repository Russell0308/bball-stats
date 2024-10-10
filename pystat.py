from nba_api.stats.library import data
from nba_api.stats.endpoints import playerindex

from thefuzz import process

import pandas as pd

import re


players_df = pd.DataFrame(data.players)
players_df.columns = ['Ids', 'Last_Name', 'First_Name', 'Full_Name', 'Current_Player']


def get_search_result_dash(user_query):
    search_results = players_df['Full_Name']
    search_results = pd.DataFrame(search_results, index=None)
    search_results.columns = ['Full_Name']
    search_results['Fixed_Names'] = search_results['Full_Name'].apply(lambda x: re.sub(r'\s+', '_', x))
    search_results['Full_Names_Linked'] = search_results.apply(lambda x: f'''<a href="/{x['Fixed_Names']}">{x['Full_Name']}</a>''')
    
    user_search_result = process.extract(user_query, search_results['Full_Name'], limit=10)

    result_df = pd.DataFrame()
    
    print(user_search_result)

    for i in user_search_result:
        row = search_results.loc[search_results['Full_Name'] == i[0]]
        result_df = pd.concat((result_df, row), axis=0, ignore_index=True)
        
    return result_df
get_search_result_dash('Russell')




