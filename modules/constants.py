from enum import Enum
from string import Template


class FieldName(Enum):
    ENTRY = "entry"
    ENTRY_NAME = "entry_name"
    LAST_DEADLINE_BANK = "last_deadline_bank"
    LAST_DEADLINE_TEAM_VALUE = "last_deadline_value"
    LAST_DEADLINE_TOTAL_TRANSFERS = "last_deadline_total_transfers"
    RESULTS = "results"
    STANDINGS = "standings"
    SUMMARY_EVENT_POINTS = "summary_event_points"
    SUMMARY_EVENT_RANK = "summary_event_rank"
    SUMMARY_OVERALL_POINTS = "summary_overall_points"
    SUMMARY_OVERALL_RANK = "summary_overall_rank"
    TEAM_NAME = "team_name"


LEAGUE_REQUEST_TEMPLATE = Template(
    f"https://fantasy.premierleague.com/api/leagues-classic/$league_entry/standings/"
)
TEAM_REQUEST_TEMPLATE = Template(
    "https://fantasy.premierleague.com/api/entry/$team_entry/"
)
