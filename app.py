#Flask web app
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#Data API
import stat

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


# Index view
@app.route('/')
def root():
    return render_template('index.html')


# Search Ids view
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

    return render_template('search_player_id.html', tables=[id_result.to_html(classes='table', index_names=False)])


# Dashboard view (main user view)
@app.route('/dash')
def dash():
    df = pd.DataFrame(PlayersIds)
    df.columns = ['Ids', 'Last_Name', 'First_Name', 'Full_Name', 'Current_Player']
    df.head()
    #df.drop('Last_Name', inplace=True)
    #df.drop('First_Name', inplace=True)
    return render_template('dash.html', tables=[df.to_html(classes='table', index_names=False)])


# Player Pages
@app.route('/<player_name_fullscreen>')
def player_fullscreen(player_name):
    #player_awards = playerawards.PlayerAwards(player_id=1628983)
    #print(player_awards)
    return render_template('player_fullscreen.html')



















