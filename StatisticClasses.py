
# a class that holds a JSON dictionary, since python doesn't have pointers we use a class whose value we can manipulate from different locations and have persistent data changes
class JSONDictionary(object):
	def __init__(self, Dict):
		self.JSONDict = Dict

	def ReturnDictionary(self):
		return JSONDict

	# prints this class' self.JSONDict
	def PrintDictionary(self, Dictionary):
		print json.dumps(self.JSONDict, indent = 2, sort_keys=False)

	# prints any JSON passed as an argument
	def PrintOtherDictionary(self, Dictionary):
		print json.dumps(Dictionary, indent = 2, sort_keys=False)

# this class holds statistics on number of games each champion has played and won. By using these two numbers we can calculate winrate statistics
class ChampionWinrateStatistics(object):

	ChampionIDDictionary = [None]*123
	ChampionWins = [None]*123
	ChampionGames = [None]*123

	def DoesChampionExist(self, ChampionID):
		if (self.ChampionIDDictionary[ChampionID]):
			return True
		else:
			return False

	def ReturnGames(self, ChampionID):
		if (self.ChampionGames(ChampionID)):
			return self,ChampionGames[ChampionID]
		else:
			return 0

	def ReturnWins(self, ChampionID):
		if (self.ChampionWins[ChampionID]):
			return self.ChampionWins[ChampionID]
		else:
			return 0

	def AddChampion(self, ChampionID):
		self.ChampionIDDictionary[ChampionID] = ChampionID

	def IncrementGames(self, ChampionID):
		if (self.ChampionIDDictionary[ChampionID]):
			if (self.ChampionGames[ChampionID]):
			# if champion has been seen before, increment number of games by one
				ChampionGames[ChampionID] += 1
			else:
			# champion not seen before, initialize element
				self.ChampionGames[ChampionID] = 1

	def IncrementWins(self, ChampionID):
		if (self.ChampionIDDictionary[ChampionID]):
			if (self.ChampionWins[ChampionID]):
			# if champion has been seen before, increment number of wins by one
				self.ChampionWins[ChampionID] += 1
				print("Champion win percentage for ", ChampionID, " is ", self.ChampionGames[ChampionID]/self.ChampionWins[ChampionID])
			else:
			# champion not seen before, initialize element
				self.ChampionWins[ChampionID] = 1




# This class holds a hash table for keeping track of which players we have seen and their last game id.
# by keeping track of their last game id that we have seen, we will not take duplicate game information.

class PlayerDictionary(object):
	PlayerIDArray = [None]*90000000 #how to store 60+ million is a problem. computer cannot handle 600 million when initializing this array
	PlayerLastGameDictionary = [None]*90000000

	# method to determine if we have encountered this player before
	def DoesPlayerExist(self, SummonerID):
		# if we have encountered player before, return true, else return false
		if (self.PlayerIDArray[SummonerID]):
			return True
		else:
			return False

	# see if a player is in the dictionary. If yes, record most recent game ID so we don't double count games.
	# if a player is not in hash, store them and record most recent game
	# by recording most recent game ID, if we encounter a summoner again we will not double count games we have seen before for our statistics.
	def UpdatePlayer(self, SummonerID, MostRecentGameID):
		if (self.PlayerIDArray[SummonerID]):
			# summoner seen before
			print ("summoner seen before")
			# update recent game id
			self.PlayerLastGameDictionary[SummonerID] = MostRecentGameID
		else:
			# summoner not seen before
			if SummonerID > 80000000:
				print "problem, greater than 80 mil"

			print ("summoner not seen before, adding to dictionary")
			# add id to hash, update recent game id
			self.PlayerIDArray[SummonerID] = SummonerID
			self.PlayerLastGameDictionary[SummonerID] = MostRecentGameID

	# return players most recent game IDa
	def GetMostRecentMatchID(self, SummonerID):
		# if player exists (we have encountered him before, then return his most recent game id
		if (self.PlayerIDArray[SummonerID]):
			return self.PlayerLastGameDictionary[SummonerID]


class SummonerIDsToExplore(object):
	# This bool is so that we stop adding player IDs after a certain array length is met.
	ArrayTooBig = False
	PlayerIDArray = [] # start empty, add IDs as the program progresses

	def __init__(self):
		self.ArrayTooBig = False

	def AddIDToExplore(self, SummonerID):
		ArraySize = len(self.PlayerIDArray)
		# check to see if ID is in array, if yes, don't add it
		# length of array capped at 1000 so that it does not expand infinitely
		if (ArraySize > 500):
			ArrayTooBig = True
			# set to true, let the array length fall for a while before adding more IDs
		elif (ArraySize < 20):
			ArrayTooBig = False
			# array length  has fallen enough, start adding more IDs

		if (SummonerID not in self.PlayerIDArray and self.ArrayTooBig == False):
			self.PlayerIDArray.append(SummonerID)
		#print "current ID array: ", self.PlayerIDArray

	def GetSummonerIDToExplore(self):
		SummonerID = self.PlayerIDArray.pop(0)
		return SummonerID