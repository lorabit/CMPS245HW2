from common import *
import enchant
import pickle
from CMUTweetTagger import *
from nltk.corpus import stopwords
from nltk.stem.porter import *

stopword = set(stopwords.words('english'))
stemmer = PorterStemmer()

num = {'0':'o','1':'one','2':'too','3':'thr','4':'for','5':'five','6':'six','7':'seven','8':'ea','9':'nin'}

def shorten(a):
		ret = ""
		for i in a:
			if len(ret)>1 and ret[-1]==i and ret[-2]==i:
				continue
			ret += i
		return ret

def matchness(a, b):
	def abbr(a,b):
		f = [0 for i in b]
		for i in range(0,len(a)):
			for j in range(0,len(b)):
				j = len(b)-j-1
				prev = 0
				if j>0:
					prev = f[j-1]
				diff = 0
				if b[j]==a[i]:
					diff = 1
				f[j] = max(f[j], prev) + diff
			for j in range(0,len(b)):
				if j>0:
					f[j] = max(f[j],f[j-1])
		fact = 2.0
		if a[0]!=b[0]:
			fact = 1.0
		return max(f)*fact/(len(b)+len(a))

	def typo(a,b):
		f = [999 for i in a]
		f[0] = 0
		for i in range(0,len(b)):
			for j in range(0,len(a)):
				j = len(a)-j-1
				prev = i
				if j>0:
					prev = f[j-1]
				diff = 0
				if a[j]!=b[i]:
					diff = 1
				f[j] = min(min(f[j], prev),i+j)+diff
		return 1-f[len(a)-1]*1.0/len(b)

	def phonetic(a):
		ret =  ''
		for i in a:
			if i in num:
				ret += num[i]
			else:
				ret += i
		return ret

	

	a = shorten(a)
	a = phonetic(a)
	if len(b)-len(a)>2:
		return abbr(a,b)
	return typo(a,b)

def word_cluster():
	print 'Loading word clusters...'
	clusters,word_dic = [],{}
	current_id,current_set = '',set()
	with open(word_cluster_file, 'r') as f:
		line = f.readline()
		while line!='':
			row = line.split('\t')
			if row[0]!=current_id:
				clusters += [current_set]
				current_id = row[0]
				current_set = set()
			if enchant_dict.check(row[1]):
				current_set.add(row[1])
			word_dic[row[1]] = len(clusters)
			line = f.readline()
	clusters += [current_set]
	return clusters,word_dic

enchant_dict = enchant.Dict("en_US")
_candidates, _cluster_map = word_cluster()

with open(dict_file,'rb') as f:
	pos_dict = pickle.load(f)

def correct_word(word):
	candidates = _candidates[_cluster_map[word]]
	ret = ''
	max_score = 0
	for candidate in candidates:
		score = matchness(word,candidate)
		if score>max_score:
			max_score = score
			ret = candidate
	return ret,max_score

def score(word, candidate, tag, confidence):
	if candidate in pos_dict:
		v = pos_dict[candidate]
		if tag in v:
			return matchness(word, candidate) + confidence*v[tag] + v['tot']
		else:
			return matchness(word, candidate) + v['tot']
	return matchness(word, candidate)


def steming(tokens):
	ret = []
	for token in tokens:
		token = ''.join([i for i in token if i.isalpha()])
		if len(token) == 0:
			continue
		token = stemmer.stem(token)
		ret += [token]
	return ret

def removeStopwords(tokens):
	ret = []
	for token in tokens:
		if len(token) <= 1:
			continue
		if token in stopword:
			continue
		ret += [token]
	return ret


def smart_candidates(word,tag):
	if word in _cluster_map:
		return _candidates[_cluster_map[word]]
	return [word]
	ret = set()
	for i in pos_dict:
		if tag in pos_dict[i]:
			ret.add(i)
	# print ret
	return ret

def correct_sentences(sentences):
	# print sentences
	sentences = runtagger_parse(sentences)
	ret = []
	for sentence in sentences:
		res = []
		for word, tag, confidence in sentence:
			word = shorten(word)
			selected = word
			if tag != '^' and not enchant_dict.check(word):
				max_score = 0
				candidates = smart_candidates(word,tag)
				# print candidates
				for candidate in candidates:
					_score = score(word,candidate, tag, confidence)
					if _score > max_score:
						max_score = _score
						selected = candidate
			res += [selected]
		ret += [' '.join(steming(removeStopwords(res)))]
	# print ret
	return ret


def main():
	correct_sentences(['i will see u tmrw.'])
	# print correct_word('2morow')
	# train()
	# print matchness('2morow','tomorrow')


if __name__ == '__main__':
	main()