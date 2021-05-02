from typing import Dict, Any

from modules.base_providers import BaseTeamStatisticsProvider
from modules.constants import FieldName


class BasicTeamStatisticsProvider(BaseTeamStatisticsProvider):

    @classmethod
    def get_team_statistics(cls, team_name: str, team_entry: int) -> Dict[str, Any]:
        team_info = cls._get_team_info(team_entry)
        team_statistics = {
            FieldName.TEAM_NAME.value: team_name,
            FieldName.SUMMARY_OVERALL_POINTS.value: cls._get_summary_overall_points(team_info),
            FieldName.SUMMARY_OVERALL_RANK.value: cls._get_summary_overall_rank(team_info),
            FieldName.SUMMARY_EVENT_POINTS.value: cls._get_summary_event_points(team_info),
            FieldName.SUMMARY_EVENT_RANK.value: cls._get_summary_event_rank(team_info),
            FieldName.LAST_DEADLINE_BANK.value: cls._get_team_bank_value(team_info),
            FieldName.LAST_DEADLINE_TEAM_VALUE.value: cls._get_team_value(team_info),
            FieldName.LAST_DEADLINE_TOTAL_TRANSFERS.value: cls._get_total_transfers(team_info),
        }
        return team_statistics
