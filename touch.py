from __future__ import division	
import nltk 
import string

# Keyboard representation
top = ['.','q','w','e','r','t','y','u','i','o','p','.']
middle = ['.','a','s','d','f','g','h','j','k','l','.']
bottom = ['.','z','x','c','v','b','n','m','.']


# A function to estimate a bigram (letter) model obtained 
# from a training corpus
def get_bigram_model():
	from nltk.corpus import brown
	from nltk.tokenize import word_tokenize, sent_tokenize

	words = brown.words()

	# Frequency of initial characters
	initials = {}
	
	# Frequency of pairs
	pairs = {}

	# Bigram model with probabilities
	bigrams = {}
	
	for word in words:
		# add start character 
		word = '$' + word 

		this_pairs = split_in_pairs(word)
		for pair in this_pairs:
			init = pair[0]
			if init in initials:
				initials[init] += 1
			else:
				initials[init] = 1
				
			if pair in pairs: 
				pairs[pair] += 1
			else:
				pairs[pair] = 1

	for p in pairs:
		init = p[0]
		bigrams[p] = (pairs[p] / initials[init])

	return bigrams


# Takes a word, returns a list of pairs of characters 
def split_in_pairs(word):
	num = len(word) - 1
	i = 0
	pairs = [''] * num
	while (i < num):
		pairs[i] = word[i:(i+2)] 	
		i += 1
	return pairs

# Takes a character, returns a tuple (left, right neighbour)
# Returns ('.','.') if character is not valid letter
def find_neighbours(char):
	if char in top:
		x = top.index(char)
		return (top[x-1],top[x+1])
	elif char in middle:
		x = middle.index(char)
		return (middle[x-1],middle[x+1])	 		
	elif char in bottom:
		x = bottom.index(char)
		return (bottom[x-1],bottom[x+1])
	else:
		return ('.','.') 		
	
# Takes a prefix of a word, and replaces the
# last letter by one of at most two neighbouring letters on the 
# keyboard to give at most two potential corrections
def find_correction(prefix):
	corr = ()
	nb = find_neighbours(prefix[-1:])
	if (nb[0]!='.'): 
		left = prefix[:-1] + nb[0]
		corr = corr + (left,)
	if (nb[1]!='.'):
		right = prefix[:-1] + nb[1]
		corr = corr + (right,)
	return corr


def find_pair_prob(str,model):
	if str in model:
		return model[str]
	else:
		return 1


# A function that computes the prefix probability of a string 
# using the bigram model (estimate_bigram). 
def compute_prefix_prob(str):
	# get bigram model using get_bigram_model 
	# split string into pairs
	model = { '$' : 0}
	str = '$' + str
	str_pairs = { '$' : 0}
	i = 0
	prob = 10
	while i < (len(str) -1):
		pair = str[i] + str[i+1]
		prob = prob * find_pair_prob(pair,model)	
		i += 1
	return prob

# A function that proposes the most likely correction of a 
# prefix. 
def best_correction(prefix):
	prefix_corr = find_correction(prefix)
	
	prob_org = compute_prefix_prob(prefix) 
	prob_l = compute_prefix_prob(prefix_l)
	prob_r = compute_prefix_prob(prefix_r)
	if (prob_l > prob_org):
		if (prob_l > prob_r): 
			return prefix_l
		else:
			return prefix_r
	elif (prob_r > prob_org):
		return prefix_r 

	else :
		return prefix
	

# Measure accuracy of our functions for a given corpus. 
def test_accuracy(corpus):
	pass


