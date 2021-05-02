import json
from typing import Dict, Any, List
import requests

from modules.constants import FieldName, LEAGUE_REQUEST_TEMPLATE
from modules.team_statistics_provider import TeamStatisticsProvider


class LeagueStatisticsProvider:

    def __init__(self, league_entry: int) -> None:
        self._league_entry = league_entry

    def _get_league_info(self) -> Dict[str, Any]:
        league_request = LEAGUE_REQUEST_TEMPLATE.substitute(league_entry=self._league_entry)
        response = requests.get(league_request)
        return json.loads(response.text)

    def _get_team_names_to_entry_mapping(self) -> Dict[str, int]:
        league_info_dict = self._get_league_info()
        return {
            player_dict[FieldName.ENTRY_NAME.value]: player_dict[FieldName.ENTRY.value]
            for player_dict in league_info_dict[FieldName.STANDINGS.value][FieldName.RESULTS.value]
        }

    def get_league_statistics(self) -> List[Dict[str, Any]]:
        return [
            TeamStatisticsProvider.get_basic_team_statistics(
                team_name=team, team_entry=entry
            )
            for team, entry in self._get_team_names_to_entry_mapping().items()
        ]
