import sqlite3

from nba_api.stats.endpoints import playerprofilev2, commonteamroster, playerawards
from nba_api.stats.static import teams, players

#from stats import stat_server

import pandas as pd

import os


# Basic player data

def create_basic_player_data_csv():
    # Does file exist?
    if os.path.isfile('./stats/CSVs/basic_player_data.csv') == True:
        pass
    else:                     # Create file
        basic_player_df = pd.DataFrame(players.get_active_players())   
        basic_player_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
        basic_player_df.to_csv('./stats/CSVs/basic_player_data.csv', index=False)


def get_basic_player_df():
    '''
    Gets (id, last name, first name, full name, activity)
    '''
    create_basic_player_data_csv()
    update_basic_player_df()
    df = pd.read_csv('./stats/CSVs/basic_player_data.csv')
    
    return df


def get_player_number(player_id):
    team_id = get_players_team_id(player_id)
    
    teamroster = get_teamroster_df(team_id)

    players_row = teamroster[teamroster['PLAYER_ID'] == player_id]

    try: 
        number = players_row['NUM'].iloc[0]
        number = int(number)
    except Exception:
        return Exception
    return number


def update_basic_player_df():
    location = './stats/CSVs/basic_player_data.csv'
    
    basic_player_df = pd.DataFrame(players.get_active_players())
    basic_player_df.columns = ['ids', 'full_name', 'first_name', 'last_name', 'is_active']

    basic_player_df.to_csv(location, index=False)


# Team ID
def get_players_team_id(player_id):
    player_profile = get_player_profile_df(player_id, 'Next Game')
    players_team_id = player_profile['PLAYER_TEAM_ID'].iloc[0]
    return players_team_id


# Player Profile data
data_names_list = ['Career Totals Regular Season by Year', 'Career Totals Regular Season', 'Career Totals Post Season by Year', 'Career Totals Post Season', 'Career Totals All-Star Games by Year', 'Career Totals All-Star Games', 'Career Totals College by Year', 'Career Totals College', 'Career Totals Preseason by Year', 'Career Totals Preseason', 'Career Rankings by Year', 'Career Playoff Ranking by Year', 'Season Highs', 'Career Highs', 'Next Game']

def create_player_profile_csv(player_id):
    player_profile_list = playerprofilev2.PlayerProfileV2(player_id=player_id).get_data_frames()

    for x, i in zip(data_names_list, player_profile_list):
        df = pd.DataFrame(i)
        if os.path.isdir(f'./stats/CSVs/playerprofiles/{player_id}') == True:
            pass
        else:
            print(os.getcwd())
            os.mkdir(f'./stats/CSVs/playerprofiles/{player_id}')


        df.to_csv(f'./stats/CSVs/playerprofiles/{player_id}/{x}.csv')


def get_player_profile_df(player_id, df_name):
    try:
        create_player_profile_csv(player_id)  # works as an update csv

    except Exception: 
        print(Exception)

    df = pd.read_csv(f'./stats/CSVs/playerprofiles/{player_id}/{df_name}.csv')


    return df


# Team Roster
def create_team_roster_csv(team_id):
    if os.path.isfile(f'./stats/CSVs/teamrosters/{team_id}.csv') == True:
        pass
    else:
        team_roster_df = pd.DataFrame(commonteamroster.CommonTeamRoster(team_id).get_data_frames()[0])
        team_roster_df.to_csv(f'./stats/CSVs/teamrosters/{team_id}.csv', index=False)


def get_teamroster_df(team_id):
    create_team_roster_csv(team_id)

    df = pd.read_csv(f'./stats/CSVs/teamrosters/{team_id}.csv')

    return df


# Basic Team data
def create_teams_data_csv():
    if os.path.isfile('./stats/CSVs/teams_data.csv') == True:
        pass
    else:
        teams_df = pd.DataFrame(teams.get_teams())
        teams_df.to_csv('./stats/CSVs/teams_data.csv')


def get_teams_df():
    create_teams_data_csv()

    teams_df = pd.read_csv('./stats/CSVs/teams_data.csv')

    return teams_df


# Search results data
def create_search_csv(df):
    if os.path.exists('./stats/CSVs/search.csv'):
        try: 
            orig_df = pd.read_csv('./stats/CSVs/search.csv')
        except Exception:
            print(Exception)

        for x in df['full_name']: 
            match = 0
            try: 
                for j in orig_df['full_name']:
                    if x == j:
                        match += 1
                        pass
            except Exception:
                print(Exception)
            if match == 0:
                add_list = x

        for i in add_list:
            row = df[df['full_name']]
            row_df = pd.DataFrame(row)
            row_df.to_csv('./stats/CSVs/search.csv', mode='a')


def get_search_csv(names):
    df = pd.read_csv('./stats/CSVs/search.csv')   

    fin_df = pd.DataFrame()
    for i in names:
        for j in df['full_name']:
            if j == i:
                fin_df[i] = df[df['full_name'] == j]

    print(fin_df.head)
    return fin_df
                


    



# Player awards
def create_player_awards_csv(player_id):
    df = playerawards.PlayerAwards(player_id=player_id).get_data_frames()[0]

    df.to_csv(f'./stats/CSVs/playerprofiles/{player_id}/awards.csv')


def get_player_awards_df(player_id):
    create_player_awards_csv(player_id)
    
    df = pd.read_csv(f'./stats/CSVs/playerprofiles/{player_id}/awards.csv')

    return df

































