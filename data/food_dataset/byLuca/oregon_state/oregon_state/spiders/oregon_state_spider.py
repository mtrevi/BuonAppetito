from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from oregon_state.items import IngredientItem
import string

class OregonStateSpider(CrawlSpider):
    name = 'oregon_state_spider'
    allowed_domains = ['food.oregonstate.edu']
    start_urls = ['http://food.oregonstate.edu/glossary/', 'http://food.oregonstate.edu/glossary/index_2_2_ac.html']
    rules = [
        Rule(
    		SgmlLinkExtractor(allow='/glossary/index_\w+\.html', restrict_xpaths='//td')
    	),
        Rule(
            SgmlLinkExtractor(allow='/glossary/[a-z]+\.html', deny=['/glossary/index_\w+\.html', '/glossary/index\.html'], restrict_xpaths='//td'), 
            'parse_ingredient_item'
        )
    ]

    def parse_ingredient_item(self, response):
        sel = Selector(response)
        ingredient_item = IngredientItem()
        ingredient_item['url'] = response.url

        # parse name when in h1/i/b
        ingredient_item['names'] = string.join(
            sel.xpath('//h1/text()').extract() +
            sel.xpath('//h1//*/text()').extract()
            )
        ingredient_item['description'] = sel.xpath('//dd/text()').extract()
        
        return ingredient_item