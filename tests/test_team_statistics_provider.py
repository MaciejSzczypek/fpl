from typing import Dict, Any
from unittest.mock import Mock, patch

import pytest

from modules.team_statistics_provider import BasicTeamStatisticsProvider

# region TEST_CASE_EMPTY_STATISTICS
TEAM_1_STATISTICS_REQUEST_RESPONSE = {}
TEAM_NAME_1 = "team_name_1"
TEAM_1_ENTRY = 111
EXPECTED_TEAM_1_STATISTICS = {
    "team_name": TEAM_NAME_1,
    "last_deadline_bank": None,
    "last_deadline_total_transfers": None,
    "last_deadline_value": None,
    "summary_event_points": None,
    "summary_event_rank": None,
    "summary_overall_points": None,
    "summary_overall_rank": None
}
TEST_CASE_EMPTY_STATISTICS = [
    TEAM_1_STATISTICS_REQUEST_RESPONSE, TEAM_NAME_1, TEAM_1_ENTRY, EXPECTED_TEAM_1_STATISTICS,
]

# endregion TEST_CASE_EMPTY_STATISTICS

# region TEST_CASE_FULLY_FILLED_STATISTICS
TEAM_2_STATISTICS_REQUEST_RESPONSE = {
    "id": 1,
    "summary_overall_points": 2000,
    "summary_overall_rank": 50000,
    "summary_event_points": 50,
    "summary_event_rank": 1000000,
    "current_event": 34,
    "last_deadline_bank": 50,
    "last_deadline_value": 1050,
    "last_deadline_total_transfers": 25
}

TEAM_NAME_2 = "team_name_2"
TEAM_2_ENTRY = 222
EXPECTED_TEAM_2_STATISTICS = {
    "team_name": TEAM_NAME_2,
    "last_deadline_bank": 5.0,
    "last_deadline_total_transfers": 25,
    "last_deadline_value": 105.0,
    "summary_event_points": 50,
    "summary_event_rank": "1 000 000",
    "summary_overall_points": 2000,
    "summary_overall_rank": "50 000"
}
TEST_CASE_FULLY_FILLED_STATISTICS = [
    TEAM_2_STATISTICS_REQUEST_RESPONSE, TEAM_NAME_2, TEAM_2_ENTRY, EXPECTED_TEAM_2_STATISTICS,
]


# endregion TEST_CASE_FULLY_FILLED_STATISTICS


class TestTeamStatisticsProvider:

    @pytest.mark.parametrize(
        "team_statistics_request_response,team_name,team_entry,expected_team_statistics",
        [TEST_CASE_EMPTY_STATISTICS, TEST_CASE_FULLY_FILLED_STATISTICS]
    )
    @patch("modules.team_statistics_provider.BasicTeamStatisticsProvider._get_team_info")
    def test_get_basic_team_statistics(
            self,
            mocked__get_team_info: Mock,
            team_statistics_request_response: str,
            team_name: str,
            team_entry: int,
            expected_team_statistics: Dict[str, Any],
    ) -> None:
        mocked__get_team_info.return_value = team_statistics_request_response
        team_statistics = BasicTeamStatisticsProvider.get_team_statistics(
            team_name=team_name, team_entry=team_entry
        )
        assert team_statistics == expected_team_statistics
