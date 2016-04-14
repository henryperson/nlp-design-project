import sys

# Takes scores dictionary with format:
# {
#  "CompleteSquare": 10,
#  "QuadraticFormula":  30,
#  ...
# }
# Returns probabilities with format:
# {
#  "CompleteSquare": .135,
#  "QuadraticFormula":  .395,
#  ...
# }
def find_probabilities(scores):
	# remove the bottom three scores
	for method in sorted(scores, key=scores.get, reverse=True):
		del scores[method]
		remaining = len(scores)
		if (remaining == 3):
			break

	# save the minimum score
	min_score = scores[min(scores, key=scores.get)]

	# initialize empty probabilities dictionary
	probabilities = {}

	# for each method & score, calculate the probabilities
	for method, score in scores.iteritems():
		probabilities[method] = float(min_score+1)/(score+1)

	# sum the probabilities & normalize the probabilities
	total_probs = sum(probabilities.values())
	prob_factor = 1/total_probs

	for method, p in probabilities.iteritems():
		probabilities[method] = prob_factor * p

	return probabilities

# Takes probabilities with format:
# {
#  "CompleteSquare": .135,
#  "QuadraticFormula":  .395,
#  ...
# }
def process_scores(probabilities):
	# values from the dictionary
	values = probabilities.values()

	# max score value
	max_score = max(values)

	# initializing empty array
	max_score_keys = []

	# for each score, add in those with the lowest or close values
	for key, value in probabilities.iteritems():
		if (abs(value - max_score) < .05):
			max_score_keys.append(key)
	
	# if none of them are actually close, vote unknown
	if ((max_score - min(values)) < .075):
		sys.exit("I am unsure what you meant. Please try again.")

	# if unknown is even one of the options, go with that
	#if "Help" in max_score_keys:
	#	print("I'm unsure what you meant. Please try again.")
	#else:
		#otherwise, print options of what you meant, or the one option
	#	print("I think you meant :"),
	#	print(max_score_keys)
	print("I think you meant :"),
	print(max_score_keys)