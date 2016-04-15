
# http://stackoverflow.com/questions/12124275/splitting-a-string-by
#    -capital-letters
import re

# Use sys to exit when unknown/inappropriate input
import sys

# Documentation here: http://www.nltk.org/
# Taken from the open-source NLTK Package, augmented for this problem
from stop_words import stop_words

# Handle profanity by filtering things from bad_words
from profanity import bad_words

import string

import math

# Takes a string, outputs string without punctuation
def depunctuation(s):
	replace_punctuation = string.maketrans(string.punctuation, 
		' '*len(string.punctuation))
	out = s.translate(replace_punctuation)
	return out

# Takes a string, splits the string at capitalized words
def split_upper(s):
    return filter(None, re.split("([A-Z][^A-Z]*)", s))

# Takes in a file name, outputs a keywords_dictionary.
def read_possible_classifications(file_name):
	# open file for reading
	f = open(file_name, 'r')

	# initialize empty dictionary	
	keywords_dictionary = {}

	# for each line, set the dictionary right for likelihoods
	for line in f: 
		current = line.rstrip()
		split_words = map(lambda x:x.lower(), split_upper(current))
		filtered_words = [word for word in split_words if word not in \
			stop_words]
		keywords_dictionary[current] = filtered_words

	# Add unknown method as a potential option. 
	keywords_dictionary["Help"] = ["dont", "know", "unknown", 
		"help", "helping", "hint", "idea"]

	return keywords_dictionary

# Returns a list of important user inputs, and weights for handling "nots"
def take_user_input():
	# take input from stdin
	solve_method = raw_input("How will you solve this problem? ")
	print(["You said: " + solve_method])

	# remove punctuation from string
	solve_method = depunctuation(solve_method)
	# split string by spaces, make lower case
	split_words = map(lambda x:x.lower(), solve_method.split())

	# test for profanity
	test = [1 for word in split_words if word in bad_words]
	if (test):
		sys.exit("Please don't say inappropriate things to me.")

	stop = stop_words;

	filtered_words = [word for word in split_words if word not in stop]
	
	# add a new dictionary of indices of key words from the nots
	word_weights = {}
	# weight all things after a "not" by how far away things are from the "not"
	# in the input. We keep the "not" so that "i do not know" keeps for unknown
	# method. 
	try: 
		target_index = filtered_words.index("not") # find the not
		words_after_not = len(filtered_words[target_index+1:])
		base = math.e

		for word in filtered_words[target_index+1:]: # put how far away word is
			dist_from_not = (filtered_words.index(word) - \
				target_index)

			# The idea here is we want to spread weightings such that distances
			# less than e get below 1 and greater than e get positive 1 (e 
			# because of its elegance)
			word_weights[word] = min(math.log(dist_from_not, base)**4, 6)

		return [filtered_words, word_weights]

	except ValueError, e:
		# return an empty word_weight
		target_index = None
		return [filtered_words[:target_index], {}]