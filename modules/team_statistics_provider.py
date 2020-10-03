import requests
import json
from string import Template
from typing import Dict, Any
from modules.constants import (
    TEAM_NAME_FIELD_NAME,
    SUMMARY_EVENT_POINTS,
    SUMMARY_EVENT_RANK,
    SUMMARY_OVERALL_POINTS,
    SUMMARY_OVERALL_RANK,
    LAST_DEADLINE_BANK_FIELD_NAME,
    LAST_DEADLINE_TEAM_VALUE_FIELD_NAME,
    LAST_DEADLINE_TOTAL_TRANSFERS_FIELD_NAME,
)
# todo overall and poland rank


class TeamStatisticsProvider:
    TEAM_REQUEST_TEMPLATE = Template(
        "https://fantasy.premierleague.com/api/entry/$team_entry/"
    )
    NO_STATISTIC_VALUE = 0
    DIVISION_FACTOR = 10

    @classmethod
    def _get_value_divided_by_factor(cls, value) -> float:
        return value / cls.DIVISION_FACTOR

    @classmethod
    def _get_formatted_rank_value(cls, rank_value) -> str:
        formatted_rank_value = ""
        for character_position, character in enumerate(reversed(str(rank_value))):
            formatted_rank_value = character + formatted_rank_value
            if (character_position + 1) % 3 == 0:
                formatted_rank_value = " " + formatted_rank_value
        return formatted_rank_value

    @classmethod
    def _get_team_value(cls, team_info: Dict[str, Any]) -> float:
        team_value = team_info.get(LAST_DEADLINE_TEAM_VALUE_FIELD_NAME)
        if team_value:
            return cls._get_value_divided_by_factor(team_value)
        return cls.NO_STATISTIC_VALUE

    @classmethod
    def _get_team_bank_value(cls, team_info: Dict[str, Any]) -> float:
        bank_value = team_info.get(LAST_DEADLINE_BANK_FIELD_NAME)
        if bank_value:
            return cls._get_value_divided_by_factor(bank_value)
        return cls.NO_STATISTIC_VALUE

    @classmethod
    def _get_total_transfers(cls, team_info: Dict[str, Any]) -> int:
        return team_info.get(LAST_DEADLINE_TOTAL_TRANSFERS_FIELD_NAME)

    @classmethod
    def _get_summary_overall_points(cls, team_info: Dict[str, Any]):
        return team_info.get(SUMMARY_OVERALL_POINTS)

    @classmethod
    def _get_summary_overall_rank(cls, team_info: Dict[str, Any]):
        return cls._get_formatted_rank_value(team_info.get(SUMMARY_OVERALL_RANK))

    @classmethod
    def _get_summary_event_points(cls, team_info: Dict[str, Any]):
        return team_info.get(SUMMARY_EVENT_POINTS)

    @classmethod
    def _get_summary_event_rank(cls, team_info: Dict[str, Any]):
        return cls._get_formatted_rank_value(team_info.get(SUMMARY_EVENT_RANK))

    @classmethod
    def get_basic_team_statistics(cls, team_name: str, team_entry: int) -> Dict[str, Any]:
        response = requests.get(
            cls.TEAM_REQUEST_TEMPLATE.substitute(team_entry=team_entry)
        )
        team_info = json.loads(response.text)
        team_statistics = {
            TEAM_NAME_FIELD_NAME: team_name,
            SUMMARY_OVERALL_POINTS: cls._get_summary_overall_points(team_info),
            SUMMARY_OVERALL_RANK: cls._get_summary_overall_rank(team_info),
            SUMMARY_EVENT_POINTS: cls._get_summary_event_points(team_info),
            SUMMARY_EVENT_RANK: cls._get_summary_event_rank(team_info),
            LAST_DEADLINE_BANK_FIELD_NAME: cls._get_team_bank_value(team_info),
            LAST_DEADLINE_TEAM_VALUE_FIELD_NAME: cls._get_team_value(team_info),
            LAST_DEADLINE_TOTAL_TRANSFERS_FIELD_NAME: cls._get_total_transfers(team_info),
        }
        return team_statistics
