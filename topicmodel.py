import gensim
from common import *
from nltk.tokenize import TweetTokenizer
from gensim import corpora, models


def lda_model(filename, k):
	tknzr = TweetTokenizer()
	texts_tokenized = []

	with open(preprocessed_filename(filename), 'rb') as csvfile:
		rows = csv_reader(csvfile)
		line = 0
		for row in rows:
			line += 1
			if line == 1:
				continue
			texts_tokenized.append(tknzr.tokenize(row[0]))

	dictionary = corpora.Dictionary(texts_tokenized)
	corpus = [dictionary.doc2bow(text) for text in texts_tokenized]
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=k, id2word = dictionary, passes=20)
	labels = []
	for bow in corpus:
		max_p = 0
		max_label = 0
		for label, p in ldamodel.get_document_topics(bow):
			if p>max_p:
				max_p = p
				max_label = label
		labels += [max_label]
	return labels


def btm_model(filename, k):

	return []

if __name__ == '__main__':
	print lda_model(dataset_default, 4)