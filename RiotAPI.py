import requests
import RiotConsts as Consts
import time

# no inheritance
class RiotAPI(object): 

	# if no regions are specified, automatically chose north_america
	def __init__(self, api_key, region=Consts.REGIONS['north_america']):

		# initializing variables
		# your api key
		self.api_key = api_key
		# your region
		self.region = region

	# if no paramaters specified, params is empty
	def _request(self, api_url, params={}):

		args = {'api_key': self.api_key}
		# unpack params.items dictionary into key & value
		for key, value in params.items():
		 	if key not in args:
		 		args[key] = value
		response = requests.get(
			Consts.URL['base'].format(
				# server you want to access for info
				proxy=self.region,
				# region to grab info from
				region=self.region,
				url=api_url
				),
			params=args 
			)
		# prints out the http request:
		print ("\n")
		print response.url
		# return JSON dictionary. At this point we should parse for status codes (ex: 404 code)
		time.sleep(1.2) # the delay here is to make sure that I do not cross API request limits (10 per 10 secs, 500 per 10 minutes)
		return response.json()

	#retrieve info on a summoner using a name
	def get_summoner_by_name(self, name):

		api_url = Consts.URL['summoner_by_name'].format(
			# assigning variables
			version=Consts.API_VERSIONS['summoner'],
			names=name
		)
		return self._request(api_url)

	# get player statistics (non ranked)
	def get_player_stats(self, sumId):

		api_url = Consts.URL['summoner_stats'].format(
			# assigning variables
			summonerId=sumId,
			version=Consts.API_VERSIONS['summoner_stats']
		)
		return self._request(api_url)

	# get recent game info. only returns info on individual summoner
	def get_recent_games(self, sumId):

		api_url = Consts.URL['recent_games'].format(
			# assigning variables
			summonerId=sumId,
			version=Consts.API_VERSIONS['recent_games']
		)
		return self._request(api_url)

	# get player statistics (ranked), WIP
	#def get_player_stats_ranked


	def _request_champion_name(self, api_url, params={}):

		args = {'api_key': self.api_key}
		# unpack params.items dictionary into key & value
		for key, value in params.items():
		 	if key not in args:
		 		args[key] = value
		response = requests.get(
			Consts.URL['champion_name_base'].format(
				# server you want to access for info
				proxy=self.region,
				# region to grab info from
				region=self.region,
				url=api_url
				),
			params=args 
			)
		# prints out the http request:
		print ("\n")
		print response.url
		# return JSON dictionary. At this point we should parse for status codes (ex: 404 code)
		# no delay here, does not count against rate limit
		return response.json()

	# function to get champion name based on champion ID
	def get_champion_name(self, ChampionId):

		api_url = Consts.URL['champion_name'].format(
			#assigning variables
			championId=ChampionId,
			version=Consts.API_VERSIONS['champion_name']
		)
		# only returning champion name, culling JSON dict for name only
		returnedDict = self._request_champion_name(api_url)
		#print returnedDict
		return returnedDict


	# current game is a slightly different beast, its request is different. Therefore it has its own class

	# request for current game
	def _request_current_game(self, api_url, params={}):

		args = {'api_key': self.api_key}
		# unpack params.items dictionary into key & value
		for key, value in params.items():
		 	if key not in args:
		 		args[key] = value
		response = requests.get(
			Consts.URL['current_game_base'].format(
				# server you want to access for info
				proxy=self.region,
				url=api_url
				),
			params=args 
			)
		# prints out the http request:
		print ("\n")
		print response.url
		time.sleep(1.2) # delay to make sure we don't cross API limits (10 reqeusts per 10 secs, 500 per 10 minutes)
		# return JSON dictionary. At this point we should parse for status codes (ex: 404 code). In this scenario, if the summoner requested is not currently in a game, the program crashes (add a parser for this case).
		return response.json()

	# get info on current game
	def get_current_game(self, sumId, platformId=Consts.PLATFORM_ID['north_america']):

		api_url = Consts.URL['current_game'].format(
			#assigning variables
			version=Consts.API_VERSIONS['current_game'],
			summonerId=sumId,
			# currently hard coded to get NA summoners only, in future can add more regions
			platformId='NA1'
		)
		return self._request_current_game(api_url) # unique, calls to a different request because the url is different.