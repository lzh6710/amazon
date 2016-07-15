from __future__ import unicode_literals
import os 
from django.db import models
import math
import nltk
import nltk.corpus
from nltk.text import Text
import sys
import collections
import io
import os.path

from nltk.sentiment.vader import SentimentIntensityAnalyzer
# Create your models here.

class Amazon_Analyse(models.Model):
	def analyse_class(self):
		
		#start = timeit.default_timer()
		sid = SentimentIntensityAnalyzer()
		reload(sys)
		sys.setdefaultencoding("utf-8")
		path = os.getcwd()
		m = Text(nltk.corpus.gutenberg.words(path + '/userReviews1.txt'))

		specs = ['camera','performance','battery','look','feel','money','sound','network','storage','software']


		save_path = path + '/analyse/data'
		 
		for res in specs:

			completeFileName = os.path.join(save_path, res+".txt")
			fileconcord = open(completeFileName, 'w')
			tmpout = sys.stdout
			sys.stdout = fileconcord
			m.concordance(res, 200, sys.maxint)
			fileconcord.close()
			sys.stdout = tmpout
		
		
		file = open('sentimentwords.txt')

		dictionary = collections.defaultdict(lambda : 0)
		for token in file:
			dictionary[token[:-1]] = 1
		#print dictionary
		#print sentimentfile
		pic = []
		for res in specs :
			completeFileName = os.path.join(save_path, res+".txt")
			fileconcord  = open(completeFileName, 'r')
			sent_pol = []
			for line in fileconcord:
				line = line.split()
				line_new=[]
				#print line
				for tok in line:
					if dictionary[tok] :
						#print tok
						line_new.append(tok)
				line =' '.join(line_new)
				if res=='heat':
					print line
				sent_pol.append( sid.polarity_scores(line)['compound'])
			print res
			xx = sum(1 for i in sent_pol if i>0)*1.0/len(sent_pol)
			xx = round(xx,2) * 10
			print xx
			pic.append((res,xx)) 
			#print sum(i for i in sent_pol )/len(sent_pol)
			#print sent_pol
			print
		
		return pic