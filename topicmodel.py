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

	with open(lda_model_filename(filename), 'wb') as outfile:
		writer = csv_writer(outfile)
		new_rows = []
		with open(filename, 'rb') as preprocessed_csv:
			rows = csv_reader(preprocessed_csv)
			line = 0
			i = 0
			for row in rows:
				line += 1
				if line == 1:
					continue
				new_rows += [row[0]]

		label_index = 0
		for new_row in new_rows:
			writer.writerow([new_row, labels[label_index]])
			label_index += 1



	return labels


def btm_model(filename, k):

	return []

if __name__ == '__main__':
	print lda_model(dataset_test, 4)