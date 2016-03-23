#!/usr/bin/python3
import praw
import pprint
import string
import shlex
from pygraph.classes.graph import graph
from pygraph.algorithms.searching import depth_first_search

lim = 5
exclude = set(string.punctuation)
subswords = []

#read in 500 most common words to set

#read in dictionary to set


#get list of subreddits
lines = open('uscolleges.txt').read().splitlines()
s = set(lines)
nodes = list(s)

#for reddit API
r = praw.Reddit('College Subreddit Text Analysis by u/DraftiestHat')

for subreddit in lines:
	words = set()
	sub = r.get_subreddit(subreddit)
	submissions = sub.get_top(limit=lim)
	#gets all the submissions (that we can ) in a subreddit
	for submission in submissions:
		if(len(submission.comments) > 0):
			#reads each comment
			for s in submission.comments:
				comment = s.translate(string.maketrans("",""),string.punctuation)
				#TODO: put all letters to lowercase
				splitted = shlex.split(comment)
				#remove all words that are in top 500 words or not in a dictionary
				words.add(splitted)
	subswords.append(list(words))

