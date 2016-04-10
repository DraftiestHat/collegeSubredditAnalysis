#!/usr/bin/python3
import praw
import pprint
import string
import shlex
import json
import time
import os
from pygraph.algorithms.searching import depth_first_search
from datetime import date

lim = 250
subswords = dict()
test = 0
today = date.today()

while True:
	fileName = '' + str(today.year) + str(today.month) + str(today.day)
	testFileName = fileName + '_' + str(test) + '_' + 'subToWordDict.txt'
	if( not os.path.isfile('./' + testFileName)):
		fileName = testFileName
		break
	test = test + 1

out = open(fileName,'w')


#read in 500 most common words to set
a = open('topwords.txt')
l = a.read().lower().splitlines()
common = set(l)
a.close()

#read in dictionary to set
a = open('dict.txt')
l = a.read().lower().splitlines()
dict = set(l)
a.close()

#get list of subreddits
subredditFile = open('uscolleges.txt')
subredditList = subredditFile.read().splitlines()
subredditsSet = sorted(subredditList)
subredditFile.close()

#for reddit API
r = praw.Reddit('College Subreddit Text Analysis by u/DraftiestHat')

for subreddit in subredditsSet:
	words = set()
	sub = r.get_subreddit(subreddit)
	submissions = sub.get_top(limit=lim)
	time.sleep(5)
	#gets all the submissions (that we can ) in a subreddit
	try:
		for submission in submissions:
			if(len(submission.comments) > 0):
				#reads each comment
				flat_comments = praw.helpers.flatten_tree(submission.comments)

				for x in flat_comments:
					s = x.body
					#remove punctuation and put lower case
					comment = s.translate(str.maketrans("","",string.punctuation)).lower()
					#split into words
					splitList = sorted(shlex.split(comment))
					splitSet = set(splitList)

					#remove all words that are in top 500 words or not in a dictionary
					for w in common:
						if w.lower() in splitSet:
							splitSet.remove(w.lower())

					toremove = []
					for w in splitSet:
						if w not in dict:
							toremove.append(w)

					for w in toremove:
						splitSet.remove(w)

					words.update(splitSet)

		#subswords[subreddit] = words
		out.write(subreddit + ': ' + repr(sorted(words)) + '\n')
	except praw.errors.Forbidden as e:
		print(subreddit + ': Forbidden')
	except praw.errors.InvalidSubreddit as e:
		print(subreddit + ': Invalid Subreddit')
	except AttributeError as e:
		print(subreddit + ': More Comments Error')
#today = date.today()
#fileName = '' + str(today.year) + str(today.month) + str(today.day) + 'subToWordDict.txt'
#out = open(fileName,'w')
out.close()
