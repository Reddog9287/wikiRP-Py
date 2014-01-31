# coding=utf-8

from __future__ import print_function

import itertools
import sys
import nltk
from nltk.grammar import Nonterminal, parse_cfg

import urllib2
import ast
import nltk

# Strip out anything between <ref> and </ref> - done
# Strip out anything between {{ and }}

def scrape(string, start, end):
	splitString = string.split(end)
	# print "Stripping this out: "+start
	# print "-------------------------------------------------------------------------------------------------"
	# print splitString[0] # So unfortunately start occurs twice here
	# print "-------------------------------------------------------------------------------------------------"


	final = ""
	x=0
	for i in splitString:
		if start in splitString[x]:
			substring = splitString[x].split(start)
			# print "------------------SUBSTRING-------------------------SUBSTRING------------------------------------"
			# print substring
			if substring[0] == '': # if [0] is empty string, then @start was found at the beginning of a line
				# Okay. So somewhere somehow this substring is getting screwed
				# final += substring[1] # [1] should be the part between @start and @end
				# and I think [2] should be out of bounds
				# Mayhaps do nothing at this point, just go through the loop again
				pass
			else:
				final += substring[0]
		x = x+1
	# print final
	return final

# @NOTE: Errors
# -------------------------------------
# if searching for @start: {{ and @end: }} - if @end does not exist,
# then there is an error parsing and the whole thing is thrown off
# -------------------------------------
# if @start and @end are the same, then nothing is returned at all

# Pythagoras works great as it is
# In_Rainbows_%e2%80%93_From_the_Basement gives some errors

def sentencer(string):
	sentences = string.split(". ")
	# print sentences[3]
	# sentences = ''
	for i in sentences:
		print('---------------------------------------------------')
		print(i) # Really have to split this string by ".\n" or just build sentences string by splitting by "." instead of ". "
		# sentences = i.split(". ")
		# print sentences[0]
		# for x in sentences:
			# print x

class WikiRP(object):
	def __init__(self):
		self.thesis = raw_input("Enter a thesis statement: ")

	def makeRequest(self, method):
		self.method = method
		body = "http://en.wikipedia.org/w/api.php?format=json&action=query"

		if method == "search":
			params = "&list=search&srprop=timestamp&srsearch="+self.thesis
		else:
			params = "&prop=revisions&rvprop=content&titles="+self.thesis

		url = body + params
		response = urllib2.urlopen(url)
		json = response.read()
		self.out = ast.literal_eval(json)
		# Below qould be useful but idk not right now
		# print "I'm a %s %s and I taste %s." % (self.color, self.name, self.flavor)

	def errors(self):
		if "#Redirect" in self.content:
			redirect = self.content.split("]]")[0].split("[[")[1]
			print(redirect)
			return True
		else:
			return False

	def parse(self):
		if self.method == "search":
			self.thesis = self.out["query"]["search"][0]["title"]
			print("New Title: "+self.thesis+"\nMaking new Pages request....")
		else:
			pageid = self.out["query"]["pages"].keys()[0]
			self.content = self.out["query"]["pages"][pageid]["revisions"][0]["*"]

			# return self.content
			# - So that these methods scrape() and sentencer() can be a part of the class
			# So essentially what I learned from the tester.py is that these need to be switched...
			strippedRefs = scrape(self.content, "{{", "}}")
			# print scrape(strippedRefs, "==", "==")
			total = scrape(strippedRefs, "<ref","</ref>")
			sentencer(total)

	def buildPaper():
		# Build a text document or PDF or something
		return

researchPaper = WikiRP()
# This all goes in a "main" method
researchPaper.makeRequest("pages")
researchPaper.parse()
if researchPaper.errors(): # This is pretty wasteful code so...
	researchPaper.makeRequest("search")
	researchPaper.parse()
	researchPaper.makeRequest("pages")
researchPaper.parse()

# In_Rainbows_%e2%80%93_From_the_Basement

def generate(grammar, start=None, depth=None, n=None):
    """
    Generates an iterator of all sentences from a CFG.

    :param grammar: The Grammar used to generate sentences.
    :param start: The Nonterminal from which to start generate sentences.
    :param depth: The maximal depth of the generated tree.
    :param n: The maximum number of sentences to return.
    :return: An iterator of lists of terminal tokens.
    """
    if not start:
        start = grammar.start()
    if depth is None:
        depth = sys.maxsize

    iter = _generate_all(grammar, [start], depth)

    if n:
        iter = itertools.islice(iter, n)

    return iter

def _generate_all(grammar, items, depth):
    if items:
        for frag1 in _generate_one(grammar, items[0], depth):
            for frag2 in _generate_all(grammar, items[1:], depth):
                yield frag1 + frag2
    else:
        yield []

def _generate_one(grammar, item, depth):
    if depth > 0:
        if isinstance(item, Nonterminal):
            for prod in grammar.productions(lhs=item):
                for frag in _generate_all(grammar, prod.rhs(), depth-1):
                    yield frag
        else:
            yield [item]

# I SUCK AT WRITING GRAMMARS
radio_grammar = """
S -> NP VP PP
	NP -> NNP Det Det NNP
	VP -> 'is' Det N N Det
	PP -> JJ JJ NNP
	NNP -> 'In Rainbows' | 'Basement' | 'Radiohead'
	JJ -> 'English' | 'alternative' | 'rock' | 'band'
	Det -> 'the' | 'a' | 'by' | 'from'
	N -> 'video' | 'album' | 'rock' | 'band'
"""
grammar = parse_cfg(radio_grammar)
for n, sent in enumerate(generate(grammar, n=10000), 1):
        print('%3d. %s' % (n, ' '.join(sent)))