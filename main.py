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

from qwerty_distance import normalized_keyboard_word_distance_withNPArray

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
			formatted_array = np.asarray(map(phonetic, keywords));

			for word in input_list:
				formatted_word = phonetic(word)
				dist_array = normalized_damerau_levenshtein_distance_withNPArray(formatted_word, formatted_array)
				dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
				scores[method] += dist

		for word in input_list:
			# Do QWERTY Keyboard analysis
			dist_array = normalized_keyboard_word_distance_withNPArray(word, keywords)
			dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
			scores[method] += dist

			# Do normal LD analysis
			dist_array = normalized_damerau_levenshtein_distance_withNPArray(word, np.asarray(keywords))
			dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
			scores[method] += dist
			

	return scores

# Adding a "live demo" to play with.
def testing():
	user_input = takeUserInput();
	keywords_dictionary = readInput("text.csv");
	scores = compare(user_input, keywords_dictionary);
	print(scores);
	print(min(scores, key=scores.get));

# run the live demo
testing();
