
# http://stackoverflow.com/questions/12124275/splitting-a-string-by
#    -capital-letters
import re

# Documentation here: http://www.nltk.org/
# pip install nltk
#nltk.download()  # Download text data sets, including stop words
from nltk.corpus import stopwords

from profanity import bad_words

import string

def depunctuation(s):
	out = s.translate(string.maketrans("",""), string.punctuation)
	return out


def split_upper(s):
    return filter(None, re.split("([A-Z][^A-Z]*)", s))

def readInput(file_name):
	# open file for reading
	f = open(file_name, 'r')
	# for each line, set the dictionary right for likelihoods

	keywords_dictionary = {}

	for line in f: 
		current = line.rstrip()
		split_words = map(lambda x:x.lower(), split_upper(current));
		filtered_words = [word for word in split_words if word not in stopwords.words('english')]
		keywords_dictionary[current] = filtered_words

	return keywords_dictionary

def takeUserInput():
	# take input from stdin
	solve_method = raw_input("How will you solve this problem? ");

	# remove punctuation from string
	solve_method = depunctuation(solve_method);
	# split string by spaces, make lower case
	split_words = map(lambda x:x.lower(), solve_method.split());

	# test for profanity
	test = [1 for word in split_words if word in bad_words]
	if (test):
		print("Please don't say inappropriate things to me.");
		return 0;

	# remove stopwords 
	stop = stopwords.words('english')
	stop.remove("not"); #take "not" out of stop words
	filtered_words = [word for word in split_words if word not in stop]
	
	# remove everything after a "not", including the not
	try: 
		target_index = filtered_words.index("not")
	except ValueError, e:
		target_index = None

	return filtered_words[:target_index]

# TESTING: 
# print(readInput({}, "text.csv"))
# t = takeUserInput()
# print(t);