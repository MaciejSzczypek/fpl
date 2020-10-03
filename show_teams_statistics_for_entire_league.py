import pandas as pd
import argparse
from modules.league_info_provider import LeagueStatisticsProvider


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--league_entry",
        required=True,
        help="League id"
    )
    args = parser.parse_args()
    league_statistics_provider = LeagueStatisticsProvider(league_entry=args.league_entry)
    teams_statistics_df = league_statistics_provider.get_teams_statistics_df()
    pd.set_option('display.width', 200)
    print(teams_statistics_df)
