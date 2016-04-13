#!/usr/bin/python

# Documentation here: https://pypi.python.org/pypi/Fuzzy
# pip install fuzzy
import fuzzy

# Documentation here: https://github.com/gfairchild/pyxDamerauLevenshtein
# pip install pyxDamerauLevenshtein
from pyxdameraulevenshtein import damerau_levenshtein_distance_withNPArray, normalized_damerau_levenshtein_distance_withNPArray

# Documentation here: http://www.nltk.org/
# pip install nltk
#nltk.download()  # Download text data sets, including stop words
from nltk.corpus import stopwords

# bag of stop words to exclude from input, convert to a set for search
stop = set(stopwords.words('english'))

from readInput import takeUserInput, readInput

from qwerty_distance import normalized_keyboard_word_distance_withNPArray, keyboard_word_distance_withNPArray

import numpy as np

# Takes keywords dictionary with format:
# {
#  "CompleteSquare": ["Complete", "Square"],
#  "QuadraticFormula":  ["Quadratic", "Formula"],
#  ...
# }

# returns scores dictionary with format:
# {
#  "CompleteSquare": 10,
#  "QuadraticFormula":  30,
#  ...
# }
def compare(input_list, keywords_dictionary):
	# Load phonetics functions
	dmeta = fuzzy.DMetaphone()
	metaphone = lambda x: dmeta(x)[0]
	soundex = fuzzy.Soundex(4)

	phonetics_methods = [metaphone, soundex]

	scores = {}

	# Iterate through methods for solving, then iterate through words in
	# scrubbed user input. For each word, compare phonetics to all keywords
	# and add score to the scores dictionary. After, do normal QWERTY and LD
	# analyses
	for method, keywords in keywords_dictionary.iteritems():
		scores[method] = 0

		for phonetic in phonetics_methods:
			formatted_array = np.asarray(map(phonetic, keywords))

			for word in input_list:
				formatted_word = phonetic(word)
				# dist_array = normalized_damerau_levenshtein_distance_withNPArray(formatted_word, formatted_array)
				dist_array = damerau_levenshtein_distance_withNPArray(formatted_word, formatted_array)
				print("Word '{}' being compared to keywords {}. Scores:".format(word, keywords))
				print(dist_array)
				dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
				scores[method] += dist**2

		for word in input_list:
			# # Do QWERTY Keyboard analysis
			# # dist_array = normalized_keyboard_word_distance_withNPArray(word, keywords)
			# dist_array = keyboard_word_distance_withNPArray(formatted_word, keywords)
			# dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
			# scores[method] += dist
			# print("Word '{}' being compared to keywords {}. QWERTY Scores:".format(word, keywords))
			# print(dist_array)

			# Do normal LD analysis
			# dist_array = normalized_damerau_levenshtein_distance_withNPArray(word, np.asarray(keywords))
			dist_array = damerau_levenshtein_distance_withNPArray(formatted_word, np.asarray(keywords))
			dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
			scores[method] += dist
			print("Word '{}' being compared to keywords {}. LD Scores:".format(word, keywords))
			print(dist_array)
			
	# import pdb; pdb.set_trace()
	return scores

def find_probabilities(scores):
	probabilities = {}
	total_score = sum(scores.values())
	print(total_score)
	for method, score in scores.iteritems():
		probabilities[method] = 1 - float(score) / total_score

	# for i in range(3):
	# 	min_p = min(probabilities.values())
	# 	probabilities.remove()

	# for method, p in p.iteritems():


	total_probs = sum(probabilities.values())
	prob_factor = 1/total_probs
	for method, p in probabilities.iteritems():
		probabilities[method] = prob_factor * p

	print(sum(probabilities.values()))

	return probabilities

# Adding a "live demo" to play with.
def testing():
	user_input = takeUserInput()
	keywords_dictionary = readInput("text.txt")
	scores = compare(user_input, keywords_dictionary)
	print(scores)
	print(min(scores, key=scores.get))
	# print(find_probabilities(scores))


# run the live demo
testing()
