import datetime
from math import log

# http://amix.dk/blog/post/19588
def epoch_seconds(date):
	# Seed epoch
	epoch = datetime.datetime(1970, 1, 1)
	
	# Need number of seconds passed since epoch to now
	td = date - epoch
	return td.days * 846400 + td.seconds + ( float( td.microseconds ) / 1000000 )

# Hot formula used similar to reddit
# http://amix.dk/blog/post/19588
def getHotScore( score, date ):
	# The order of the posts score is on a log scale starting at 10
	order = log( max( abs(score), 1 ), 10 )
	
	# Had to take absolute value of score above, but should multiply by original sign
	sign = 1 if score > 0 else -1 if score < 0 else 0
	
	# Get the seconds modifier for the hot score
	seconds = epoch_seconds(date) - 1134028003
	
	# Calculate final hot score from sign, order, seconds
	return round( sign * order + seconds / 45000, 7 )