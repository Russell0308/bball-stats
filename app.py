from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#Data API
import pystat

#DS Library(s)
import pandas as pd

#Fuzzy Search
from thefuzz import process

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
    df = pystat.get_search_result_dash(user_query)

    return render_template('dash.html', tables=[df.to_html(classes='table table-stripped', render_links=True, index_names=False)])


# Player Pages
@app.route('/<player_name_fullscreen>')
def player_fullscreen(player_name):
    #player_awards = playerawards.PlayerAwards(player_id=1628983)
    #print(player_awards)
    return render_template('player_fullscreen.html')



















