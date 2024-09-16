#Flask web app
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#Data API
from nba_api.stats.library import data

#DS Library(s)
import pandas as pd

#Fuzzy Search
from thefuzz import process

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)

PlayersIds = data.players

df_players_ids = pd.DataFrame(PlayersIds)


def name_to_id(player_name):
    df = pd.DataFrame(PlayersIds)
    df[df[3] == player_name]
    return df

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/search_players_id', methods = ('POST', 'GET'))
def search_player_id():
    df_players_ids = pd.DataFrame(PlayersIds)
    df_players_ids.columns = ['Ids', 'Last_Name', 'First_Name', 'Full_Name', 'Current_Player']
    df_result = df_players_ids

    user_query = str(request.form.get('playerName'))

    user_search_result = process.extract(user_query, df_players_ids['Full_Name'], limit=5)

    result_player_name_list = []

    for i in user_search_result:
        result_player_name_list.append(i[0])

    df_result = (name_to_id(result_player_name_list[0]))

    # TODO - return df of players and their ids


    #df_result = df_search_results

    return render_template('dash.html', tables=[df_result.to_html(classes='data')], titles=df_result.columns.values)
