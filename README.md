# Matching User Input with Answer Solving Categories
_Toby Baratta, 2017 - barattat17_, 
_Henry Fisher, 2018 - fisherhe_, 
_April 13, 2016_

## Summary
This is a program to match user input with a set of specific math problem-solving classifications. It is a classic natural language processing question for the problem-solving question. We use a combination of NLP known methods for matching, pre-processing, and assigning scores.

## Assumed Input
Our input is assumed to be any English sentence typed without weird characters or numbers. (If you want to add number compatibility, it's actually really easy and we can do that.) 

## Algorithms

Our methodology combines steps of pre-processing for user input, processing for classifications, and processing for Natural-Language Processing methods. We then assign scores based on potential matches based on a scoring system of "closeness" determined by phonetics, Demarau-Levenshtein, QWERTY Keyboard, and closeness to "not" within the input. 

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

When given input from a user, we check how close that input is to keywords for each method, and compile a score for each method based on that distance. As mentioned above, there are four different methods we use to determine distance - two phonetics packages, an edit distance, and a keyboard distance. For each word in the users input, we take the minimum of the distances between that word and our keywords (keywords would be "quadratic" and "formula" for "QuadraticForumla"). 

As an example, say the user's input is "kwadratic formuula". We begin with the soundex distance metric, use it to first compare "kwadratic" to "quadratic" and "formula" (the keywords), take the minimum distance there, and then do the same for "formuula". Note that the minimum here is so that when we check "kwadratic" (for instance) we don't penalize it for being far away from "formula". We then repeat this for all four distance metrics, for all methods. The score for a method is simply the sum of these minimum distances for all distance metrics, for all words in the input string. The best scores will be the lowest ones, since that means the user's input had the lowest distance from that method after aggregating over all our distance metrics.

The difficulty comes when dealing with "not". As we mentioned, our original plan was to ignore input after we see "not". However, this doesn't work for cases where the user says "not this but maybe that". So we have to weight input around "not". Since a higher score is worse, our first instinct was to weight words after the "not" very strongly, multiplying them by around 5 times their original quantity, decreasing with distance from the "not". However, it's easy to see why this has the opposite effect as intended. If input is "not substitution but elimination", substitution will get a distance of 0 with a weight of 5, and elimination will get a distance of (say) 2 with a weight of 5, leading to a total score increase by 10. We end up punishing words for being far away from substitution!

After a couple more failed techniques, we found the one that works - weight words close to the "not" much less than 1 and words further away from it much higher. In the example given above, how close a word is to substitution barely matters at all - best case it gets a 0, but worst case it gets around a .2. Further away from the "not" gives an increasing weight. This is done by assuming after around the 3rd word after the "not", the user is done specifying what they believe to not be the answer. We take the natural log of the distance from "not" and then take it to the 4th power to spread the distribution even more. The weight is capped at 6 so that in cases where the user specifies two methods after a not ("not substitution but elimination or square roots") we do not give ridiculous weights to square roots just because it's further away from the "not". Using this weighting scheme (along with a weight of 1 to any words before "not"), we find consistently very good results.

After compiling a score for each solution method, we take the minimum three scores and find probabilities for these three. The probabilities here are more or less arbitrary since the scores are arbitrary - in order to keep probabilities well spread, we take the minimum score and assume that twice the minimum is half as likely. We give the minimum a probability of 1, then find the other probabilities, and then normalize those results. This method ends up with intuitively plausible results. Since our probabilities are arbitrary, the way to determine if an answer is unknown or if we should return two answers is at the programmer's discretion. After playing around with numbers, we found that the best criteria was if the two highest probabilities were within .05 of each other then we return both of them, but if all three are within .05 of each other then we assume the answer is unknown.

## Resources

The python libraries that we use are:
  - json
  - sys
  - math
  - numpy
  - re
  - string
  - nltk.corpus
  - fuzzy
  - pyxdameraulevenshtein

## Restrictions

There are certain cases where this fails - it's not so good at knowing when it shouldn't know the right answer, such as when given something that sounds moderately "mathish" but is just really really off. We could fix this by raising the bar for similarity, but then we worry that we would tell a client we don't understand their input if it's too close. We think that the case of suggesting a potential solution when someone said gibberish is less harmful than discouraging a correct student.

## Results By Input
Below are the results for the cases in the email, as well as additional edge cases. 
#### Environmental Assumptions
We ran our code on MacBook Pro's running Yosemite & El Capitan. The Yosemite computer is a 15-inch, Early 2011 MBP with a 2.2 GHz Intel Core i7 and 16 GB of memory. The El Capitan 13-inch, Late 2013 wth a 2.8 Ghz Intel Core i7 and 8 GB of memory. This code works on both computers. 

#### Example Results
```
How will you solve this problem? ['You said: Use the complete the squares method']
{
 "CompleteTheSquare": 0.41575528687778684, 
 "EliminationMethod": 0.2811457841693379, 
 "SubstitutionMethod": 0.30309892895287543
}
I think you meant : ['CompleteTheSquare']

How will you solve this problem? ["You said: I'll use the method of completing the squares"]
{
 "CompleteTheSquare": 0.393921257521752, 
 "EliminationMethod": 0.29103573803071475, 
 "SubstitutionMethod": 0.31504300444753325
}
I think you meant : ['CompleteTheSquare']

How will you solve this problem? ['You said: komplete da skware']
{
 "TakeSquareRoots": 0.30375040263107245, 
 "CompleteTheSquare": 0.420406772782702, 
 "Help": 0.27584282458622555
}
I think you meant : ['CompleteTheSquare']

How will you solve this problem? ["You said: I'm not sure"]
{
 "TakeSquareRoots": 0.31858024714393274, 
 "Help": 0.32209525604172934, 
 "SubstitutionMethod": 0.3593244968143379
}
I am unsure what you meant. Please try again.

How will you solve this problem? ['You said: complete-the-squares method']
{
 "CompleteTheSquare": 0.41575528687778684, 
 "EliminationMethod": 0.2811457841693379, 
 "SubstitutionMethod": 0.30309892895287543
}
I think you meant : ['CompleteTheSquare']

How will you solve this problem? ["You said: I'd use the quadratic formula cuz itz my fave"]
{
 "QuadraticFormula": 0.47995038842031434, 
 "SubstitutionMethod": 0.19851800647900636, 
 "FactorQuadratic": 0.3215316051006793
}
I think you meant : ['QuadraticFormula']

How will you solve this problem? ["You said: I'll factor quadratics"]
{
 "QuadraticFormula": 0.17539925000631898, 
 "TakeSquareRoots": 0.11240989931918252, 
 "FactorQuadratic": 0.7121908506744985
}
I think you meant : ['FactorQuadratic']

How will you solve this problem? ['You said: I plan to complete the squares']
{
 "TakeSquareRoots": 0.2752197537358025, 
 "CompleteTheSquare": 0.48104046463443006, 
 "Help": 0.2437397816297675
}
I think you meant : ['CompleteTheSquare']

How will you solve this problem? ['You said: Do a square root']
{
 "TakeSquareRoots": 0.5393418624052703, 
 "CompleteTheSquare": 0.28774056575319396, 
 "SubstitutionMethod": 0.1729175718415359
}
I think you meant : ['TakeSquareRoots']

How will you solve this problem? ['You said: Utilize the methods of square roots']
{
 "TakeSquareRoots": 0.464494631605512, 
 "CompleteTheSquare": 0.2671990975590527, 
 "SubstitutionMethod": 0.2683062708354354
}
I think you meant : ['TakeSquareRoots']

How will you solve this problem? ['You said: Solve by substitution']
{
 "TakeSquareRoots": 0.268875307037918, 
 "Help": 0.2732965093937963, 
 "SubstitutionMethod": 0.45782818356828564
}
I think you meant : ['SubstitutionMethod']

How will you solve this problem? ['You said: I have no idea']
{
 "EliminationMethod": 0.14881428776638386, 
 "SubstitutionMethod": 0.16139515140500674, 
 "Help": 0.6897905608286095
}
I think you meant : ['Help']

How will you solve this problem? ['You said: Help']
{
 "EliminationMethod": 0.15112846630879118, 
 "SubstitutionMethod": 0.1468916354926982, 
 "Help": 0.7019798981985106
}
I think you meant : ['Help']

How will you solve this problem? ['You said: Give me a hint']
{
 "EliminationMethod": 0.26424046159671716, 
 "SubstitutionMethod": 0.2621920174036329, 
 "Help": 0.4735675209996501
}
I think you meant : ['Help']

How will you solve this problem? ['You said: Xyzzy']
{
 "TakeSquareRoots": 0.32852684792250564, 
 "SubstitutionMethod": 0.3520820345126482, 
 "FactorQuadratic": 0.31939111756484617
}
I am unsure what you meant. Please try again.

How will you solve this problem? ['You said: Use Kolmolgorov Turbulence']
{
 "QuadraticFormula": 0.3913684688410312, 
 "CompleteTheSquare": 0.2999207437252117, 
 "Help": 0.30871078743375713
}
I think you meant : ['QuadraticFormula']

How will you solve this problem? ['You said: Factor Third-order Partial Differential Equations']
{
 "TakeSquareRoots": 0.31357942682191525, 
 "Help": 0.3224725212165533, 
 "FactorQuadratic": 0.36394805196153135
}
I think you meant : ['Help', 'FactorQuadratic']

How will you solve this problem? ['You said: Consult the i ching']
{
 "CompleteTheSquare": 0.3176414314357454, 
 "Help": 0.36470775232041625, 
 "SubstitutionMethod": 0.3176508162438384
}
I am unsure what you meant. Please try again.

How will you solve this problem? ['You said: Read Tea Leaves']
{
 "EliminationMethod": 0.3283304653108357, 
 "SubstitutionMethod": 0.33264100847710637, 
 "Help": 0.33902852621205803
}
I am unsure what you meant. Please try again.

How will you solve this problem? ['You said: Substitution method not quadratic formula']
{
 "QuadraticFormula": 0.2953618637413158, 
 "SubstitutionMethod": 0.4190777262085775, 
 "FactorQuadratic": 0.28556041005010663
}
I think you meant : ['SubstitutionMethod']

How will you solve this problem? ['You said: Not factor quadratics but maybe elimination method or quadratic formula']
{
 "QuadraticFormula": 0.38153976345309637, 
 "EliminationMethod": 0.3397297965457948, 
 "FactorQuadratic": 0.2787304400011088
}
I think you meant : ['QuadraticFormula', 'EliminationMethod']

How will you solve this problem? ['You said: Not elimination method but maybe taking square roots']
{
 "TakeSquareRoots": 0.5465325959447944, 
 "CompleteTheSquare": 0.25254198816232504, 
 "Help": 0.2009254158928806
}
I think you meant : ['TakeSquareRoots']
```

## Conclusions
Overall, we think our solution solves the problem adequately enough, and efficiently enough. We hope you agree!