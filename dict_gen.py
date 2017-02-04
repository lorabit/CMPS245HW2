from common import *
from CMUTweetTagger import *
import enchant
import pickle
import math

d = enchant.Dict("en_US")

def train():
	dataset = []
	with open(dataset_default, 'r') as f:
		reader = csv_reader(f)
		n_row = 0
		for row in reader:
			n_row += 1
			if n_row == 1:
				continue
			dataset += [row[0]]
	sentences = runtagger_parse(dataset)
	raw = {}
	max_tot = 0
	for sentence in sentences:
		for word,token,confidence in sentence:
			if not d.check(word):
				continue
			# total += 1
			if not word in raw:
				raw[word] = {'tot':0}
			raw[word]['tot'] += 1
			max_tot = max(max_tot,raw[word]['tot'])
			if not token in raw[word]:
				raw[word][token] = 1
			else:	
				raw[word][token] += 1
	ret = {}
	for k,v in raw.items():
		tot = v['tot']
		new_v = {'tot':math.sqrt(1.0*tot/max_tot)}
		for _k,_v in v.items():
			if _k !='tot':
				new_v[_k] = 1.0*_v/tot
		ret[k] = new_v
	with open(dict_file,'wb') as f:
		pickle.dump(ret, f)


def main():
	with open(dict_file,'rb') as f:
		ret = pickle.load(f)
		print ret['nix']
	# train()


if __name__ == '__main__':
	main()