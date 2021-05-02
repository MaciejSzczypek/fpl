import json
from typing import Dict, Any, Optional

import requests

from modules.constants import FieldName, TEAM_REQUEST_TEMPLATE


class TeamStatisticsProvider:
    _DIVISION_FACTOR = 10

    @classmethod
    def _get_value_divided_by_factor(cls, value: Optional[float]) -> Optional[float]:
        return None if value is None else value / cls._DIVISION_FACTOR

    @classmethod
    def _get_formatted_rank_value(cls, rank_value: Optional[int]) -> Optional[str]:
        if rank_value is None:
            return rank_value
        rank_value_string = str(rank_value)
        formatted_rank_value = ""
        for character_position in range(1, len(rank_value_string) + 1):
            formatted_rank_value = rank_value_string[-character_position] + formatted_rank_value
            if character_position % 3 == 0:
                formatted_rank_value = " " + formatted_rank_value
        return formatted_rank_value

    @classmethod
    def _get_team_value(cls, team_info: Dict[str, Any]) -> Optional[float]:
        team_value = team_info.get(FieldName.LAST_DEADLINE_TEAM_VALUE.value)
        return cls._get_value_divided_by_factor(team_value)

    @classmethod
    def _get_team_bank_value(cls, team_info: Dict[str, Any]) -> Optional[float]:
        bank_value = team_info.get(FieldName.LAST_DEADLINE_BANK.value)
        return cls._get_value_divided_by_factor(bank_value)

    @classmethod
    def _get_total_transfers(cls, team_info: Dict[str, Any]) -> Optional[int]:
        return team_info.get(FieldName.LAST_DEADLINE_TOTAL_TRANSFERS.value)

    @classmethod
    def _get_summary_overall_points(cls, team_info: Dict[str, Any]) -> Optional[int]:
        return team_info.get(FieldName.SUMMARY_OVERALL_POINTS.value)

    @classmethod
    def _get_summary_overall_rank(cls, team_info: Dict[str, Any]) -> Optional[str]:
        return cls._get_formatted_rank_value(team_info.get(FieldName.SUMMARY_OVERALL_RANK.value))

    @classmethod
    def _get_summary_event_points(cls, team_info: Dict[str, Any]) -> Optional[int]:
        return team_info.get(FieldName.SUMMARY_EVENT_POINTS.value)

    @classmethod
    def _get_summary_event_rank(cls, team_info: Dict[str, Any]) -> Optional[str]:
        return cls._get_formatted_rank_value(team_info.get(FieldName.SUMMARY_EVENT_RANK.value))

    @classmethod
    def _get_team_info(cls, team_entry: int) -> Dict[str, Any]:
        response = requests.get(TEAM_REQUEST_TEMPLATE.substitute(team_entry=team_entry))
        return json.loads(response.text)

    @classmethod
    def get_basic_team_statistics(cls, team_name: str, team_entry: int) -> Dict[str, Any]:
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
