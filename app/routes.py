# Flask
from flask import Blueprint, Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

# Stat server
from app.stats import stat_server

# DS Library(s)
import pandas as pd

# Other
import os
import datetime

year = str(datetime.date.today())[:4]
season = str(int(year) - 1) + '-' + year[2:]


main = Blueprint('main', __name__, './main/static/assets')


# Index view
@main.route('/')
def root():
    return render_template('index.html')


# Dashboard view (main user view)
@main.route('/dash', methods=['GET', 'POST'])
def dash():
    user_query = str(request.form.get('playerName'))
    df = stat_server.get_search_result_dash(user_query)

    image = os.path.join(main.config['STATIC_FOLDER'], 'BostonCeltics.png')

    award_winners = stat_server.get_season_awardwinners(season)

    return render_template('dash.html',
                           champ_img=image,
                           season=season,
                           award_winners=award_winners,
                           tables=[df.to_html(classes='table',
                                              render_links=True,
                                              index_names=False,
                                              escape=False,
                                              index=False,
                                              header=False)])


# Player Pages
@main.route('/players/<player_name>')
def player_fullscreen(player_name):
    player_name_clean = player_name.replace('_', ' ')
    player_id = stat_server.get_id_from_name(player_name_clean)
    player_number = stat_server.get_player_number(player_id)
    team_name = stat_server.get_team_name(player_id)
    player_pos = stat_server.get_player_position(player_id)
    height, weight = stat_server.get_player_height_weight(player_id)
    df = stat_server.get_career_per_game_by_season(player_id)
    df_awards = stat_server.get_player_awards(player_id)
    return render_template('player_fullscreen.html',
                           player_name=player_name_clean,
                           player_id=player_id,
                           player_number=player_number,
                           player_position=player_pos,
                           player_height=height,
                           player_weight=weight,
                           team_name=team_name,
                           tablePawards=[df_awards.to_html(
                               classes='table',
                               escape=False,
                               index=False,
                               header=True)
                            ],
                           tablepgstats=[df.to_html(classes='table',
                                                    escape=False,
                                                    index=False,
                                                    header=True)])




















