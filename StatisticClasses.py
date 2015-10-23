
# a class that holds a JSON dictionary, since python doesn't have pointers we use a class whose value we can manipulate from different locations and have persistent data changes
class JSONDictionary():
	JSONdict = NULL

	def ReturnDictionary():
		return JSONdict

class ChampionWinrateStatistics():
	NumberOfChampions = 123

	ChampionID[NumberOfChampions]
	ChampionWins[NumberOfChampions]
	ChampionGames[NumberOfChampions]

	def AddWin():


# This class holds a hash table for keeping track of which players we have seen and their last game id.
# by keeping track of their last game id that we have seen, we will not take duplicate game information.

class PlayerDictionary():
	# 60 million is a very conservative number for the amount of players on one server. Actual stats are unknown.
	PlayerIdDictionary[]
	PlayerLastGameDictionary[]

	# see if a player is in the dictionary. If yes, record most recent game ID so we don't double count games.
	# if a player is not in hash, store them and record most recent game
	# by recording most recent game ID, if we encounter a summoner again we will not double count games we have seen before for our statistics.
	def UpdatePlayer(SummonerID, MostRecentGameID):
		if (PlayerIdDictionary[SummonerID]):
			# summoner seen before
			print ("summoner seen before")
			# update recent game id
			PlayerLastGameDictionary[SummonerID] = MostRecentGameID
		else:
			# summoner not seen before
			print ("summoner not seen before")
			# add id to hash, update recent game id
			PlayerIdDictionary[SummonerID] = SummonerID
			PlayerLastGameDictionary[SummonerID] = MostRecentGameID

		# method to determine if we have encountered this player before
		def DoesPlayerExist(SummonerID):
			# if we have encountered player before, return true, else return false
			if (PlayerIdDictionary[SummonerID]):
				return True
			else:
				return False

		# return players most recent game ID
		def GetMostRecentMatchID(SummonerID):
			# if player exists (we have encountered him before, then return his most recent game id
			if (PlayerIdDictionary[SummonerID])
				return PlayerLastGameDictionary[SummonerID]