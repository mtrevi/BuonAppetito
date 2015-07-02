import json
import string
import nltk
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stopwords = stopwords.words('english')

def create_node(word, is_final):
	return {
		'word': word,
		'is_final': is_final,
		'children': {}
	}

def create_trie(words, sep='_'):
	trie = create_node(None, False)

	for word in words:
		word_split = word.split(sep)
		
		# Lemmatize words and remove stopwords
		word_split = [lemmatizer.lemmatize(word_split_element) for word_split_element in word_split if word_split_element not in stopwords]

		node = trie
		path = []
		## keep only NN
		## select only nouns from l_words
		# word_split = [w for w,pos in pos_tag( word_split ) if pos == 'NN']
		for word_split_element in word_split:
			if word_split_element == '':
				continue

			path.append(word_split_element)
			if (word_split_element in node['children']):
				new_node = node['children'][word_split_element]
			else:
				new_node = create_node(string.join(path, ' '), False)
				node['children'][word_split_element] = new_node

			node = new_node
		node['is_final'] = True
	return trie

## read food names
bbc_menupages_words = ''
## space separeted words or combination of words (each one "_" separated)
for line in open('bbc_menupages.all.names'):
	bbc_menupages_words += line.strip() + ' '
bbc_menupages_words = bbc_menupages_words.lower().strip()

bbc_menupages_trie = create_trie( bbc_menupages_words.split(' ') )

json.dump(bbc_menupages_trie, open('bbc_menupages-trie.json', 'w'))
