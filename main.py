from RiotAPI import RiotAPI
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

	# get summoner info based on summoner name
	r = api.get_summoner_by_name(SumName)
	print ("\nPrinting summoner info:")
	print r # printing the whole JSON dictionary

	# get current game info, WIP
	# need to strip spaces for SumName for the correct key value in the returned JSON dictionary
	SumName = SumName.replace(" ", "")
	# grab the summoner's id
	sumId = r[SumName]['id']
	# eventually, add a PlatformID variable so that other regions can use this program
	r = api.get_current_game(sumId)
	print ("\nPrinting current game info:")
	print r

	# get a summary of stats from the summoner, prints are commented because of the sheer amount of info
	r = api.get_player_stats(sumId)
	#print ("\nPrinting out summoner stats:")
	#print r


if __name__ == "__main__":
	main()