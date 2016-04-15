
# http://stackoverflow.com/questions/12124275/splitting-a-string-by
#    -capital-letters
import re

# Use sys to exit when unknown/inappropriate input
import sys

# Documentation here: http://www.nltk.org/
# pip install nltk
#nltk.download()  # Download text data sets, including stop words
from nltk.corpus import stopwords

# Handle profanity by filtering things from bad_words
from profanity import bad_words

import string

# Takes a string, outputs string without punctuation
def depunctuation(s):
	replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
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
			stopwords.words('english')]
		keywords_dictionary[current] = filtered_words

	# Add unknown method as a potential option. 
	keywords_dictionary["Help"] = ["dont", "know", "unknown", 
		"help", "helping", "hint", "idea"]

	return keywords_dictionary

# Returns a list of important user inputs, and weights for handling "nots"
def take_user_input():
	# take input from stdin
	solve_method = raw_input("How will you solve this problem? ")

	# remove punctuation from string
	solve_method = depunctuation(solve_method)
	# split string by spaces, make lower case
	split_words = map(lambda x:x.lower(), solve_method.split())

	# test for profanity
	test = [1 for word in split_words if word in bad_words]
	if (test):
		sys.exit("Please don't say inappropriate things to me.")

	# remove stopwords 
	stop = stopwords.words('english')
	stop.remove("not") #take "not" out of stop words

	# add in stop words with bad slang
	map(stop.append, ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o",
		"p","q","r","s","t","u","v","w","x","y","z","cuz","wat","teh","itz",
		"wut","probs","probz","dunno","huh", "use"])

	filtered_words = [word for word in split_words if word not in stop]
	
	# add a new dictionary of indices of key words from the nots
	word_weights = {}
	# weight all things after a "not" by how far away things are from the "not"
	# in the input. We keep the "not" so that "i do not know" keeps for unknown
	# method. 
	try: 
		target_index = filtered_words.index("not") # find the not
		target_index_original_string = split_words.index("not") # original not
		words_after_not = len(filtered_words[target_index+1:])
		tot_normalize = (words_after_not*(words_after_not+1))/2

		for word in filtered_words[target_index+1:]: # put how far away word is
			# word_weights[word] = ((split_words.index(word) - \
			# 	target_index_original_string)/float(tot_normalize))*10
			word_weights[word] = (split_words.index(word) - \
				target_index_original_string)

		return [filtered_words, word_weights]

	except ValueError, e:
		# return an empty word_weight
		target_index = None
		return [filtered_words[:target_index], {}]