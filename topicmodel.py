import gensim
from common import *
from nltk.tokenize import TweetTokenizer
from gensim import corpora, models






	
def lda_model(filename):

	tknzr = TweetTokenizer()
	texts_tokenized = []

	with open(filename, 'rb') as csvfile:
		rows = csv_reader(csvfile)
		line = 0
		for row in rows:
			line += 1
			if line == 1:
				continue
			texts_tokenized.append(tknzr.tokenize(row[0]))
	
	# print texts

	dictionary = corpora.Dictionary(texts_tokenized)
	corpus = [dictionary.doc2bow(text) for text in texts_tokenized]
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)
	print(ldamodel.print_topics(num_topics=3, num_words=3))
	# print ldamodel
	print(ldamodel.get_topic_terms(topicid = 0, topn=15))
	

if __name__ == '__main__':
	lda_model('test_preprocessed.csv')