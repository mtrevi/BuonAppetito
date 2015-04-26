import re
import json
import string

'''
Reads and parses BBC Ingredients Crawl files
'''
result = [];
all_words = set()

crawl = json.load(open('db/bbc_crawl.json'))
for crawl_element in crawl:
	# print crawl_element

	url = crawl_element['url']
	name_str = crawl_element['name'].lower().strip()
	description = crawl_element['description']
	
	# Split name if multiple parts
	names = re.split('((^|\s+)[()])|((^|\s+)(with|and|\w+[-\s]style)($|\s+))|([,]($|\s+))', name_str)
	# names += [re.sub('[^\w\s]', '', name_str)]
	
	# Skip detected groups
	names = [names[i] for i in range(0, len(names), 9)]

	print name_str + ' -> ' + str(names)
	
	names = set(names + [name_str])
	for name in names:
		name = name.strip()
		if name == '':
			continue

		name = re.sub('[^\w\s]', '', name)
		name = re.sub('\s+', '_', name)
		result.append({
			'word': name,
			'meaning': description
			})	

json.dump(result, open('output/bbc_result.json', 'w'))
json.dump(list(set(map(lambda x : x['word'], result))), open('output/bbc_words.json', 'w'))