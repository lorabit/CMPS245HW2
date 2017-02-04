# CMPS245HW2 - Topic model on Twitter
Yanan Xie, Ziqiang Wang

## Preprocessing and lexical normalisation of tweets

As the first step, we remove all @user and trailing hash tag after tokenize with nltk. And then we apply lexicon normalisation of our own implementation on the sentences. Finally, we remove stop words to form the dataset to feed the clutering algorithm. 

### Lexicon Normalisation

#### Candidates Generation
We use enchant library to detect errors in sentence. In order to obtain a candidate set for each error word, we use [Twitter word clusters from CMU](http://www.cs.cmu.edu/~ark/TweetNLP/) which contains over 1,000 clusters. For each wrong word, we find the cluster containing this word, and then those correct words in this group are the candidates. 

#### Candidates Ranking
##### Preprocessing
For each word, we first try to **shorten** it by keeping only 2 characters for consequentive characters. And then we **replace digits** in the words with its phonic word in order to adapt phonetic substitutions. Specifically, we use following dictionary.
```
{
	'0':'o',
	'1':'one',
	'2':'too',
	'3':'thr',
	'4':'for',
	'5':'five',
	'6':'six',
	'7':'seven',
	'8':'ea',
	'9':'nin'
}
``` 

For example, `toooook` would be transformed to `took` and `4eva` would be `foreva`.

After the processing, we use following metrics to score each candidate with the processed word.

##### Edit Distance

The metric measures how many letter insertions, deletions, and replacements needed to transform error word to the given candidate. For example, `foreva` takes 2 operations (one replacement and one insertion) to transform to `forever`. The score is calculated by `1 - #operations / length of candidate`.  Hence, `EditDistanceScore('foreva','forever') = 1 - 2/7 = 0.71`. We implement this scoring method in Dynamic Programming. 
 
##### Abbreviation Matchness

For the cases where length of candidate is at least 2 letters longer than the length of transformed error word, we use a different algorithm to score the matchness. Basically, we measure how many letters in the subsequence of transformed error word can match letters in the candidate word preserving letter order. For example, `tmrw` matches `tomorrow` with 4 letters while `twmr` matches `tomorrow` with only 3 letters. We also use Dynamic Programming to implement this. `AbbrMatchness = length of matched subsequence*2 / (length of transformed error word + length of candidate)`. 

The above 2 methods are used to measure the similarity between the transformed error word and its candidate. The similarty score ranges from 0 to 1. The higher the score is, the better match the candidate is.

##### Term Frequency

We noticed that in many cases, above similarity method alone will find some rare words as the best candidates. So we also put the popularity of the candidate into account. We score each candidate with its frequency in the given dataset. The score is normalized from 0 to 1.

##### Dependency Frequency

In some cases, the same error word is supposed to corrected as 2 different words. For example, word `2` is supposed to be corrected by `to` in the sentence `I am about 2 get there` while in the sentence `I am 2 old to play this game` the same word is supposed to be replaced by `too`. Fortunately, we found CMU's Twitter POS Tagger can still produce the correct POS tags given sentence with error words in most cases. So we count the POS tag distribution for each correct word in the given dataset. An additional score is given by the product of tag frequency and confidence produced by POS Tagger. 


As lack of training data, we simply sum the above 3 scores together as the final score to measure each candidate. We pick the candidate with highest score as the replacement to the error word.

##### Cases study
`I lve you -> I love you`

`I will see you tmrw -> I will see you tomorrow`

`I will be with uu 4eva -> I will be with u forever`

`how r u doing 2day -> how r u doing today`
