
# http://stackoverflow.com/questions/12124275/splitting-a-string-by
#    -capital-letters
import re

# Documentation here: http://www.nltk.org/
# pip install nltk
#nltk.download()  # Download text data sets, including stop words
from nltk.corpus import stopwords

def split_upper(s):
    return filter(None, re.split("([A-Z][^A-Z]*)", s))


def readInput(keywords_dictionary, file_name):
	# open file for reading
	f = open(file_name, 'r')
	# for each line, set the dictionary right for likelihoods
	for line in f: 
		current = line.rstrip()
		splitWords = map(lambda x:x.lower(), split_upper(current));
		filtered_words = [word for word in splitWords if word not in stopwords.words('english')]
		keywords_dictionary[current] = filtered_words

	return keywords_dictionary


#print(readInput({}, "text.csv"))