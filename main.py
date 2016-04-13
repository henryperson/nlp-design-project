#!/usr/bin/python

# Import separate written functions for code written
from read_input import take_user_input, read_possible_classifications
from compare import compare
from process_probabilities import find_probabilities, process_scores

# Import sys to exit with messages
import sys

# Adding a "live demo" to play with.
def live_demo():

	# Question for the Demo
	print("How would you solve this problem? x^2 + 16x = 96")

	# Read in user input, clear out stop words, weight given the style of input
	[user_input, word_weights] = take_user_input()

	# if none of the input is significant at all
	if user_input is None:
		sys.exit("I am unsure what you meant. Please try again.")

	# Read in the possible classifications to the dictionary
	keywords_dictionary = read_possible_classifications("text.txt")

	# Compare possibly classifications to significant user input, weighted
	#   appropriately for "nots"
	scores = compare(user_input, keywords_dictionary, word_weights)

	# Calculate probabilities from the scores returned
	probabilities = find_probabilities(scores);

	# Print the probabilities, if you want to know more details
	print(probabilities)

	# Process scores based on probabilities
	process_scores(probabilities);

# Run the live demo. 
live_demo()