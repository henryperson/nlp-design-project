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

def readInput(keywords_dictionary, file_name):
	# open file for reading
	f = open(file_name, 'r')
	# for each line, set the dictionary right for likelihoods
	for line in f: 
		# cut the newline crap
		keywords_dictionary[line.rstrip()] = 0
	return keywords_dictionary


# me testing - works correct
#readInput({}, "text.csv")

from qwerty_distance import normalized_keyboard_word_distance_withNPArray

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
def compare(user_input, keywords_dictionary):
	# Load phonetics functions
	dmeta = fuzzy.DMetaphone()
	metaphone = lambda x: dmeta(x)[0]
	soundex = fuzzy.Soundex(4)

	phonetics_methods = [metaphone, soundex]

	# Split user input into lists for iteration
	raw_input_list = user_input.split()
	input_list = map(lambda x: x.lower(), raw_input_list)

	scores = {}

	# Iterate through methods for solving, then iterate through words in
	# scrubbed user input. For each word, compare phonetics to all keywords
	# and add score to the scores dictionary. After, do normal QWERTY and LD
	# analyses
	for method, keywords in keywords_dictionary.iteritems():
		scores[method] = 0
		for word in input_list:
			for phonetic in phonetics_methods:
				# Get phonetics of user input and keywords, analyze distance with DL
				formatted_word = phonetic(word)
				formatted_array = map(phonetic, keywords)

				dist_array = normalized_damerau_levenshtein_distance_withNPArray(formatted_word, formatted_array)
				dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
				scores[method] += dist

			# Do QWERTY Keyboard analysis
			dist_array = normalized_keyboard_word_distance_withNPArray(word, keywords)
			dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
			scores[method] += dist

			# Do normal LD analysis
			dist_array = normalized_damerau_levenshtein_distance_withNPArray(word, keywords)
			dist = reduce(lambda x, y: x if x < y else y, dist_array, float("inf"))
			scores[method] += dist

	return scores

