from collections import defaultdict
from RiotAPI import RiotAPI
import StatisticClasses
import json

ClassSummonerIDsToExplore = StatisticClasses.SummonerIDsToExplore()
ClassChampionWinrateStatistics = StatisticClasses.ChampionWinrateStatistics()
ClassPlayerDictionary = StatisticClasses.PlayerDictionary()

def main():

	#
	# REMEMBER TO REMOVE YOUR API KEY WHEN YOU PUSH REPO. IMMEDIATELY REQUEST A NEW KEY IF YOU FORGET.
	#

	api = RiotAPI('') # Your API key goes inbetween the blank quotes. if you forget to remove your api key, generate a new one.

	#
	# REMEMBER TO REMOVE YOUR API KEY WHEN YOU PUSH REPO. IMMEDIATELY REQUEST A NEW KEY IF YOU FORGET.
	#

	print ("enter your summoner name")
	SumName = raw_input()
	# get summoner info based on summoner name. all info is stored as a JSON dictionary in the variable r
	r = api.get_summoner_by_name(SumName) 
	#print ("\nPrinting summoner info:")
	print json.dumps(r, indent = 2, sort_keys=False) # printing the whole JSON dictionary

	# riot uses the summoner name w/o spaces as a key value in its JSON dictionaries. Since we no longer need the space, we take it out.
	SumName = SumName.replace(" ", "")
	# grab the summoner id from the json dictionary
	SummonerId = r[SumName]['id']

	# # get recent game history
	# r = api.get_recent_games(SumId)
	# print ("\nPrinting recent game info:")
	# print json.dumps(r, indent = 2, sort_keys=False)

	"""
	#
	# Psuedocode for scraping games for champion win rate info:
	# 1) start with any summoner (id or name -> id) (GetSummonerIDToExplore)
	# 2) get info on match history (ChampionWinrateStatistics)
	# 	 - Record which champions were in game (champion id), whether or not that champion won, and increment the total games we have seen that particular champion in
	# 3) store summoner id in an array. Additionally, keep info on that summoners latest game id (so if we encounter him again we dont recount games) (PlayerDictionary)
	# 4) get summoner id on each summoner in that particular game, repeat the above steps for each of them. (SummonerIDsToExplore)
	#
	"""


	### This is likely to be its own function in a separate file

	# This function crawls for champion winrate info. 

	# Scrape_Info() # code is as follows beneath

	ClassSummonerIDsToExplore.AddIDToExplore(SummonerId)

	while True:
		r = api.get_recent_games(ClassSummonerIDsToExplore.GetSummonerIDToExplore())

		SummonerId = r['summonerId']

		MostRecentGame = False
		MostRecentGameID = 0 # the most recent game ID t
		HistoryMostRecentGameID = 0 # if we have seen the summoner before then this stores their most recent game ID

		# if we have seen this summoner before then pull their most recent match ID from our records
		if ClassPlayerDictionary.DoesPlayerExist(SummonerId) == True:
			HistoryMostRecentGameID = ClassPlayerDictionary.GetMostRecentMatchID(SummonerId)



		# This will keep track of what games in the match history we want to ignore. Since there may be aram or bot games in a match history, we are trying to remove those from our win rate analysis. 
		IgnoreElement = [False for i in range(0, 10)]
		for i in range(0, 10):

			e = r['games'][i]
			for key, val in e.items():
				if key == 'gameId':
					if val <= HistoryMostRecentGameID:
						print "ignoring b/c most recent game id", val, " On Record: ", HistoryMostRecentGameID
						# ignore any games that we have seen before (values smaller than the summoner's most recent gameId in our records)
						IgnoreElement[i] = True
				if key == 'gameMode':
					if val != 'CLASSIC':
						#print "ignoring b/c game mode (!= CLASSIC)", val
						# not a summoners rift variant we are interested in
						IgnoreElement[i] = True
				if key == 'subType':
					if val != 'NORMAL' and val != 'RANKED_SOLO_5x5' and val != 'RANKED_TEAM_5x5':
						#print "ignoring b/c sub type (!= NORMAL/RANKED(TEAM/SOLO))", val
						# not normal or ranked. Could be other (ex: one for all, URF)
						IgnoreElement[i] = True
				if key == 'mapId':
					if val != 11: # note, this works without having 11 in quotes.
						#print "ignoring b/c map ID (!= 11)", val
						# not summoners rift
						IgnoreElement[i] = True


		# parse for info based on the games that meet our previous criteria
		for i in range(0, 10):

			# e is a sub dictionary within r, makes parsing through it much easier
			e = r['games'][i]

			PlayerWin = e['stats']['win'] # a bool value that will keep track whether or not the player won

			for key, val in e.items():

				if IgnoreElement[i] == False: # False means game meets our criteria, parsing for info.
					#if key == 'gameId' and val > HistoryMostRecentGameID: # condition to check for, make sure we don't double count games

						if key == 'gameId':
							if MostRecentGame == False: 
								# the first game id we encounter will be the most recent one. Therefore declare the bool MostRecentGame True upon reaching this loop
								MostRecentGame = True
								# updating summoner's most recent game
								ClassPlayerDictionary.UpdatePlayer(SummonerId, val)

						if key == 'championId':
							ChampionInfoDict = api.get_champion_name(val)
							print "Champion Name: ", ChampionInfoDict['name']

							if PlayerWin == True:
								print "Player Won"
								# increment champ games and wins
								ClassChampionWinrateStatistics.IncrementGames(val)
								ClassChampionWinrateStatistics.IncrementWins(val)

							elif PlayerWin == False:
								print "Player Lost"
								# increment champ games
								ClassChampionWinrateStatistics.IncrementGames(val)


			# this will go through the fellow players dictionaries and scrape summoner IDs so that we can run this whole loop on those IDs as well.

			for j in range(0, 9): # 9 other players in the game assuming classical mode on summoner's rift
				# f is a sub dictionary within r. makes parsing through it much easier
				try:
					f = r['games'][i]['fellowPlayers'][j]
					#print f
					for key, val in f.items():
						if key == 'summonerId':
							# adding id to explore later (val)
							ClassSummonerIDsToExplore.AddIDToExplore(val)
						# do not collect champ winrate stats here on other player's champs in the game. We cannot ensure we are not double counting or that we account for all possible data

				except IndexError:
					pass
					# this error may occur due to a game type that is not normal summoners rift (ex: bot games, custom games)
					#print ("index error, out of index, ignoring")
					# do nothing

				except KeyError:
					pass
					# this error may occur due to a game type that is not normal summoners rift (ex: bot games, custom games)
					#print ("key error, key not found, ignoring")
					# do nothing

	### END FUNCTION

	return 0


