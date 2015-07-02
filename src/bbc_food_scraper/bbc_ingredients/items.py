# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IngredientItem(scrapy.Item):
	url = scrapy.Field()
	name = scrapy.Field()
	description = scrapy.Field()
	image = scrapy.Field()
	item_type = scrapy.Field()

class RecipeItem(scrapy.Item):
	url = scrapy.Field()
	name = scrapy.Field()
	description = scrapy.Field()
	image = scrapy.Field()
	ingredients = scrapy.Field()
	ingredient_urls = scrapy.Field()
	preparation = scrapy.Field()
	item_type = scrapy.Field()

class IngredientRecipeItem(scrapy.Item):
	'''
	This class relates the ingredientItem to its
	recipe.
	'''
	ingredient_url = scrapy.Field()
	recipe_url = scrapy.Field()
	item_type = scrapy.Field()
