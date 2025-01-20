from app.stats.stat_collector import get_player_ids, create_player_profile_csv, create_player_awards_csv

def main():
    ids = get_player_ids()

    for i in ids:
        print(f'Trying {i}')
        create_player_profile_csv(i)
        create_player_awards_csv(i)

        print(f'Created {i}')


if __name__ == '__main__':
    main()
