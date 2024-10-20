import sqlite3

from nba_api.stats.library import data
from nba_api.stats.endpoints import playerprofilev2, commonteamroster
from nba_api.stats.static import teams

import pandas as pd

import os


def create_basic_player_data_csv():
    # Does file exist?
    if os.path.isfile('./stats/CSVs/basic_player_data.csv') == True:
        pass
    else:                     # Create file
        basic_player_df = pd.DataFrame(data.players)   
        basic_player_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
        basic_player_df.to_csv('./stats/CSVs/basic_player_data.csv', index=False)


def get_basic_player_df():
    '''
    Gets (id, last name, first name, full name, activity)
    '''
    create_basic_player_data_csv()

    df = pd.read_csv('./stats/CSVs/basic_player_data.csv')

    

    return df


#def update_basic_player_df():
#    location = './stats/CSVs/basic_player_data.csv'
#    
#    basic_player_df = pd.DataFrame(data.players)
#    basic_player_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
#
#    basic_player_df.to_csv(location, index=False)


def create_basic_teams_csv():
    if os.path.isfile('./stats/CSVs/basic_teams.csv') == True:
        pass
    else:
        basic_teams_df = pd.DataFrame(teams.get_teams())    
        basic_teams_df.to_csv('./stats/CSVs/basic_teams.csv', index=False)


def get_teams_df():
    create_basic_teams_csv()
    
    df = pd.read_csv('./stats/CSVs/basic_teams.csv')
    
    return df


def create_player_profile_csv(player_id):
    if os.path.isfile(f'./stats/CSVs/playerprofiles/{player_id}.csv') == True:
        pass
    else:
        try:
            player_profile_df = pd.DataFrame(playerprofilev2.PlayerProfileV2(player_id=player_id).get_data_frames()[0])
            player_profile_df.to_csv(f'./stats/CSVs/playerprofiles/{player_id}.csv', index=False)
        except:
            playerprofile = playerprofilev2.PlayerProfileV2(player_id=player_id).get_data_frames()
            print(pd.DataFrame(playerprofile[0]).head)
            return Exception

    
def get_player_profile_df(player_id):
    create_player_profile_csv(player_id)

    df = pd.read_csv(f'./stats/CSVs/playerprofiles/{player_id}.csv')

    return df


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







































