# coding=utf-8

import urllib2
import ast

# Strip out anything between <ref> and <\/ref>
# Strip out anything between {{ and }}

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

		print self.content
		while "</ref>" in self.content:
			substring = self.content.split("</ref>")[0].split("<ref>") # Splits the paper for a ref
			print substring[1]
			print "Test"

	def buildPaper():
		# Do this
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