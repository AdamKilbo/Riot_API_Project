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
	print ("\nPrinting summoner info:")
	#the json.dumps function formats the print of the JSON dict
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

		MostRecentGame = False
		MostRecentGameID = 0

		#print r

		i = 0 # this keeps track of which of the ten games were are analyzing. Since there may be aram or bot games in a match history, we are trying to remove those. 
		# i is the iterator which keeps track of what element we are on. 
		for Game, GameInfo in r.iteritems():
			print Game
			for InnerKey, InnerValue in r.iteritems():
				print InnerKey
				print 'check\n', Game
				if InnerValue == 'gameMode':
					print 'in gameMode'
					if (InnerValue != 'Classic'):
						r['games'].pop[i]
				elif InnerValue == 'subType':
					print 'in subType'
					# only counting the game towards our statistics if it is a normal or ranked game of any type
					if (InnerValue != 'NORMAL' or 'NORMAL_5x5_BLIND' or 'NORMAL_5x5_DRAFT' or 'RANKED_SOLO_5x5' or 'RANKED_TEAM_5x5' or 'RANKED_PREMADE_5x5'):
						r['games'].pop[i]
				else:
					print "incrementing", i
					# this is a game we want to collect statistics on, do not delete it, move onto the next element in dictionary
					i += 1
				if (InnerValue == 'championId'):
					print("Champion Name: ", api.get_champion_name(InnerValue))	

		print ("Printing JSON (summonersrift, normal/ranked, classic):")
		#print json.dumps(r, indent = 2, sort_keys=False)
		print i

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