import sqlite3

from nba_api.stats.endpoints import playerprofilev2, commonteamroster, playerawards
from nba_api.stats.static import teams, players

import pandas as pd

import os


# Basic player data

def create_basic_player_data_csv():
    # Does file exist?
    if os.path.isfile('./app/stats/CSVs/basic_player_data.csv') == True:
        pass
    else:                     # Create file
        basic_player_df = pd.DataFrame(players.get_active_players())   
        basic_player_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
        basic_player_df.to_csv('./app/stats/CSVs/basic_player_data.csv', index=False)


def get_basic_player_df():
    '''
    Gets (id, last name, first name, full name, activity)
    '''
    create_basic_player_data_csv()
    update_basic_player_df()
    df = pd.read_csv('./app/stats/CSVs/basic_player_data.csv')
    
    return df


def get_player_ids():
    '''
    '''
    df = get_basic_player_df()
    return list(df['ids'])


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
    location = './app/stats/CSVs/basic_player_data.csv'
    
    basic_player_df = pd.DataFrame(players.get_active_players())
    basic_player_df.columns = ['ids', 'full_name', 'first_name', 'last_name', 'is_active']

    basic_player_df.to_csv(location, index=False)


# Team ID
def get_players_team_id(player_id):
    player_profile = get_player_profile_df(player_id, 'Next Game')
    players_team_id = player_profile['PLAYER_TEAM_ID'].iloc[0]
    return players_team_id


# Player Profile data
def create_player_profile_csv(player_id):
    global data_names_list
    data_names_list = ['Career Totals Regular Season by Year',
                       'Career Totals Regular Season',
                       'Career Totals Post Season by Year',
                       'Career Totals Post Season',
                       'Career Totals All-Star Games by Year',
                       'Career Totals All-Star Games',
                       'Career Totals College by Year',
                       'Career Totals College',
                       'Career Totals Preseason by Year',
                       'Career Totals Preseason',
                       'Career Rankings by Year',
                       'Career Playoff Ranking by Year',
                       'Season Highs',
                       'Career Highs',
                       'Next Game']
    try:
        player_profile_list = playerprofilev2.PlayerProfileV2(player_id=player_id).get_data_frames()

    except Exception as e:
        print(e)
    for x, i in zip(data_names_list, player_profile_list):
        df = pd.DataFrame(i)
        if os.path.isdir(f'./app/stats/CSVs/playerprofiles/{player_id}') == True:
            pass
        else:
            os.makedirs(f'./app/stats/CSVs/playerprofiles/{player_id}')


        df.to_csv(f'./app/stats/CSVs/playerprofiles/{player_id}/{x}.csv')


def get_player_profile_df(player_id, df_name):
    try:
        create_player_profile_csv(player_id)  # works as an update csv

    except Exception: 
        print(Exception)

    df = pd.read_csv(f'./app/stats/CSVs/playerprofiles/{player_id}/{df_name}.csv')


    return df


# Team Roster
def create_team_roster_csv(team_id):
    if os.path.isfile(f'./app/stats/CSVs/teamrosters/{team_id}.csv') == True:
        pass
    else:
        team_roster_df = pd.DataFrame(commonteamroster.CommonTeamRoster(team_id).get_data_frames()[0])
        team_roster_df.to_csv(f'./app/stats/CSVs/teamrosters/{team_id}.csv', index=False)


def get_teamroster_df(team_id):
    create_team_roster_csv(team_id)

    df = pd.read_csv(f'./app/stats/CSVs/teamrosters/{team_id}.csv')

    return df


# Basic Team data
def create_teams_data_csv():
    if os.path.isfile('./app/stats/CSVs/teams_data.csv') == True:
        pass
    else:
        teams_df = pd.DataFrame(teams.get_teams())
        teams_df.to_csv('./app/stats/CSVs/teams_data.csv')


def get_teams_df():
    create_teams_data_csv()

    teams_df = pd.read_csv('./app/stats/CSVs/teams_data.csv')

    return teams_df


# Search results data
def create_search_csv(df):
    if os.path.exists('./app/stats/CSVs/search.csv'):
        try: 
            search_df = pd.read_csv('./app/stats/CSVs/search.csv')
        except Exception as e:
            print(e)
            pass
        add_list = []
        for x in df['full_name']: 
            matchlis = []
            try:
                for j in search_df['full_name']:
                    if x == j:
                        matchlis.append(True)
                    else:
                        matchlis.append(False)
            except:
                add_list.append(x)
        match_count = 0
        for i in matchlis:
            if i == True:
                match_count += 1
        if match_count == 0:
            add_list.append(x)
        for i in add_list:
            row = df[df['full_name'] == i]
            row_df = pd.DataFrame(row)
            row_df.to_csv('./app/stats/CSVs/search.csv', mode='a')
    else:
        os.mknod('./app/stats/CSVs/search.csv')

def get_search_csv(names):
    df = pd.read_csv('./app/stats/CSVs/search.csv')   
    response = False
    count = 0

    fin_df = pd.DataFrame()
    row_keep = []
    if df.empty == True:
        return response, fin_df
    for i in names:
        for j in df['full_name']:
            if j == i:
                count += 1
                row = df.loc[df['full_name'] == j]
                row_keep.append(pd.DataFrame(row))
    for x in range(len(row_keep)):
        fin_df = pd.concat([fin_df, row_keep[x]])
    if count == 9:
        response = True
    return response, fin_df

                
# Player awards
def create_player_awards_csv(player_id):
    try:
        df = playerawards.PlayerAwards(player_id=player_id).get_data_frames()[0]
        df.to_csv(f'./app/stats/CSVs/playerprofiles/{player_id}/awards.csv')
    except:
        print(Exception)



def get_player_awards_df(player_id):
    create_player_awards_csv(player_id)
    
    df = pd.read_csv(f'./app/stats/CSVs/playerprofiles/{player_id}/awards.csv')

    return df































