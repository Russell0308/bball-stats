import sqlite3

from flask import url_for

from app.stats import stat_collector as statc

from thefuzz import process

import pandas as pd

import re

import sys

players_df = statc.get_basic_player_df()
players_df.drop('last_name', inplace=True, axis=1)
players_df.drop('first_name', inplace=True, axis=1)
players_df = players_df[players_df['is_active'] == True]
players_df.drop('is_active', inplace=True, axis=1)


def get_search_result_dash(user_query):
    user_search_result = process.extract(user_query, players_df['full_name'], limit=10) #Fuzzy find top ten active players names using user search 'name'. 

    result_df = pd.DataFrame()

    user_names_result = [] # Cut out all the names we don't care about decreases load time immensely
    for i in user_search_result:
        user_names_result.append(i[0])
    result_df['full_name'] = user_names_result
    
    try:
        response, df = statc.get_search_csv(result_df['full_name'])
        if response == True:
            df = df.drop(['Unnamed: 0', 'full_name'], axis=1)
            return df.iloc[0:]

    except:
        pass

    player_links_list = []
    player_team_abbrev_list = []
    player_number_list = []

    for i in result_df['full_name']:
        result_df['link_names'] = result_df['full_name'].apply(lambda x: re.sub(r'\s+', '_', x)) # Add underscores to players names for links to players page
        player_name = i

        player_row = players_df[players_df['full_name'] == player_name]
        player_id = player_row['ids'].iloc[0]

        players_team_id = statc.get_players_team_id(player_id)

        teams = pd.DataFrame(statc.get_teams_df())
        teams = teams[teams['id'] == players_team_id]
        if teams['abbreviation'].empty == True:  # If players don't have a valid team id they are removed from result_df
            result_df = result_df.loc[result_df['full_name'] != player_name]
            continue
        player_team_abbrev_list.append(teams['abbreviation'].iloc[0])

        player_number = statc.get_player_number(player_id)

        player_number_list.append(player_number)

    for x, y in zip(result_df['full_name'], result_df['link_names']):
        player_links = f'''<a href=" { url_for('main.player_fullscreen', player_name=y) } ">{x}</a>'''
        player_links_list.append(player_links)

    result_df.drop('link_names', axis=1, inplace=True)
    
    result_df['Player_Number'] = player_number_list
    result_df['player_link'] = player_links_list
    result_df['Abbreviations'] = player_team_abbrev_list

    statc.create_search_csv(df=result_df)

    result_df.drop('full_name', axis=1, inplace=True)
    

    return result_df.iloc[:5]


def get_id_from_name(player_name):
    df = players_df
    player_id = df[df['full_name'] == player_name]
    player_id = (player_id['ids'].iloc[0])
    return player_id


def get_name_from_id(player_id):
    df = players_df
    player_name = df[df['ids'] == player_id]
    return player_name


