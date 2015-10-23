# elements within brackets are similar to variables, replaced with arguemnts
URL = {
	'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
	'summoner_by_name': 'v{version}/summoner/by-name/{names}',
	'summoner_stats': 'v{version}/stats/by-summoner/{summonerId}/summary',
	'recent_games': 'v{version}/game/by-summoner/{summonerId}/recent',

	'current_game_base': 'https://{proxy}.api.pvp.net/{url}',
	'current_game': 'observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}'
}

API_VERSIONS = {
	'summoner': '1.4',
	'current_game': '1.0',
	'summoner_stats': '1.3',
	'recent_games': '1.3'
}

REGIONS = {
	'brazil': 'br',
	'europe_nordic_and_east': 'eune',
	'europe_west': 'euw',
	'korea': 'kr',
	'latin_america_north': 'lan',
	'latin_america_south': 'las',
	'north_america': 'na',
	'oceana': 'oce',
	'russia': 'ru',
	'turkey': 'tr'
}

# used for current game request
PLATFORM_ID = {
	'north_america': 'NA1'
}