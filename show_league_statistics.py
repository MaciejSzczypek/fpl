import tabulate
import argparse
from modules.league_statistics_provider import BasicLeagueStatisticsProvider
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--league_entry",
        required=True,
        help="League id",
        type=int,
    )
    args = parser.parse_args()
    league_statistics_provider = BasicLeagueStatisticsProvider(league_entry=args.league_entry)
    t0 = time.time()
    teams_statistics = league_statistics_provider.get_league_statistics()
    t1 = time.time()
    tabulated_team_statistics = tabulate.tabulate(teams_statistics, headers="keys")
    print(tabulated_team_statistics)
    print(t1 - t0)
