import csv

dataset_default = 'Homework2_data.csv'
dataset_test = 'test.csv'
dict_file = 'dict.pickle'

word_cluster_file = '50mpaths2.txt'

def csv_writer(outfile):
	return csv.writer(outfile, delimiter=',', quotechar='"')

def csv_reader(infile):
	return csv.reader(infile, delimiter=',', quotechar='"')

def preprocessed_filename(filename):
	return filename[:-4]+'_preprocessed.csv'

def result_filename(filename):
	return filename[:-4]+'_result.csv'

def lsi_filename(filename):
	return filename[:-4]+'_lsi.csv'

def fmt_feature_set(features):
	if len(features) == 0:
		return ''
	str_features = []
	for a,b in features:
		# print a
		# str_features += str(a)
		str_features += ['('+a+','+str(b)+')']
	return ' '.join(str_features)