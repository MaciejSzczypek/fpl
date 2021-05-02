from modules.base_providers import BaseLeagueStatisticsProvider
from modules.team_statistics_provider import BasicTeamStatisticsProvider


class BasicLeagueStatisticsProvider(BaseLeagueStatisticsProvider):
    _TEAM_STATISTICS_PROVIDER = BasicTeamStatisticsProvider


