import re
import json

def parse_line(line):
	ret = []

	line = line.rstrip().lower()

	if line.startswith(' '):
		return ret

	line_split = line.split(' | ', 1)
	data = line_split[0]
	meaning = line_split[1]

	data_split = data.split(' ')
	if (data_split[1] == '13' and data_split[2] == 'n'):
		n = int(data_split[3], 16)
		for i in range(4, 4 + 2 * n, 2):
			ret.append({
				'word': data_split[i],
				'meaning': meaning
				})

	return ret

'''
Reads and parses WordNet files
'''
result = [];
for line in open('db/data.noun'):
	print line
	result += parse_line(line)


json.dump(result, open('output/wordnet_result.json', 'w'))
json.dump(list(set(map(lambda x : x['word'], result))), open('output/wordnet_words.json', 'w'))