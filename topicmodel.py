import gensim
from common import *
from nltk.tokenize import TweetTokenizer
from gensim import corpora, models
import indexDocs
from subprocess import call


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


def btm_model(filename, K):
	W=48267   # vocabulary size
	alpha= "%.3f"%(50/K)
	beta=0.005
	n_day=1
	input_dir='tmp/input/'
	output_dir='tmp/output/'
	dwid_dir= output_dir+'doc_wids/'
	model_dir= output_dir + 'model/'
	voca_pt= output_dir + 'voca.txt'
	method='ibtm'   # must be obtm or ibtm

	sentences = []
	with open(preprocessed_filename(filename), 'rb') as csvfile:
		rows = csv_reader(csvfile)
		line = 0
		for row in rows:
			line += 1
			if line == 1:
				continue
			sentences += [row[0]]
	with open(input_dir+'0.txt','w') as outfile:
		for s in sentences:
			outfile.write(s)
			outfile.write('\n')
	# python indexDocs.py $input_dir $dwid_dir $voca_pt
	indexDocs.indexDir(input_dir, dwid_dir)
	indexDocs.write_w2id(voca_pt)

	# learning
	if method == "obtm":
		n_iter=500
		lam=1
		params = ['OnlineBTM/src/run','obtm',K,W,alpha,beta,dwid_dir,n_day,model_dir,n_iter,lam]
		call([str(i) for i in params])
		# ../src/run obtm $K $W $alpha $beta $dwid_dir $n_day $model_dir $n_iter $lam
	else:
		win=2000000
		n_rej=100
		params = ['OnlineBTM/src/run','ibtm',K,W,alpha,beta,dwid_dir,n_day,model_dir,win,n_rej]
		call([str(i) for i in params])
		# ../src/run ibtm $K $W $alpha $beta $dwid_dir $n_day $model_dir $win $n_rej
	#  infer

	dwid_pt=dwid_dir+'0.txt'
	params = ['OnlineBTM/src/infer','sum_b',K,0,dwid_pt,model_dir]
	call([str(i) for i in params])
	# ../src/infer sum_b $K $day $dwid_pt $model_dir
	ret = []
	with open(model_dir+'k'+str(K)+'.day0.pz_d', 'r') as infile:
		for line in infile.readlines():
			max_label = 0
			max_p = 0
			label = 0
			for i in line.split(' '):
				if i!='\n' and float(i)>max_p:
					max_p = float(i)
					max_label = label
				label += 1
			ret += [max_label]
	return ret

if __name__ == '__main__':
	print btm_model(dataset_test, 5)
	print lda_model(dataset_test, 5)