from flask import Flask
from flask import render_template
from nba_api.stats.library import data
import pandas as pd

app = Flask(__name__)

@app.route("/")
def root():
        return render_template('templates/index.html')


@app.route("/player_finder")
def player_finder():
    player_search = data.players

    player_df = pd.DataFrame(player_search)
    
    return player_df



    

