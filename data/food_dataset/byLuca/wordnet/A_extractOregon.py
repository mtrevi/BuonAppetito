import re
import json
import string

'''
Reads and parses Oregon State University Crawl files
'''
result = [];
all_words = set()

crawl = json.load(open('db/oregon_crawl.json'))
for crawl_element in crawl:
	print crawl_element

	url = crawl_element['url']
	names = crawl_element['names'].lower().strip()
	description = crawl_element['description']
	meaning = string.join(description).strip()

	names_split = re.split(',\s+', names)

	for name in names_split:
		# remove parenthesis
		name = re.sub('\(.*\)', '', name).strip()

		# change spaces by underscore
		name = re.sub('\s+', '_', name)

		if (name == ''):
			continue

		result.append({
			'word': name,
			'meaning': meaning
			})

json.dump(result, open('output/oregon_result.json', 'w'))
json.dump(list(set(map(lambda x : x['word'], result))), open('output/oregon_words.json', 'w'))