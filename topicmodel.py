import genism


texts = [];

with open('preprocessed.csv','rb') as csvfile:
	rows = csv_reader(csvfile)