# coding=utf-8

import urllib2
import ast

# Strip out anything between <ref> and <\/ref>
# Strip out anything between {{ and }}

def scrape(string, start, end):
	splitString = string.split(end)

	final = ""
	x=0
	for i in splitString:
		if start in splitString[x]:
			substring = splitString[x].split(start)
			final += substring[0]
		x = x+1
	# print final
	return final

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
			print redirect
			return True
		else:
			return False

	def parse(self):
		if self.method == "search":
			self.thesis = self.out["query"]["search"][0]["title"]
			print "New Title: "+self.thesis+"\nMaking new Pages request...."
		else:
			pageid = self.out["query"]["pages"].keys()[0]
			self.content = self.out["query"]["pages"][pageid]["revisions"][0]["*"]

		strippedRefs = scrape(self.content, "<ref", "</ref>")
		# print scrape(strippedRefs, "==", "==")
		print scrape(strippedRefs, "{{","}}")

		# @NOTE: Errors
		# -------------------------------------
		# if searching for @start: {{ and @end: }} - if @end does not exist,
		# then there is an error parsing and the whole thing is thrown off
		# -------------------------------------
		# if @start and @end are the same, then nothing is returned at all

		# Pythagoras works great as it is
		# In_Rainbows_%e2%80%93_From_the_Basement gives some errors

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