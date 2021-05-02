import tabulate
import argparse
from modules.league_statistics_provider import BasicLeagueStatisticsProvider

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
    teams_statistics = league_statistics_provider.get_league_statistics()
    tabulated_team_statistics = tabulate.tabulate(teams_statistics, headers="keys")
    print(tabulated_team_statistics)
