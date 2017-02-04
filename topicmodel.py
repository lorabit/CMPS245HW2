import genism
from nltk.tokenize import RegexpTokenizer

texts = [];

with open('preprocessed.csv','rb') as csvfile:
	rows = csv_reader(csvfile)
	for row in rows:
		texts.append(row[0])


for text in texts:
	
