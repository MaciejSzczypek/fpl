import requests
import json
from string import Template
import pandas as pd
from modules.team_statistics_provider import TeamStatisticsProvider
from modules.constants import (
    ENTRY_FIELD_NAME,
    ENTRY_NAME_FIELD_NAME,
    STANDINGS_FIELD_NAME,
    RESULTS_FIELD_NAME,
)


class LeagueStatisticsProvider:
    LEAGUE_REQUEST_TEMPLATE = Template(
        f"https://fantasy.premierleague.com/api/leagues-classic/$league_entry/standings/"
    )

    def __init__(self, league_entry: int):
        self._league_entry = league_entry

    def _get_league_info_dict(self):
        league_request = self.LEAGUE_REQUEST_TEMPLATE.substitute(league_entry=self._league_entry)
        response = requests.get(league_request)
        return json.loads(response.text)

    def _get_team_names_to_entry_mapping(self):
        league_info_dict = self._get_league_info_dict()
        return {
            player_dict[ENTRY_NAME_FIELD_NAME]: player_dict[ENTRY_FIELD_NAME]
            for player_dict in league_info_dict[STANDINGS_FIELD_NAME][RESULTS_FIELD_NAME]
        }

    def get_teams_statistics_df(self):
        # todo split to 2 different dfs (rank/points and additional statistics)
        teams_statistics = [
            TeamStatisticsProvider.get_basic_team_statistics(
                team_name=team, team_entry=entry
            )
            for team, entry in self._get_team_names_to_entry_mapping().items()
        ]
        return pd.DataFrame(teams_statistics)
