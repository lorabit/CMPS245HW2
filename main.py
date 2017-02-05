from common import *
import preprocess
import topicmodel

def main():
	dataset = dataset_default
	preprocess.preprocess(dataset)
	for k in [3,4,5]:
		topicmodel.lda_model(dataset,k)
		topicmodel.btm_model(dataset,k)

if __name__ == '__main__':
	main()