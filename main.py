from collections import defaultdict
from RiotAPI import RiotAPI
import StatisticClasses
import json

ClassSummonerIDsToExplore = StatisticClasses.SummonerIDsToExplore()
ClassChampionWinrateStatistics = StatisticClasses.ChampionWinrateStatistics()
ClassPlayerDictionary = StatisticClasses.PlayerDictionary()

def main():

	#
	# REMEMBER TO REMOVE YOUR API KEY WHEN YOU PUSH REPO
	#

	api = RiotAPI('5b62dca2-b2ac-4f75-950a-3fa497841837') # Your API key goes inbetween the blank quotes. if you forget to remove your api key, generate a new one.

	#
	# REMEMBER TO REMOVE YOUR API KEY WHEN YOU PUSH REPO
	#

	print ("enter your summoner name")
	SumName = 'golden foxes'#raw_input() currently 'golden foxes' for debugging faster
	# get summoner info based on summoner name. all info is stored as a JSON dictionary in the variable r
	r = api.get_summoner_by_name(SumName) 
	#print ("\nPrinting summoner info:")
	print json.dumps(r, indent = 2, sort_keys=False) # printing the whole JSON dictionary

	# riot uses the summoner name w/o spaces as a key value in its JSON dictionaries. Since we no longer need the space, taking it out.
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


	### WIP. This is likely to be its own function in a separate file

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



		# this keeps track of which of the ten games were are analyzing. Since there may be aram or bot games in a match history, we are trying to remove those. 
		# i is the iterator which keeps track of what element we are on.
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

		# this little blurb will count how many games we are ignoring. debugging.
		#NumOfIgnores = 0
		#for i in range(0,10):
		#	if IgnoreElement[i] == True:
		#		NumOfIgnores += 1
		#print NumOfIgnores

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
							if PlayerWin == True:
								print "Player Won"
								# increment champ games and wins
								ClassChampionWinrateStatistics.IncrementGames(val)
								ClassChampionWinrateStatistics.IncrementWins(val)
								ClassChampionWinrateStatistics.PrintWinrateStatistics(val)
							elif PlayerWin == False:
								print "Player Lost"
								# increment champ games
								ClassChampionWinrateStatistics.IncrementGames(val)
								ClassChampionWinrateStatistics.PrintWinrateStatistics(val)
							#ChampionInfoDict = api.get_champion_name(val)
							#print "Champion Name: ", ChampionInfoDict['name']

			# this will go through the fellow players dictionaries and scrape stats there
			#if IgnoreElement[i] == False:
			for j in range(0, 9): # 9 other players in the game assuming classical mode on summoner's rift
				# f is a sub dictionary within r. makes parsing through it much easier
				try:
					f = r['games'][i]['fellowPlayers'][j]
					#print f
					for key, val in f.items():
						if key == 'summonerId':
							#print "inserting ID: ", val
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

	### END WIP ###

	return 0


if __name__ == "__main__":
	main()

"""
to do list: 

shorter class names and variables that reference the class
move the match history algorithm to another file
implement other options for this program, champion winrate statistics should be one feature of many

bugs:

not printing out champion winrate



"""


"""

Code Graveyard:

This is for snippets of code that I may use later but are currently unneeded

	#print json.dumps(r, indent = 2, sort_keys=False)

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
	# here i was planning to determine which team won when i planned to count other player's champion wins in the same game. no longer needed.
	# This block will determine which team won (team 100 or 200) and set the bools accordingly
	# Make this its own object. pass PlayerTeam, PlayerWin, Win100, Win200. return win100, win200.
	PlayerTeam = e['teamId'] # a bool that will keep track of whether the game was a win or not
	PlayerWin = e['stats']['win'] # a integer value that will keep track of which team the player was on
	Win100 = True # bool that keeps track of whether or not team ID 100 won
	Win200 = True # see above, team 200


	if PlayerWin == True:
		if PlayerTeam == 100: # if player was on team 100 and won, then team 100 won
			Win100 = True
			Win200 = False
		else:                   # else team 200 won
			Win100 = False
			Win200 = True

	elif PlayerWin == False:
		if PlayerTeam == 100: # team 100 lost, set bools accordingly
			Win100 = False
			Win200 = True
		else:					# team 200 lost, set bools accordingly
			Win100 = True
			Win200 = False
	else:
		print "Error determining player winning"
	###


	# here i was planning to collect win rates of other champs in the game, but without enough information i cannot ensure that all games are accounted for and that we are not double counting data
	teamID # a int that keeps track of which team player is on
	if key == 'teamId'
		teamID = val
	if key == 'championId':
		champID = val
		# update champion winrate statistics
		if teamID == 100 and Win100 == True:
			#increment wins and games
		elif teamID == 100 and Win100 == False:
			#increment games
		elif teamID == 200 and Win200 == True:
			#increment wins and games
		elif teamID == 200 and Win200 == False:
			#increment games
		#ChampionInfoDict = api.get_champion_name(val)
		#print "Champion Name: ", ChampionInfoDict['name']
"""