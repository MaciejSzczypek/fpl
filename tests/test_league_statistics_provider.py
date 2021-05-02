from typing import Dict, Any, List
from unittest.mock import patch, Mock

import pytest

from modules.league_statistics_provider import LeagueStatisticsProvider

# region constants
LEAGUE_ENTRY = 1000
TEAM_1_STATISTICS_REQUEST_RESPONSE = {
    "id": 1,
    "summary_overall_points": 2000,
    "summary_overall_rank": 1000,
    "summary_event_points": 50,
    "summary_event_rank": 1000,
    "current_event": 34,
    "last_deadline_bank": 50,
    "last_deadline_value": 1050,
    "last_deadline_total_transfers": 25
}
TEAM_2_STATISTICS_REQUEST_RESPONSE = {
    "id": 2,
    "summary_overall_points": 1900,
    "summary_overall_rank": 2000,
    "summary_event_points": 40,
    "summary_event_rank": 2000,
    "current_event": 34,
    "last_deadline_bank": 40,
    "last_deadline_value": 1040,
    "last_deadline_total_transfers": 27
}
TEAM_3_STATISTICS_REQUEST_RESPONSE = {
    "id": 3,
    "summary_overall_points": 1800,
    "summary_overall_rank": 3000,
    "summary_event_points": 25,
    "summary_event_rank": 3000,
    "current_event": 34,
    "last_deadline_bank": 20,
    "last_deadline_value": 1030,
    "last_deadline_total_transfers": 10
}


def _get_team_info_mock(league_entry: int) -> Dict[str, Any]:
    team_entry_to_team_statistics_map = {
        111: TEAM_1_STATISTICS_REQUEST_RESPONSE,
        222: TEAM_2_STATISTICS_REQUEST_RESPONSE,
        333: TEAM_3_STATISTICS_REQUEST_RESPONSE,
    }
    return team_entry_to_team_statistics_map.get(league_entry, {})


# endregion constants
# region TEST_CASE_NO_LEAGUE_PARTICIPANTS
EMPTY_LEAGUE_REQUEST_RESPONSE = {
    "league": {
        "id": LEAGUE_ENTRY,
        "name": "LEAGUE_NAME",
        "created": "2020-09-11T16:02:15.788544Z",
        "has_cup": False,
        "cup_league": None
    },
    "new_entries": {"has_next": False, "page": 1, "results": []},
    "standings": {"has_next": False, "page": 1, "results": []}
}
EXPECTED_EMPTY_LEAGUE_STATISTICS = []
TEST_CASE_NO_LEAGUE_PARTICIPANTS = [
    EMPTY_LEAGUE_REQUEST_RESPONSE, LEAGUE_ENTRY, EXPECTED_EMPTY_LEAGUE_STATISTICS,
]
# endregion TEST_CASE_NO_LEAGUE_PARTICIPANTS
# region TEST_CASE_3_PARTICIPANTS
THREE_PARTICIPANTS_LEAGUE_REQUEST_RESPONSE = {
    "league": {
        "id": LEAGUE_ENTRY,
        "name": "LEAGUE_NAME",
        "created": "2020-09-11T16:02:15.788544Z",
        "has_cup": False,
        "cup_league": None
    },
    "new_entries": {"has_next": False, "page": 1, "results": []},
    "standings": {
        "has_next": False,
        "page": 1,
        "results": [
            {
                "id": 1,
                "event_total": 50,
                "player_name": "A A",
                "rank": 1,
                "last_rank": 1,
                "rank_sort": 1,
                "total": 2000,
                "entry": 111,
                "entry_name": "AA TEAM"
            },
            {
                "id": 2,
                "event_total": 40,
                "player_name": "B B",
                "rank": 2,
                "last_rank": 2,
                "rank_sort": 2,
                "total": 1900, "entry": 222,
                "entry_name": "BB TEAM"
            },
            {
                "id": 3,
                "event_total": 30,
                "player_name": "C C",
                "rank": 3,
                "last_rank": 3,
                "rank_sort": 3,
                "total": 1800, "entry": 333,
                "entry_name": "CC TEAM"
            },
        ]
    }
}
EXPECTED_3_PARTICIPANTS_LEAGUE_STATISTICS = [
    {'last_deadline_bank': 5.0,
     'last_deadline_total_transfers': 25,
     'last_deadline_value': 105.0,
     'summary_event_points': 50,
     'summary_event_rank': '1 000',
     'summary_overall_points': 2000,
     'summary_overall_rank': '1 000',
     'team_name': 'AA TEAM'},
    {'last_deadline_bank': 4.0,
     'last_deadline_total_transfers': 27,
     'last_deadline_value': 104.0,
     'summary_event_points': 40,
     'summary_event_rank': '2 000',
     'summary_overall_points': 1900,
     'summary_overall_rank': '2 000',
     'team_name': 'BB TEAM'},
    {'last_deadline_bank': 2.0,
     'last_deadline_total_transfers': 10,
     'last_deadline_value': 103.0,
     'summary_event_points': 25,
     'summary_event_rank': '3 000',
     'summary_overall_points': 1800,
     'summary_overall_rank': '3 000',
     'team_name': 'CC TEAM'}
]
TEST_CASE_3_PARTICIPANTS = [
    THREE_PARTICIPANTS_LEAGUE_REQUEST_RESPONSE,
    LEAGUE_ENTRY,
    EXPECTED_3_PARTICIPANTS_LEAGUE_STATISTICS,
]


# endregion TEST_CASE_3_PARTICIPANTS


class TestLeagueStatisticsProvider:
    @pytest.mark.parametrize(
        "league_request_response,league_entry,expected_statistics",
        [TEST_CASE_NO_LEAGUE_PARTICIPANTS, TEST_CASE_3_PARTICIPANTS]
    )
    @patch("modules.league_statistics_provider.LeagueStatisticsProvider._get_league_info")
    @patch(
        "modules.team_statistics_provider.TeamStatisticsProvider._get_team_info",
        side_effect=_get_team_info_mock,
    )
    def test_get_teams_statistics_df(
            self,
            mocked__get_team_info: Mock,
            mocked__get_league_info: Mock,
            league_request_response: Dict[str, Any],
            league_entry: int,
            expected_statistics: List[Dict[str, Any]],
    ) -> None:
        mocked__get_league_info.return_value = league_request_response
        league_statistics_provider = LeagueStatisticsProvider(league_entry)
        league_statistics = league_statistics_provider.get_league_statistics()
        assert league_statistics == expected_statistics
