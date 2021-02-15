# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HpWikiItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    path = scrapy.Field()
