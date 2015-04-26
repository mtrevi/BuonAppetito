from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from bbc_ingredients.items import IngredientItem, RecipeItem
import string

class BbcIngredientsSpider(CrawlSpider):
    name = 'bbc_ingredients_spider'
    allowed_domains = ['www.bbc.co.uk']
    start_urls = [
        # 'http://www.bbc.co.uk/food/margarita', 
        'http://www.bbc.co.uk/food/ingredients'
        ]
    rules = [
        Rule(
            link_extractor = SgmlLinkExtractor(
                allow='/food/\w+$', 
                deny=[
                    '/food/ingredients', 
                    '/food/recipes', 
                    '/food/chefs', 
                    '/food/techniques', 
                    '/food/about', 
                    '/food/seasons', 
                    '/food/occasions',
                    '/food/menus',
                    '/food/cuisines',
                    '/food/dishes',
                    '/food/my', 
                    '/food/feedback',
                    '/food/programmes',
                    '/food/?$'],
                # restrict_xpaths='//li[@class="resource food"]'
                ),
            callback = 'parse_food_page',
            follow = True
        ),
        Rule(
            link_extractor = SgmlLinkExtractor(
                allow='/food/recipes/\w+_\d+$', 
                # restrict_xpaths='//li'
                ),
            callback = 'parse_recipe_page',
            follow = True
        ),

        # Follow links
        Rule(
            SgmlLinkExtractor(allow='/food/ingredients/by/letter/[a-z]$', restrict_xpaths='//ol[@class="resource-nav"]/li')
        ),
        Rule(
            SgmlLinkExtractor(
                allow=[
                    '/food/seasons',
                    '/food/recipes',
                    '/food/occasions',
                    '/food/menus',
                    '/food/cuisines',
                    '/food/dishes',
                    '/food/programmes'
                ],
                deny = [
                    '/food/recipes/search',
                    '/sharetools',
                    '/cgi-perl',
                    '/food/.*/share$',
                    '/food/.*/shopping-list$'
                ])
        ),
    ]

    def parse_ingredient_page(self, response):
        sel = Selector(response)
        # parse name when in h1/i/b
        ingredients = sel.xpath('//li[@class="resource food"]/a[1]')
        for ingredient in ingredients:
            item = IngredientItem()

            url = ingredient.xpath('./@href').extract()[0]
            item['url'] = 'http://www.bbc.co.uk' + url

            item['name'] = string.join(ingredient.xpath('./text()').extract()).strip()

            yield item

    def parse_food_page(self, response):
        sel = Selector(response)
        
        #
        url = response.url

        summary = sel.xpath('//div[@id="summary"]')
        descriptions = summary.xpath('./div/p/text()').extract()
        images = summary.xpath('./img/@src').extract()

        name = summary.xpath('./h1/text()').extract()[0].replace(' recipes', '')
        description = descriptions[0] if len(descriptions) > 0 else None
        image = images[0] if len(images) > 0 else None

        item = IngredientItem()
        item['url'] = url
        item['name'] = name
        item['description'] = description
        item['image'] = image

        return item

    def parse_recipe_page(self, response):
        sel = Selector(response)
        
        #
        url = response.url

        container = sel.xpath('//div[@class="page hrecipe"]')
        descriptions = container.xpath('.//span[@class="summary"]//text()').extract()
        ingredients = container.xpath('.//div[@id="ingredients"]//p[@class="ingredient"]')
        preparation = map(lambda x : string.join(x.xpath('.//text()').extract()), container.xpath('.//div[@id="preparation"]//li[@class="instruction"]/p'))
        images = container.xpath('.//img[@id="food-image"]/@src').extract()


        name = container.xpath('.//div[@class="article-title"]/h1/text()').extract()[0]
        ingredients_text = map(lambda x : string.join(x.xpath('.//text()').extract()), ingredients)
        description = descriptions[0] if len(descriptions) > 0 else None
        image = images[0] if len(images) > 0 else None

        ingredient_ids = []
        for ingredient in ingredients:
            ingredient_ids += map(lambda x : 'http://www.bbc.co.uk' + x, ingredient.xpath('.//a[@class="name food"]/@href').extract())
        
        item = RecipeItem()
        item['url'] = url
        item['name'] = name
        item['description'] = description
        item['ingredients'] = ingredients_text
        item['ingredient_ids'] = ingredient_ids
        item['preparation'] = preparation
        item['image'] = image

        return item