from flask import Flask, render_template
from nba_api.stats.library import data
import pandas as pd


app = Flask(__name__)


@app.route("/")
def root():
        return render_template('index.html')


@app.route("/player_finder")
def player_lookup():
    player_search = data.players

    player_df = pd.DataFrame(player_search)
    

    return 'hello world!'

    

