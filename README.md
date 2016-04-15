# Matching User Input with Answer Solving Categories
_Toby Baratta, 2017 - barattat17_, 
_Henry Fisher, 2018 - fisherhe_, 
_April 13, 2016_

##
This is a program to match user input with a set of specific math problem-solving classifications. It is a classic natural language processing question for the problem-solving question. We use a combination of NLP known methods for matching, pre-processing, and assigning scores. 

## Methodology

Our methodology combines steps of pre-processing for user input, processing for classifications, and processing for Natural-Language Processing methods. We then assign scores based on potential matches based on a scoring system of "closeness" edetermined by phonetics, Demarau-Levenshtein, QWERTY Keyboard, and closeness to "not" within the input. 

So, basically we take the user input, look for any key words in that input or any key phrases (such as a "not this, but that" or "this, not that") and then keep those words. We then give more points for things far away from or before any "nots" or negative words. Then, we measure closeness based on pronounciation (phonetics), and then typo measurements based on keyboards--so typing a 'q' instead of a 'w' gets more points than accidentally typing an 'o'. Demarau-Levenshtein takes into consideration if you type things wrong, such as 'rwote' instead of 'wrote'.  

Then, given these "closeness" scores and "spelling/pronounciation" scores, we calculate a combined score for each potential classification. By classification, we're meaning the method of problem being solved--such as "QuadraticFormula" or "TakeSquareRoots". Next, given those scores we assign probabilities. Then, for the best three options, we look at how close they are  - if they're too close, we ask if either of them were what was meant, unless *all* options are very close. If they're all really close, we say that we don't know what they want. 

#### Parsing User Input

To parse the user input, we first remove punctuation and replace that by spaces. We then split on those spaces to tokenize the input. Before we go any further, we search for any "bad words"; if any are found, we tell the user to fix their language and quit. If we get past that, we see if the input is within a list of stopwords, created from the generic NLP package of stopwords addended with several other potential stop words. We remove those stopwords from the lists. 

Then, we see if there is a "not" within the input. If there was a not within the input, we weight each word after the "not" based on how far away it is from the "not". At first, we just cleared all input that was after the not, but then realized that a user could plug in "not this, but that", so we rethought our methodologies. This method, through vigorous testing, does seem to be working properly. 

#### Phonetics 
For phonetics, we used Soundex and Double Metaphone to assess both the input words and the dictionary words (the classifications). We then matched those together, and used the Demarau-Levenshtein Edit Distance to compare the differences for phonetic words. These algorithms were implemented in the Fuzzy package. 

#### Demarau-Levenshtein Edit Distance
Demarau-Levenshtein Edit Distance uses the DL algorithm classically, as implemented within the "pyxdameraulevenshtein" Python package. 

#### QWERTY Keyboard Distance
QWERTY Keyboard Distance formula takes into consideration how far keys are from each other on the basic keyboard. This was implemented through some code from Stack Overflow, plus some original python code by us. 

#### Scoring & Probability

## Results By Input
Below are the results for the cases in the email, as well as additional edge cases.

#### 
```bash
```

## Failure Cases
There are certain cases where this fails - it's not so good at knowing when it shouldn't know the right answer, such as when given something that sounds moderately "mathish" but is just really really off. We could fix this by raising the bar for similarity, but then we worry that we would tell a client we don't understand their input if its too close. We think that the case of suggesting a potential solution when someone said gibberish is less harmful than discouraging a correct student. 

## Conclusions
Overall, we think our solution solves the problem adequately enough, and efficiently enough. We hope you agree!