# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotestoscrapeItem(scrapy.Item):
    quote: str = scrapy.Field()
    author: str = scrapy.Field()
    author_about_link: str = scrapy.Field()
    tags: list[str] = scrapy.Field()
    author_born_date: str = scrapy.Field()
    author_born_location: str = scrapy.Field()
    author_description: str = scrapy.Field()
