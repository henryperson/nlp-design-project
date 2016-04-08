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

# Import pandas for reading data in/out for data structures from csv's.
#pip install pandas
import pandas

from qwerty_distance import normalized_keyboard_word_distance


# returns scores dictionary with format:
# {
#  "CompleteSquare": 10,
#  "QuadraticFormula":  30,
#  ...
# }
def compare(user_input, keywords_dictionary):
	# Load phonetics functions
	dmeta = fuzzy.DMetaphone()
	metaphone = lambda x: dmeta(x)[0]
	soundex = fuzzy.Soundex(4)

	# Load distance functions

	compare_methods = [metaphone, soundex]

	# Split user input into lists for iteration
	input_list = user_input.split()

	# Iterate through methods for solving, then iterate through words in
	# scrubbed user input. For each word, compare phonetics to all keywords
	# and add score to the scores dictionary

	# TODO (here):
	# Rework for loop to iterate through comparisons first (dynamic programming)
	# Separate for loop so we can actually use qwerty distance
	# Add in logical support (not complete square)

	for method, keywords in keywords_dictionary.iteritems():
		for word in input_list:
			for comparison in compare_methods:
				formatted_word = comparison(word)
				formatted_array = map(comparison, keywords)

				dist_array = normalized_damerau_levenshtein_distance_withNPArray(formatted_word, formatted_array)
				dist = reduce(lambda x, y: x+y, dist_array)
