from RiotAPI import RiotAPI
import StatisticClasses
import json

def main():

	#
	# REMEMBER TO REMOVE YOUR API KEY WHEN YOU PUSH REPO
	#

	api = RiotAPI('') # Your API key goes inbetween the blank quotes.

	#
	# REMEMBER TO REMOVE YOUR API KEY WHEN YOU PUSH REPO
	#

	print ("enter your summoner name")
	SumName = raw_input()
	# get summoner info based on summoner name. all info is stored as a JSON dictionary in the variable r
	r = api.get_summoner_by_name(SumName)
	print ("\nPrinting summoner info:")
	#the json.dumps function formats the print of the JSON dict
	print json.dumps(r, indent = 2, sort_keys=False) # printing the whole JSON dictionary

	# riot uses the summoner name w/o spaces as a key value in its JSON dictionaries. Since we no longer need the space, taking it out.
	SumName = SumName.replace(" ", "")
	# grab the summoner id from the json dictionary
	SumId = r[SumName]['id']

	# # get recent game history
	# r = api.get_recent_games(SumId)
	# print ("\nPrinting recent game info:")
	# print json.dumps(r, indent = 2, sort_keys=False)

	"""
	#
	# Psuedocode for scraping games for champion win rate info:
	# 1) start with any summoner (id or name -> id)
	# 2) get info on match history
	# 	 - Record which chmpions were in game (champion id), whether or not that champion won, and increment the total games we have seen that particular champion in
	# 3) store summoner id in hash array. Additionally, keep info on that summoners latest game id (so if we encounter him again we dont recount games)
	# 4) get summoner id on each summoner in that particular game, repeat the above steps for each of them
	#
	"""

	# 123 champions currently.
	NumberOfChampions = 123
	# to keep track of a champion's win rate, we need to keep track of their Id, their wins, and total games. Win rate can be calculated for each champion with these stats
	ChampionId[NumberOfChampions]
	ChampionWins[NumberOfChampions]
	ChampionGames[NumberOfChampions]



	###

	Scrape_Info()

	while (True)
		r = api.get_recent_games(SumId)

		MostRecentGame = False
		MostRecentGameID = 0

		i = 0 # this keeps track of which of the ten games were are analyzing. Since there may be aram or bot games in a match history, we are trying to remove those. 
		# i is the iterator which keeps track of what element we are on. 
		for Game, GameInfo in r.items():
			for Key, Value in GamInfo.items():
				if Key == 'gameMode':
					if Value != 'Classic':
						r.pop[i]
				else if Key == 'subType':
					# only counting the game towards our statistics if it is a normal or ranked game of any type
					if Value != 'NORMAL' or 'NORMAL_5x5_BLIND' or 'NORMAL_5x5_DRAFT' or 'RANKED_SOLO_5x5' or 'RANKED_TEAM_5x5' or 'RANKED_PREMADE_5x5':
						r.pop[i]
				else
					# this is a game we want to collect statistics on, do not delete it, move onto the next element in dictionary
					i++

		# the games that are left are ones we want to collect date from.
		# scraping info from the JSON dictionary
		for Game, GameInfo in r.items(): # for (key), (value of key in dictionary) in our dictionary:
			#check to see if the game played was normal or ranked on summoners rift
			for key, value in gameInfo.items():
				if key == 'gameId':
					# check to see if we have pulled a game id. we only update the first MostRecentGameID with the first gameId encountered because it will be the most recent game played.
					if (MostRecentGame = False)
						MostRecentGameID = value


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


if __name__ == "__main__":
	main()