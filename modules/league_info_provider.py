import requests
import json
import pandas as pd
from modules.team_statistics_provider import TeamStatisticsProvider
from modules.constants import FieldName, LEAGUE_REQUEST_TEMPLATE


class LeagueStatisticsProvider:

    def __init__(self, league_entry: int):
        self._league_entry = league_entry

    def _get_league_info_dict(self):
        league_request = LEAGUE_REQUEST_TEMPLATE.substitute(league_entry=self._league_entry)
        response = requests.get(league_request)
        return json.loads(response.text)

    def _get_team_names_to_entry_mapping(self):
        league_info_dict = self._get_league_info_dict()
        return {
            player_dict[FieldName.ENTRY_NAME.value]: player_dict[FieldName.ENTRY.value]
            for player_dict in league_info_dict[FieldName.STANDINGS.value][FieldName.RESULTS.value]
        }

    def get_teams_statistics_df(self):
        teams_statistics = [
            TeamStatisticsProvider.get_basic_team_statistics(
                team_name=team, team_entry=entry
            )
            for team, entry in self._get_team_names_to_entry_mapping().items()
        ]
        return pd.DataFrame(teams_statistics)
