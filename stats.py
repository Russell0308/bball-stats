import requests
import pandas as pd
import tkinter as tk


# Player id search using players name #
def players():
    players_name = input('Enter player name: ')
    api_players = 'https://www.balldontlie.io/api/v1/players?search=' + players_name
    r_players = requests.get(api_players)
    players = r_players.json()
    print('id:', players["data"][0]["id"], 'Player:', players["data"][0]["first_name"], players["data"][0]["last_name"])

# Player search using player id #
def spec_player():
    player_id = input('Enter player id: ')
    api_spec_player = 'https://www.balldontlie.io/api/v1/players/' + player_id
    r_spec_player = requests.get(api_spec_player)
    spec_player = r_spec_player.json()
    print('Team:', spec_player["team"]["full_name"])
    print('Position:', spec_player["position"])
    print('Height:', spec_player["height_feet"], '-', spec_player["height_inches"])
    print('Weight:', spec_player["weight_pounds"], 'lbs')


# Initialize all teams #
def teams():
    api_teams = 'https://www.balldontlie.io/api/v1/teams'
    r_teams = requests.get(api_teams)
    all_teams = r_teams.json()

# Initialize specific team #
def spec_team():
    team_id = input('Enter team ID: ')
    api_spec_team = 'https://www.balldontlie.io/api/v1/teams/' + team_id
    r_spec_team  = requests.get(api_spec_team)
    spec_team = r_spec_team.json()
    print(spec_team)

api_games = 'https://www.balldontlie.io/api/v1/games'
api_spec_game = 'https://www.balldontlie.io/api/v1/games/<ID>'
api_stats = 'https://www.balldontlie.io/api/v1/stats'

api_avg = 'https://www.balldontlie.io/api/v1/season_averages'


spec_player()
