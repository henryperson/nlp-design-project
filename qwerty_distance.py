########################   QWERTY Keyboard Distance    #########################
# Source, though edited:
#   http://stackoverflow.com/questions/29233888/edit-distance-such-as-
#    levenshtein-taking-into-account-proximity-on-keyboard
from math import sqrt

# Distances on QWERTY keyboard for typo accuracy
keyboard_cartesian = {
                        'q': {'x':0, 'y':0},
                        'w': {'x':1, 'y':0}, 
                        'e': {'x':2, 'y':0}, 
                        'r': {'x':3, 'y':0}, 
                        't': {'x':4, 'y':0}, 
                        'y': {'x':5, 'y':0}, 
                        'u': {'x':6, 'y':0}, 
                        'i': {'x':7, 'y':0}, 
                        'o': {'x':8, 'y':0}, 
                        'p': {'x':9, 'y':0}, 
                        'a': {'x':0, 'y':1},
                        'z': {'x':0, 'y':2},
                        's': {'x':1, 'y':1},
                        'x': {'x':1, 'y':2},
                        'd': {'x':2, 'y':1},
                        'c': {'x':2, 'y':2}, 
                        'f': {'x':3, 'y':1}, 
                        'b': {'x':4, 'y':2}, 
                        'm': {'x':5, 'y':2}, 
                        'j': {'x':6, 'y':1}, 
                        'g': {'x':4, 'y':1}, 
                        'h': {'x':5, 'y':1}, 
                        'j': {'x':6, 'y':1}, 
                        'k': {'x':7, 'y':1}, 
                        'l': {'x':8, 'y':1}, 
                        'v': {'x':3, 'y':2}, 
                        'n': {'x':5, 'y':2}, }

# QWERTY keyboard distance for letters
def keyboard_distance(a,b):
    X = (keyboard_cartesian[a]['x'] - keyboard_cartesian[b]['x'])**2
    Y = (keyboard_cartesian[a]['y'] - keyboard_cartesian[b]['y'])**2
    return sqrt(X+Y)

# QWERTY keyboard distance for words
def keyboard_word_distance(s1,s2):
	sum = 0

	for i in range(0, min(len(s1), len(s2))):
		sum += keyboard_distance(s1[i],s2[i])

	if (len(s1) != len(s2)):
		sum += abs(len(s1) - len(s2))
	
	return sum

# Normalized QWERTY keyboard distances for words
def normalized_keyboard_word_distance(a, b):
    return float(keyboard_word_distance(a,b))/max(len(a),
                                                  len(b))

################################################################################