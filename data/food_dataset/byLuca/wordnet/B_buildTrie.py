import json
import string
import nltk
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

def create_trie(words):
	trie = create_node(None, False)

	for word in words:
		word_split = word.split('_')
		
		# Lemmatize words and remove stopwords
		word_split = [lemmatizer.lemmatize(word_split_element) for word_split_element in word_split if word_split_element not in stopwords]

		node = trie
		path = []
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

wordnet_words = json.load(open('output/wordnet_words.json'))
oregon_words = json.load(open('output/oregon_words.json'))
bbc_words = json.load(open('output/bbc_words.json'))

wordnet_bbc_words = set(wordnet_words + bbc_words)
all_words = set(wordnet_words + oregon_words + bbc_words)

wordnet_trie = create_trie(wordnet_words)
oregon_trie = create_trie(oregon_words)
bbc_trie = create_trie(bbc_words)
wordnet_bbc_trie = create_trie(wordnet_bbc_words)
all_trie = create_trie(all_words)

json.dump(wordnet_trie, open('output/wordnet_trie.json', 'w'))
json.dump(oregon_trie, open('output/oregon_trie.json', 'w'))
json.dump(bbc_trie, open('output/bbc_trie.json', 'w'))
json.dump(wordnet_bbc_trie, open('output/wordnet_bbc_trie.json', 'w'))
json.dump(all_trie, open('output/all_trie.json', 'w'))
