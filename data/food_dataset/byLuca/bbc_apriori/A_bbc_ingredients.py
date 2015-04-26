import json
from apriori import runApriori, printResults

def generateItemsets(items):
	for item in items:
		if ('ingredient_ids' in item):
			yield item['ingredient_ids']



data = json.load(open('../bbc_ingredients/bbc_crawl.json', 'r'));

ingredients = generateItemsets(data)

print 'Computing apriori'

items, rules = runApriori(ingredients, 0.00, 0.80)

printResults(items, rules)