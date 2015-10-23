


# This class holds a hash table for keeping track of which players we have seen and their last game id.
# by keeping track of their last game id that we have seen, we will not take duplicate game information.

class PlayerHash(object):
	# 60 million is a very conservative number for the amount of players on one server. Actual stats are unknown.
	PlayerIdHash[60,000,000]
	PlayerLastGame[60,000,000]

	# see if a player is in the hash table. If yes, return most recent game ID so we don't double count games.
	# if a player is not in hash, store them and record most recent game
	# by recording most recent game ID, if we encounter a summoner again we will not double count games we have seen before for our statistics.
	def HashPlayer(SummonerID, MostRecentGameID):
		HashValue = hash(SummonerID) % 60,000,000 # mod 60 million because thats the size of the array
		if (PlayerIdHash[HashValue]):
			# summoner seen before
			print ("summoner seen before")
			# update recent game id
			PlayerLastGame[HashValue] = MostRecentGameID
		else
			# summoner not seen before
			print ("summoner not seen before")
			# add id to hash, update recent game id
			PlayerIdHash[HashValue] = SummonerID
			PlayerLastGame[HashValue] = MostRecentGameID