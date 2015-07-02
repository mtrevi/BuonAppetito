from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from bbc_ingredients.items import IngredientItem, RecipeItem, IngredientRecipeItem
import urlparse
import string

class BbcIngredientsSpider(CrawlSpider):
    name = 'bbc_ingredients_spider'
    allowed_domains = ['www.bbc.co.uk']
    start_urls = [
        'http://www.bbc.co.uk/food/ingredients',
        ]
    rules = [
        # Rule(
        #     link_extractor = LxmlLinkExtractor(
        #         allow=[
        #             '/food/recipes/search\?dishes%5B%5D=.*$',
        #             '/food/recipes/search\?dishes\[]=.*$',
        #         ],
        #     ),
        #     callback = 'parse_ingredient_recipe_page',
        #     follow = True
        # ),
        Rule(
            link_extractor = LxmlLinkExtractor(
                allow='/food/recipes/[\-a-zA-Z0-9_]+_\d+$', 
                # restrict_xpaths='//li'
                deny=[
                    '/food/recipes/search']
                ),
            callback = 'parse_recipe_page',
            follow = True
        ),
        Rule(
            link_extractor = LxmlLinkExtractor(
                allow='/food/[\-a-zA-Z0-9_]+$', 
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
                ),
            callback = 'parse_food_page',
            follow = True
        ),
        # Follow links
        Rule(
            LxmlLinkExtractor(allow='/food/ingredients/by/letter/[a-z]$', restrict_xpaths='//ol[@class="resource-nav"]/li'),
        ),
        Rule(
            LxmlLinkExtractor(
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


    def parse_food_page(self, response):
        log.msg('parse_food_page(%s).' % response.url, level=log.DEBUG)
        sel = Selector(response)
        
        url = response.url
        # Extract the dish name
        ingredient_id = url.split('/food/')[0]

        summary = sel.xpath('//div[@id="summary"]')
        descriptions = summary.xpath('./div/p/text()').extract()
        images = summary.xpath('./img/@src').extract()

        name = summary.xpath('./h1/text()').extract()[0].replace(' recipes', '').strip()
        description = descriptions[0] if len(descriptions) > 0 else None
        image = images[0] if len(images) > 0 else None

        item = IngredientItem()
        item['url'] = url
        item['name'] = name
        item['description'] = description
        item['image'] = image
        item['item_type'] = 'IngredientItem'

        yield item

        # Look for ingredient recipes
        yield Request(
            'http://www.bbc.co.uk/food/recipes/search?dishes[]=%s' % ingredient_id,
            callback=self.parse_ingredient_recipe_page)

    def parse_recipe_page(self, response):
        log.msg('parse_recipe_page(%s).' % response.url, level=log.DEBUG)
        sel = Selector(response)
        
        url = response.url

        try:
            container = sel.xpath('//div[@class="page hrecipe"]')
            descriptions = container.xpath('.//span[@class="summary"]//text()').extract()
            ingredients = container.xpath('.//div[@id="ingredients"]//p[@class="ingredient"]')
            preparation = map(lambda x : string.join(x.xpath('.//text()').extract()), container.xpath('.//div[@id="preparation"]//li[@class="instruction"]/p'))
            images = container.xpath('.//img[@id="food-image"]/@src').extract()

            name = container.xpath('.//div[@class="article-title"]/h1/text()').extract()[0].strip()
            ingredients_text = map(lambda x : string.join(x.xpath('.//text()').extract()), ingredients)
            description = descriptions[0] if len(descriptions) > 0 else None
            image = images[0] if len(images) > 0 else None

            ingredient_urls = []
            for ingredient in ingredients:
                ingredient_urls.append(map(lambda x : 'http://www.bbc.co.uk' + x, ingredient.xpath('.//a[@class="name food"]/@href').extract()))
            
            item = RecipeItem()
            item['url'] = url
            item['name'] = name
            item['description'] = description
            item['ingredients'] = ingredients_text
            item['ingredient_urls'] = ingredient_urls
            item['preparation'] = preparation
            item['image'] = image
            item['item_type'] = 'RecipeItem'

            return item
        except IndexError:
            log.msg('IndexError at URL %s: recrawling web page.' % response.url, level=log.WARNING)
            return Request(response.url, callback=self.parse_recipe_page)

    def parse_ingredient_recipe_page(self, response):
        log.msg('parse_ingredient_recipe_page(%s).' % response.url, level=log.DEBUG)
        sel = Selector(response)
        
        # Check if is any result
        errors = sel.xpath('//h3[@class="error"]').extract()
        if len(errors) > 0:
            log.msg('No recipes for ingredient at URL %s.' % response.url, level=log.INFO)
            return

        ingredient_url = 'http://www.bbc.co.uk' + sel.xpath('//div[@id="queryBox"]/h2/a/@href').extract()[0]

        container = sel.xpath('//div[@id="article-list"]')
        recipe_urls = container.xpath('.//h3/a/@href').extract()

        for recipe_url in recipe_urls:
            recipe_url = 'http://www.bbc.co.uk' + recipe_url

            item = IngredientRecipeItem()
            item['ingredient_url'] = ingredient_url
            item['recipe_url'] = recipe_url
            item['item_type'] = 'IngredientRecipeItem'

            yield item
            yield Request(recipe_url)

        # Follow the links to the next page
        next_urls = container.xpath('//li[@class="pagInfo-page-numbers-next"]/a/@href').extract()
        if len(next_urls) > 0:
            next_url = 'http://www.bbc.co.uk' + next_urls[0]

            yield Request(next_url, callback=self.parse_ingredient_recipe_page)
