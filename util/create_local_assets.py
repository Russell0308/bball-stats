from app.stats import stat_collector as statc

df = statc.get_teams_df()

ids = list(df['id'])

if __name__ == '__main__':
    for i in ids:
        statc.get_team_logos(i)
