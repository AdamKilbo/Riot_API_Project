##########################################################################################################################
#
#
# StatisticClasses.py, a file that holds class definitions for classes that collect statistics.
#
# JSONDictionary: Currently unused, Holds a JSON dictionary, makes it easier to pass a JSON dictionary to where it is 
#  needed.
#
# ChampionWinrateStatistics: A class that has two arrays. One array holds the amount of games that a certain champion 
#  was seen in. The other array holds the amount of wins that the champion has. By knowing these two numbers we can 
#  calculate the champion's winrate.
# 
# PlayerDictionary: A class that holds all of the summoner IDs that we have explored. It holds an array that tells us
#  the most recent match that the summoner has competed in (ranked, or normal summoners rift). By knowing the most recent
#  match we will avoid double counting games if we encounter the summoner again.
#
# SummonerIDsToExplore: A class that holds an array of summoner IDs. When prompted, it will either put a summoner ID that
#  we encountered into the array, or give us a summoner ID for us to explore for match history information.
#
#
##########################################################################################################################


# This class holds statistics on number of games each champion has played and won. By using these two numbers we can calculate winrate statistics

class ChampionWinrateStatistics(object):
	
	# each champion has a unique ID. However they are not 1-(current # of champs), instead they are non sequential. However no champ ID goes above 300, so we initialize arrays with the size of 300.
	ChampionWins = [0]*500
	ChampionGames = [0]*500

	def ReturnGames(self, ChampionID):
		
		return self.ChampionGames[ChampionID]

	def ReturnWins(self, ChampionID):
		
		return self.ChampionWins[ChampionID]

	def IncrementGames(self, ChampionID):
		
		self.ChampionGames[ChampionID] += 1

		# print winrate info
		games = self.ChampionGames[ChampionID]
		wins = self.ChampionWins[ChampionID]
		print "Champion Id: ", ChampionID, " has ", games, " games and ", wins, " wins"

	def IncrementWins(self, ChampionID):
		
		self.ChampionWins[ChampionID] += 1

	def PrintWinrateStatistics(self, ChampionID):

		games = self.ChampionGames[ChampionID]
		wins = self.ChampionWins[ChampionID]
		if games > 0:
			print "champion: ", ChampionID, ", winrate: ", wins/games, " percent"


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
			#print ("summoner seen before")
			# update recent game id
			self.PlayerLastGameDictionary[SummonerID] = MostRecentGameID
		else:
			# summoner not seen before
			if SummonerID > 80000000:
				print "problem, greater than 80 mil"
				# So far I have not seen any summoner ID's greater than the number above. If the above message prints out then increase the size of the player ID array.

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
	
	ArrayTooBig = False # This bool is so that we stop adding player IDs after a certain array length is met.
	PlayerIDArray = [] # start empty, add IDs as the program progresses

	def __init__(self):
		
		self.ArrayTooBig = False

	def AddIDToExplore(self, SummonerID):
		
		ArraySize = len(self.PlayerIDArray)
		# check to see if ID is in array, if yes, don't add it
		# length of array capped at 1000 so that it does not expand infinitely
		if ArraySize > 500:
			self.ArrayTooBig = True
			#print "too big, not accepting new data"
			# set to true, let the array length fall for a while before adding more IDs
		elif ArraySize < 40:
			self.ArrayTooBig = False
			#print "too small, adding data"
			# array length  has fallen enough, start adding more IDs

		if (SummonerID not in self.PlayerIDArray) and (self.ArrayTooBig == False):
			self.PlayerIDArray.insert(0, SummonerID)
			# Not the most efficient algorithm, implement FIFO queue when I get the chance
			#print "current ID array: ", self.PlayerIDArray
		#if SummonerID in self.PlayerIDArray: #DEBUGGING IF
			#ignoring summoner, id already in array and ready to explore
			#print "summoner id in array already, ignoring"

	def GetSummonerIDToExplore(self):
		
		SummonerID = self.PlayerIDArray.pop()
		return SummonerID
