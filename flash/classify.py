#!/usr/bin/python
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.navigr
things=db.things


lemmatz = WordNetLemmatizer()

cur=""


def getCategory(sent):
	try:
		word_tok = word_tokenize(sent.lower())

		pos_lis=pos_tag(word_tok)
		a=list()
		#lemmatz.lemmatize(pos_lis[2][0])
		#print pos_lis
		for item in pos_lis:
			if item[1][0] == 'N':
				a.append(lemmatz.lemmatize(item[0]))

		#print a[0]

		cur=things.find({"content":""+a[0]+""},{"type":1})
		category= list(cur)[0]['type']
		return category
	except:
		category= "other"
		return category
#print getCategory("get iphone from the store")