def get_career_per_game_by_season(player_id):
    df_name = statc.data_names_list[0]
    df = statc.get_player_profile_df(player_id, df_name)

    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop('PLAYER_ID', axis=1, inplace=True)
    df.drop('LEAGUE_ID', axis=1, inplace=True)
    df.drop('TEAM_ID', axis=1, inplace=True)
    df.drop('PLAYER_AGE', axis=1, inplace=True)

    df.columns = ['YEAR', 'TEAM', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG%', 'FG3M', 'FG3A', 'FG3%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

    df['PTS'] = round(df['PTS']/df['GP'], 1)
    df['PF'] = round(df['PF']/df['GP'], 1)
    df['TOV'] = round(df['TOV']/df['GP'], 1)
    df['BLK'] = round(df['BLK']/df['GP'], 1)
    df['STL'] = round(df['STL']/df['GP'], 1)
    df['AST'] = round(df['AST']/df['GP'], 1)
    df['REB'] = round(df['REB']/df['GP'], 1)
    df['DREB'] = round(df['DREB']/df['GP'], 1)
    df['OREB'] = round(df['OREB']/df['GP'], 1)
    df['FTA'] = round(df['FTA']/df['GP'], 1)
    df['FTM'] = round(df['FTM']/df['GP'], 1)
    df['FG3A'] = round(df['FG3A']/df['GP'], 1)
    df['FG3M'] = round(df['FG3M']/df['GP'], 1)
    df['FGA'] = round(df['FGA']/df['GP'], 1)
    df['FGM'] = round(df['FGM']/df['GP'], 1)
    df['MIN'] = round(df['MIN']/df['GP'], 1)

    return df


def get_player_number(player_id):
    return statc.get_player_number(player_id)


def get_team_name(player_id):
    team_id = statc.get_players_team_id(player_id)

    df = statc.get_teams_df()

    team = df[df['id'] == team_id]

    team_name = team['full_name'].iloc[0]

    return team_name


def get_player_position(player_id):
    team_id = statc.get_players_team_id(player_id)

    teamroster_df = statc.get_teamroster_df(team_id)

    player_row = teamroster_df[teamroster_df['PLAYER_ID'] == player_id]

    return player_row['POSITION'].iloc[0]


def get_player_height_weight(player_id):
    team_id = statc.get_players_team_id(player_id)

    teamroster_df = statc.get_teamroster_df(team_id)

    player_row = teamroster_df[teamroster_df['PLAYER_ID'] == player_id]

    return player_row['HEIGHT'].iloc[0], player_row['WEIGHT'].iloc[0]


def get_player_awards(player_id):
    df = statc.get_player_awards_df(player_id)

    df.drop('Unnamed: 0', inplace=True, axis=1)
    df.drop('PERSON_ID', inplace=True, axis=1)
    df.drop('FIRST_NAME', inplace=True, axis=1)
    df.drop('LAST_NAME', inplace=True, axis=1)

    new_df = pd.DataFrame(index=[0])
    
    olympic_gold_medal = 0
    nba_champion = 0
    mvp = 0
    fmvp = 0
    nba_allstar = 0
    all_nba = 0
    all_rookie_team = 0
    rookie_of_the_month = 0
    player_of_the_week = 0
    player_of_the_month = 0


    for i in list(df['DESCRIPTION']):
        if i == 'Olympic Gold Medal':
            olympic_gold_medal += 1
        elif i == 'NBA Champion':
            nba_champion += 1
        elif i == 'NBA All-Star':
            nba_allstar += 1
        elif i == 'All-NBA':
            all_nba += 1
        elif i == 'NBA Most Valuable Player':
            mvp += 1
        elif i == 'NBA Finals Most Valuable Player':
            fmvp += 1
        elif i == 'All-Rookie Team':
            all_rookie_team += 1
        elif i == 'NBA Rookie of the Month':
            rookie_of_the_month += 1
        elif i == 'NBA Player of the Week':
            player_of_the_week += 1
        elif i == 'NBA Player of the Month':
            player_of_the_month += 1


    new_df['Olympic Gold Medal'] = olympic_gold_medal
    new_df['NBA Champion'] = nba_champion
    new_df['All-Star'] = nba_allstar
    new_df['All-NBA'] = all_nba
    new_df['MVP'] = mvp
    new_df['Finals MVP'] = fmvp
    new_df['All-Rookie Team'] = all_rookie_team
    new_df['Rookie of the Month'] = rookie_of_the_month
    new_df['Player of the Week'] = player_of_the_week
    new_df['Player of the Month'] = player_of_the_month


    return new_df
    

def get_season_awardwinners(season):
    id_df = pd.DataFrame(players_df['ids'])
    count = 0

    df_awards_ = []
    FMVP = 'NBA Finals Most Valuable Player'
    MVP = 'NBA Most Valuable Player'
    DPOY = 'NBA Defensive Player of the Year'
    ROTY = 'NBA Rookie of the Year'
    CPOTY = 'NBA Clutch Player of the Year'
    COTY = 'NBA Coach of the Year'
    MIP = 'NBA Most Improved Player'
    SMOTY = 'NBA Sixth Man of the Year'



    for i in range(len(id_df)):
        player_id = id_df['ids'][i]
    
        path = (f'./app/stats/CSVs/playerprofiles/{player_id}/awards.csv')
        df = pd.read_csv(path)

        df = df[df['SEASON'] == season]
        
        if df.empty == True:
            continue

        df_FMVP = df[df['DESCRIPTION'] == FMVP]
        df_MVP = df[df['DESCRIPTION'] == MVP]
        df_DPOY = df[df['DESCRIPTION'] == DPOY]
        df_ROTY = df[df['DESCRIPTION'] == ROTY]
        df_CPOTY = df[df['DESCRIPTION'] == CPOTY]
        #df_COTY = df[df['DESCRIPTION'] == COTY]
        df_MIP = df[df['DESCRIPTION'] == MIP]
        df_SMOTY = df[df['DESCRIPTION'] == SMOTY]
        
        if df_FMVP.empty == False:
            df_awards_.append(df_FMVP)

        if df_MVP.empty == False:
            df_awards_.append(df_MVP)

        if df_DPOY.empty == False:
            df_awards_.append(df_DPOY)

        if df_ROTY.empty == False:
            df_awards_.append(df_ROTY)

        if df_CPOTY.empty == False:
            df_awards_.append(df_CPOTY)

        #if df_COTY.empty == False:
            #df_awards_.append(df_COTY)

        if df_MIP.empty == False:
            df_awards_.append(df_MIP)

        if df_SMOTY.empty == False:
            df_awards_.append(df_SMOTY)
    
    display_awards = []
    for i in df_awards_:
        fname = i['FIRST_NAME'].iloc[0]
        lname = i['LAST_NAME'].iloc[0]
        award = i['DESCRIPTION'].iloc[0]

        full_name = fname + ' ' + lname

        link_name = re.sub(r'\s+', '_', full_name)

        link = f'''<a href=" { url_for('main.player_fullscreen', player_name=link_name) } ">{full_name}</a>'''

        winner = award + ': ' + link
        
        display_awards.append(winner)




    return display_awards


def get_teams_data():
    df = statc.get_teams_df()
    df[' '] = df['abbreviation']
    df['Team Names'] = df['full_name']
    droplist = ['Unnamed: 0', 'id', 'full_name', 'abbreviation', 'nickname', 'city', 'state', 'year_founded']
    for i in droplist:
        df.drop(i, axis=1, inplace=True)

    team_links_list = []

    for x in df['Team Names']:
        team_links = f'''<a href=" { url_for('main.team_fullscreen', team_name=x) } ">{x}</a>'''
        team_links_list.append(team_links)

    df['Team Names'] = team_links_list

    return df



def get_team_data_df(team_name):
    df = statc.get_teams_df()
    df = df[df['full_name'] == team_name]

    full_name = df['full_name'].iloc[0]
    abbreviation = df['abbreviation'].iloc[0]
    nickname = df['nickname'].iloc[0]
    city = df['city'].iloc[0]
    state = df['state'].iloc[0]
    year_founded = df['year_founded'].iloc[0]


    team_id = statc.get_team_id_from_team_name(team_name)

    roster = statc.get_teamroster_df(team_id)

    player_names = list(roster['PLAYER'])

    players_links = []

    for i in player_names:
        link_name = re.sub(r'\s+', '_', i)
        link = f'''<a href=" { url_for('main.player_fullscreen', player_name=link_name) } ">{i}</a>'''
        players_links.append(link)
    
    roster['PLAYER'] = players_links
    
    drop_list = ['TeamID', 'SEASON', 'LeagueID', 'NICKNAME', 'PLAYER_SLUG', 'BIRTH_DATE', 'PLAYER_ID']

    for i in drop_list:
        roster.drop(i, inplace=True, axis=1)

    return full_name, abbreviation, city, state, year_founded, roster



