import scrapy

from quotestoscrape.items import QuotestoscrapeItem


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    absolute_link: str = "https://quotes.toscrape.com"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = [absolute_link]

    def parse(self, response, **kwargs):
        quote_elements = response.xpath('//div[@class="quote"]')
        for quote_element in quote_elements:
            author_about_link = quote_element.xpath('.//span/a/@href').get()
            yield response.follow(url=author_about_link, callback=self.author_parse,
                                  meta= {'quote_element': quote_element, 'author_about_link': author_about_link})

        if next_page := response.xpath('//li[@class="next"]/a/@href').get():
            yield response.follow(url=next_page, callback=self.parse)

    def author_parse(self, response):
        quote_element = response.meta['quote_element']
        author_about_link = response.meta['author_about_link']

        quote_item: QuotestoscrapeItem = QuotestoscrapeItem()

        quote_item['quote'] = quote_element.xpath('./span[@class="text"]/text()').get()
        quote_item['author'] = quote_element.xpath('./span/small[@class="author"]/text()').get()
        quote_item['author_about_link'] = f"{self.absolute_link}/{author_about_link}"
        quote_item['tags'] = quote_element.xpath('./div[@class="tags"]/a/text()').getall()
        quote_item['author_born_date'] = response.xpath('//span[@class="author-born-date"]/text()').get()
        quote_item['author_born_location'] = response.xpath('//span[@class="author-born-location"]/text()').get()[3:]
        quote_item['author_description'] = response.xpath('//div[@class="author-description"]/text()').get().strip()
        yield quote_item