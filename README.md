# fpl_info_provider

This microproject enables you to get and print current standings and statistics for specific league from the official "Fantasy Premier League" game [https://fantasy.premierleague.com/].

The API urls have been found here: https://www.reddit.com/r/FantasyPL/comments/c64rrx/fpl_api_url_has_been_changed/

> **_NOTE:_**  fpl_info_provider will work as long as the API remains unchanged. Otherwise, one may expect errors connected with API modification.

## Table of contents
* [Technologies used in the project](#technologies_used)
* [Entry point](#entry_point)

## <a name="technologies_used"></a>Technologies used in the project
* Python 3.8

## <a name="entry_point">Entry point
In order to get the standings and statistics for specific league simply run 

`show_league_statistics.py ---league_entry=$YOUR_LEAGUE_ENTRY`

YOUR_LEAGUE_ENTRY is a unique code for every league, which you can get from url, after you click on one of your leagues on https://fantasy.premierleague.com/leagues level.
After you are redirected to league page, you will see https://fantasy.premierleague.com/leagues/YOUR_LEAGUE_ENTRY/standings/c url in your browser.
