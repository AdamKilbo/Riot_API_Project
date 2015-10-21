# elements within brackets are similar to variables
URL = {
	'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
	'summoner_by_name': 'v{version}/summoner/by-name/{names}',
	'summoner_stats': 'v{version}/stats/by-summoner/{summonerId}/summary',

	'current_game_base': 'https://{proxy}.api.pvp.net/{url}',
	'current_game': 'observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}'
}

API_VERSIONS = {
	'summoner': '1.4',
	'current_game': '1.0',
	'summoner_stats': '1.3'
}

REGIONS = {
	'europe_nordic_and_east': 'eune',
	'europe_west': 'euw',
	'north_america': 'na',
	'korea': 'kr'
}

# used for current game request
PLATFORM_ID = {
	'north_america': 'NA1'
}