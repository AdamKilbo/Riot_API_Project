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

	api = RiotAPI('') # Your API key goes inbetween the blank quotes.

	#
	# REMEMBER TO REMOVE YOUR API KEY WHEN YOU PUSH REPO
	#

	print ("enter your summoner name")
	SumName = 'golden foxes'#raw_input() currently 'golden foxes' for debuggin faster
	# get summoner info based on summoner name. all info is stored as a JSON dictionary in the variable r
	r = api.get_summoner_by_name(SumName) 
	#print ("\nPrinting summoner info:")
	#the json.dumps function formats the print of the JSON dict
	#print json.dumps(r, indent = 2, sort_keys=False) # printing the whole JSON dictionary

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
	# 3) store summoner id in dictionary. Additionally, keep info on that summoners latest game id (so if we encounter him again we dont recount games) (PlayerDictionary)
	# 4) get summoner id on each summoner in that particular game, repeat the above steps for each of them. (SummonerIDsToExplore)
	#
	"""


	### WIP. This is likely to be its own function in a separate file

	# This function crawls for champion winrate info. 

	# Scrape_Info() # code is as follows beneath

	ClassSummonerIDsToExplore.AddIDToExplore(SummonerId)

	while (True):
		r = api.get_recent_games(ClassSummonerIDsToExplore.GetSummonerIDToExplore())

		SummonerId = r['summonerId']

		MostRecentGame = False
		MostRecentGameID = 0


		# this keeps track of which of the ten games were are analyzing. Since there may be aram or bot games in a match history, we are trying to remove those. 
		# i is the iterator which keeps track of what element we are on.
		IgnoreElement = [False for i in range(0, 10)]
		for i in range(0, 10):
			e = r['games'][i]
			for key, val in e.items():
				if key == 'gameMode':
					if val != 'CLASSIC':
						# not a summoners rift variant we are interested in
						IgnoreElement[i] = True
				if key == 'subType':
					if val == 'NORMAL' or val == 'RANKED_SOLO_5x5' or val == 'RANKED_TEAM_5x5':
						# not normal or ranked. Could be other (ex: one for all, URF)
						IgnoreElement[i] = True
				if key == 'mapId':
					if val != 11: # note, this works without having 11 in quotes.
						# not summoners rift
						IgnoreElement[i] = True



		# parse for info based on the games that meet our previous criteria
		for i in range(0, 10):
			if IgnoreElement[i] == False: # False means game meets our criteria, parsing for info

				# e is a sub dictionary within r, makes parsing through it much easier
				e = r['games'][i]

				###
				# This block will determine which team won (team 100 or 200) and set the bools accordingly
				# Make this its own object. pass PlayerTeam, PlayerWin, Win100, Win200. return win100, win200.
				PlayerTeam = e['teamId'] # a bool that will keep track of whether the game was a win or not
				PlayerWin = e['stats']['win'] # a integer value that will keep track of which team the player was on
				#Win100 # bool that keeps track of whether or not team ID 100 won
				#Win200 # see above, team 200


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

				for key, val in e.items():
					if key == 'gameId':
						if MostRecentGame == False: 
							# the first game id we encounter will be the most recent one. Therefore declare the bool MostRecentGame True upon reaching this loop
							MostRecentGame = True
							#### to add: update player w/ game id ####
							# val = gameID
							ClassPlayerDictionary.UpdatePlayer(SummonerId, val)
					if key == 'championId':
						ChampionInfoDict = api.get_champion_name(val)
						print "Champion Name: ", ChampionInfoDict['name']
					#### add collection of this player's win/loss on champ ####

				print "yo"

				# this will go through the fellow players dictionaries and scrape stats there
				for j in range(0, 9): # 9 other players in the game assuming classical mode on summoner's rift
					# f is a sub dictionary within r. makes parsing through it much easier
					f = r['games'][i]['fellowPlayers'][j]
					for key, val in f.items():
						if key == 'summonerId':
							ClassSummonerIDsToExplore.AddIDToExplore(val)
						if key == 'championId':
							ChampionInfoDict = api.get_champion_name(val)
							print "Champion Name: ", ChampionInfoDict['name']
						#### also collect champ winrate stats here on other player's champs in the game ####



		#if (Value == 'championId'):
		#print("Champion Name: ", api.get_champion_name(InnerValue))	

		#print ("Printing JSON (summonersrift, normal/ranked, classic):")
		#print json.dumps(r, indent = 2, sort_keys=False)

		return 0
"""

		SummonerID = r['summonerId']
		# the games that are left are ones we want to collect date from.
		# scraping info from the JSON dictionary
		for Game, GameInfo in r.items(): # for (key), (value of key in dictionary) in our dictionary:
			#check to see if the game played was normal or ranked on summoners rift
			for key, value in gameInfo.items():
				if key == 'gameId':
					# check to see if we have pulled a game id. we only update the first MostRecentGameID with the first gameId encountered because it will be the most recent game played.
					if (MostRecentGame == False):
						MostRecentGame = True
						MostRecentGameID = value

"""

	### END WIP




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


if __name__ == "__main__":
	main()