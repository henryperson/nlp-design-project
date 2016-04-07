# Documentation here: https://pypi.python.org/pypi/Fuzzy
# pip install fuzzy
import fuzzy

# Documentation here: https://github.com/gfairchild/pyxDamerauLevenshtein
# pip install pyxDamerauLevenshtein
import pyxdameraulevenshtein


# Documentation here: http://www.nltk.org/
# pip install nltk
import nltk
nltk.download()  # Download text data sets, including stop words
from nltk.corpus import stopwords
# bag of stop words to exclude from input, convert to a set for search
stop = set(stopwords.words('english'));

# ML Package, Documentation:
#  http://scikit-learn.org/stable/modules/svm.html#multi-class-classification
#  http://scikit-learn.org/stable/modules/tree.html#classification
#  http://scikit-learn.org/stable/supervised_learning.html#supervised-learning
#pip install scikit-learn.org
import scikit-learn.org


# Import pandas for reading data in/out for data structures from csv's.
#pip install pandas
import pandas



# scores_dictionary format:
# {
#  "CompleteSquare": 10,
#  "QuadraticFormula":  30,
#  ...
# }
def phonetics_comparison(user_input, scores_dictionary, keywords_dictionary):
	# iterate through solving methods
	# for each one, iterate through scrubbed user input
	# compare word w/ metaphone to list of keywords for solving method
	# you get a list of distances from each keyword, reduce list by adding
	# add this score to scores_dictionary for the method you're using (update, not set)

	# Load phonetics packages
	dmeta = fuzzy.DMetaphone()
	soundex = fuzzy.Soundex(4)

	# Split user input into lists for iteration
	input_list = user_input.split()

	# Iterate through methods for solving, then iterate through words in
	# scrubbed user input. For each word, compare phonetics to all keywords
	# and add score to the scores dictionary
	for method, keywords in keywords_dictionary.iteritems():
		for word in input_list:
			metaphone_word = dmeta(word)[0]
			metaphone_array = map(lambda x: dmeta(x)[0], keywords)

			soundex_word = soundex(word)
			soundex_array = map(soundex, keywords)

			dist_array = damerau_levenshtein_distance_withNPArray(word, keywords)
			dist = reduce(lambda x, y: x+y, dist_array)


