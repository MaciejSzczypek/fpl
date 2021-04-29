import pandas as pd
import argparse
from modules.league_info_provider import LeagueStatisticsProvider
import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--league_entry",
        required=True,
        help="League id"
    )
    payload = {
        'password': 'c7A',
        'login': 'maciek.szczypek@gmail.com',
        'redirect_uri': 'https://fantasy.premierleague.com/a/login',
        'app': 'plfpl-web'
    }

    args = parser.parse_args()
    league_statistics_provider = LeagueStatisticsProvider(league_entry=args.league_entry)
    teams_statistics_df = league_statistics_provider.get_teams_statistics_df()
    pd.set_option('display.width', None)
    print(teams_statistics_df)
