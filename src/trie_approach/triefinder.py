import json
import logging
import string

# logger = logging.getLogger('TrieFinder')

class TrieFinder():
	'''
	A class that finds expressions in a text.
	It uses a trie structure to look for expression in an efficient way.
	It receives as input an array of tokens and finds the expressions in the trie.
	'''

	def __init__(self, trie):
		self.trie = trie
	
	def find(self, tokens):
		'''
		Finds the expressions in the tokens.
		The 'tokens' variable is an array of strings.

		It returns a list of expressions that are found.
		Words are separated by space.
		'''

		ret = []
		while len(tokens) > 0:
			path = self.find_helper(tokens, self.trie)
			# logger.debug('Checking for tokens ' + str(tokens))
			if path is None:
				tokens = tokens[1:]
			else:
				ret.append(string.join(path))
				tokens = tokens[len(path):]

		return ret

	def find_helper(self, tokens, node):
		'''
		Finds the tokens in the tree.

		Returns the expression found or None if 
		no match.
		'''

		ret = None
		if len(tokens) > 0:
			next_token = tokens[0]
			# Look for the next token in the trie
			if next_token in node['children']:
				next_node = node['children'][next_token]
				sub_path = self.find_helper(tokens[1:], next_node)
				# Sub expression not found
				if sub_path is None:
					if (next_node['is_final'] == True):
						ret = [next_token]
					else:
						pass
				else:
					ret = [next_token] + sub_path
			else:
				pass

		# logger.debug('find_helper(' + str(tokens) + ',' + str(node['word']) + ') = ' + str(ret))
		return ret

# logging.basicConfig(level=logging.DEBUG)

# trie = json.load(open('wordnet/output/bbc_trie.json'))

# trie_finder = TrieFinder(trie)

# print trie_finder.find('bloody'.split(' '))
# print trie_finder.find('bloody mary'.split(' '))
# print trie_finder.find('wholemeal cheese scone'.split(' '))
# print trie_finder.find('wholemeal cheese'.split(' '))
# print trie_finder.find('wholemeal cheese cheese'.split(' '))