if __name__ == "__main__":
	main()

"""

to do list: 

shorter class names and variables that reference the class

move the match history algorithm to another file

remove amount of prints to terminal, it looks ugly. Currently useful for debugging but once i confirm it is working I need to remove some of the unneeded stuff

bugs:

not printing out champion winrate



"""

"""
Reflections on current program:

This program does have some limitations due to how it was built
and the information given by the Riot API. For example, being
unable to pull the date of the game means I could be collecting
data on previous patches. Since the program is a crawler and not
looking for the newest game ID's, I cannot determine if I am 
looking at the newest game or going way back in LoL match history
and grabbing irrelevent information, similar to how I don't know
what patch each game is taking place on. 

This program would be great if I could build external files to
hold data already collected, such as champion winrates and most
recent game IDs for summoners. That way, I can have persistnet data
over multiple runs of the program instead of having to build the
data every time I start the program again. 
"""


"""

Code Graveyard:

This is for snippets of code that I may use later but are currently unneeded. Each snippet is in between ### markers


###
	#print json.dumps(r, indent = 2, sort_keys=False)
###


###
	# get current game info
	# grab the summoner's id from the previous request
	# eventually, add a PlatformID variable so that other regions can use this program
	#r = api.get_current_game(sumId)
	#print ("\nPrinting current game info:")
	#print r

	# get a summary of stats from the summoner, prints are commented because of the sheer amount of info
	#r = api.get_player_stats(sumId)
	#print ("\nPrinting out summoner stats:")
	#print r
###


###
	# a class that holds a JSON dictionary, since python doesn't have pointers we use a class whose value we can manipulate from different locations and have persistent data changes

class JSONDictionary(object):
	
	def __init__(self, Dict):
		
		self.JSONDict = Dict

	def ReturnDictionary(self):
		
		return JSONDict

	# prints this class' self.JSONDict
	def PrintDictionary(self, Dictionary):
		
		print json.dumps(self.JSONDict, indent = 2, sort_keys=False)

	# prints any JSON passed as an argumentID
	def PrintOtherDictionary(self, Dictionary):
		
		print json.dumps(Dictionary, indent = 2, sort_keys=False)
###
"""