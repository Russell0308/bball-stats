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


def name_to_id(players_names):
    print(players_names)
    df = pd.DataFrame(PlayersIds)
    df.columns = ['Ids', 'Last_Name', 'First_Name', 'Full_Name', 'Current_Player']
    
    result_df = pd.DataFrame()

    for i in players_names:
        row = df.loc[df['Full_Name'] == i]

        result_df = pd.concat((result_df, row), axis=0, ignore_index=True)
    return result_df

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/search_players_id', methods = ('POST', 'GET'))
def search_player_id():
    df_players_ids = pd.DataFrame(PlayersIds)
    df_players_ids.columns = ['Ids', 'Last_Name', 'First_Name', 'Full_Name', 'Current_Player']

    user_query = str(request.form.get('playerName'))
    user_search_result = process.extract(user_query, df_players_ids['Full_Name'], limit=10)

    result_player_name_list = []

    for i in user_search_result:
        result_player_name_list.append(i[0])
    id_result = (name_to_id(result_player_name_list))

    return render_template('dash.html', tables=[id_result.to_html(classes='table', index_names=False)], titles=id_result.columns.values)
