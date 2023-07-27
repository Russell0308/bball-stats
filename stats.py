import requests
import pandas as pd
from tkinter import *
from tkinter import ttk


# Player id search using players name #
def players():
    players_name = ttk.Entry(root, text = 'Enter a players name').grid()
    api_players = 'https://www.balldontlie.io/api/v1/players?search=' + str(players_name)
    r_players = requests.get(api_players)
    players = r_players.json()
    ttk.Label(root, text = ('id:', players["data"][0]["id"], 'Player:', players["data"][0]["first_name"], players["data"][0]["last_name"])).grid()

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
def teams(): # No use case yet #
    team_name = input('Enter team name: ')
    api_teams = 'https://www.balldontlie.io/api/v1/teams'
    r_teams = requests.get(api_teams)
    all_teams = r_teams.json()
    print(all_teams[team_name])

# Initialize specific team #
def spec_team(): # No use case yet #
    team_id = input('Enter team id: ')
    api_spec_team = 'https://www.balldontlie.io/api/v1/teams/' + team_id
    r_spec_team  = requests.get(api_spec_team)
    spec_team = r_spec_team.json()
    print(spec_team)

def games():
    api_games = 'https://www.balldontlie.io/api/v1/games'
    r_games = requests.get(api_games)

def spec_game():
    game_id = input('Enter game id: ')
    api_spec_game = 'https://www.balldontlie.io/api/v1/games/' + game_id
    r_spec_game = requests.get(api_spec_game)
    spec_game = r_spec_game.json()
    print(spec_game["date"])
    print(spec_game["home_team"]["abbreviation"], 'vs', spec_game["visitor_team"]["abbreviation"])
    print(spec_game["home_team_score"], '-' ,spec_game["visitor_team_score"])

def stats():
    player_id = input('Enter player id: ')
    api_stats = 'https://www.balldontlie.io/api/v1/stats?player_ids[]=' + player_id
    r_stats = requests.get(api_stats)
    stats = r_stats.json()
    print(stats)

def avg():
    season = input('Enter season: ')
    player_id = input('Enter player id: ')
    api_avg = 'https://www.balldontlie.io/api/v1/season_averages'
    r_avg = requests.get(api_avg)
    avg = r_avg.json()
    print(avg)

root = Tk()

root.title('bball-stats')

ttk.Label(root, text = 'What are you looking for?')


def Players_Button():
    players()
ttk.Button(root, text = "Players/Players id", command = Players_Button()).grid()




ttk.Radiobutton(root, text = "Specific Player").grid()
ttk.Radiobutton(root, text = "All Teams").grid()
ttk.Radiobutton(root, text = "Specific Teams").grid()
ttk.Radiobutton(root, text = "games").grid()
ttk.Radiobutton(root, text = "Specific Games").grid()
ttk.Radiobutton(root, text = "Stats").grid()
ttk.Radiobutton(root, text = "Season Averages").grid()
ttk.Button(root).grid()


root.mainloop()
