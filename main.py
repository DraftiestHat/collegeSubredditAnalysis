#!/usr/bin/python3
import praw
import pprint
import string
import shlex
import json
import time
from datetime import date
from pygraph.classes.graph import graph
from pygraph.algorithms.searching import depth_first_search

lim = 5
exclude = set(string.punctuation)
subswords = dict()

#read in 500 most common words to set
a = open('topwords.txt').read().lower().splitlines()
common = set(a)

#read in dictionary to set
b = open('dict.txt').read().lower().splitlines()
dict = set(b)

#get list of subreddits
subredditList = open('uscolleges.txt').read().splitlines()
subredditsSet = set(subredditList)

#for reddit API
r = praw.Reddit('College Subreddit Text Analysis by u/DraftiestHat')

for subreddit in subredditsSet:
	words = set()
	sub = r.get_subreddit(subreddit)
	submissions = sub.get_top(limit=lim)
	#gets all the submissions (that we can ) in a subreddit
	for submission in submissions:
		if(len(submission.comments) > 0):
			#reads each comment
			for s in submission.comments:
				#remove punctuation and put lower case
				comment = s.translate(string.maketrans("",""),exclude).lower()
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
				
				words.add(sorted(splitSet))
				
	subswords[subreddit] = words
	
today = date.today()
fileName = '' + today.year + today.month + today.day + 'subToWordDict.txt'
json.dump(subswords, open(fileName,'w'))		

	
	

