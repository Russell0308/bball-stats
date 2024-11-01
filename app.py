#Flask
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

#Stat server
from stats import stat_server

#DS Library(s)
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


# Index view
@app.route('/')
def root():
    return render_template('index.html')


# Dashboard view (main user view)
@app.route('/dash', methods=['GET', 'POST'])
def dash():
    user_query = str(request.form.get('playerName'))
    df = stat_server.get_search_result_dash(user_query)

    return render_template('dash.html', tables=[df.to_html(classes='table', render_links=True, index_names=False, escape=False, index=False, header=False)])


# Player Pages
@app.route('/players/<player_name>')
def player_fullscreen(player_name):
    df = stat_server.get_player_profile_season_pg()
    return render_template('player_fullscreen.html', player_name=player_name, table=[df.to_html(classes='table', render_links=True, index_names=False, escape=False, index=False, header=False)])






















