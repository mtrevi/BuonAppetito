# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class IngredientItem(Item):
	url = Field()
	name = Field()
	description = Field()
	image = Field()

class RecipeItem(IngredientItem):
	ingredients = Field()
	ingredient_ids = Field()
	preparation = Field()