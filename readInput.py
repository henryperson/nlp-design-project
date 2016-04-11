
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
		split_words = map(lambda x:x.lower(), split_upper(current));
		filtered_words = [word for word in split_words if word not in stopwords.words('english')]
		keywords_dictionary[current] = filtered_words

	return keywords_dictionary

def takeUserInput():
	solve_method = raw_input("How will you solve this problem? ");
	split_words = map(lambda x:x.lower(), solve_method.split());
	stop = stopwords.words('english')
	stop.remove("not");
	filtered_words = [word for word in split_words if word not in stop]
	try: 
		target_index = filtered_words.index("not")
	except ValueError, e:
		target_index = None
	return filtered_words[:target_index]

# TESTING: 
#print(readInput({}, "text.csv"))
#t = takeUserInput()
#print(t);