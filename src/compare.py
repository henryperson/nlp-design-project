import sys
sys.path.append("../dependencies")

# Documentation here: https://pypi.python.org/pypi/Fuzzy
import fuzzy

# Documentation here: https://github.com/gfairchild/pyxDamerauLevenshtein
# Import Normalized Damerau-Levenshtein Distance
from pyxdameraulevenshtein import \
	normalized_damerau_levenshtein_distance_withNPArray

# Import numpy library for Damerau-Levenshtein Edit Distance Equations
import numpy as np

# Import read bac
from read_input import take_user_input, read_possible_classifications

from qwerty_distance import normalized_keyboard_word_distance_withNPArray

import math


# Takes input_list: 
#   ["quadratic", "formula", "not", "komplete", "squar"]
#
# Takes keywords dictionary with format:
# {
#  "CompleteSquare": ["Complete", "Square"],
#  "QuadraticFormula":  ["Quadratic", "Formula"],
#  ...
# }
# Takes word_weights of form: 
#  {
#	"input_after_not": 2
#   "input_after_not_2": 3
#   ...
#  }
#
# Returns scores dictionary with format:
# {
#  "CompleteSquare": 10,
#  "QuadraticFormula":  30,
#  ...
# }
def compare(input_list, keywords_dictionary, word_weights):
	# Load phonetics functions
	dmeta = fuzzy.DMetaphone()
	metaphone = lambda x: dmeta(x)[0]
	soundex = fuzzy.Soundex(4)
	phonetics_methods = [metaphone, soundex]

	# initiate empty dictionary for scores
	scores = {}

	# Iterate through methods for solving, then iterate through words in
	# scrubbed user input. For each word, compare phonetics to all keywords
	# and add score to the scores dictionary. After, do normal QWERTY and LD
	# analyses
	for method, keywords in keywords_dictionary.iteritems():
		scores[method] = 0
		# print(method)
		# Phonetic Scoring methods
		for phonetic in phonetics_methods:
			formatted_array = np.asarray(map(phonetic, keywords))

			for word in input_list:
				formatted_word = phonetic(word)
				dist_array = \
				normalized_damerau_levenshtein_distance_withNPArray(
					formatted_word, formatted_array)
				
				dist = min(dist_array)

				# Handle cases where "not" was found within the input - add to 
				#    scores dictionary.
				weight = word_weights.get(word) if word_weights.get(word) else 1

				scores[method] += weight*math.sqrt(dist)

		# For QWERTY and Damerau-Levenshtein distances, calcuate the differences
		for word in input_list:
			# Do QWERTY Keyboard analysis
			dist_array = normalized_keyboard_word_distance_withNPArray(
				word, keywords)
			dist = min(dist_array)
			
			# handle weighting for position from "not"
			weight = word_weights.get(word) if word_weights.get(word) else 1
			scores[method] += weight*math.sqrt(dist)

			# Do normal LD analysis
			dist_array = normalized_damerau_levenshtein_distance_withNPArray(
				word, np.asarray(keywords))
			dist = min(dist_array)
			
			weight = word_weights.get(word) if word_weights.get(word) else 1
			scores[method] += weight*math.sqrt(dist)

	return scores
