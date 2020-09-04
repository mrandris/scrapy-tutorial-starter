import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.logger.info('this is a spider')
        quotes = response.css('div.quote')
        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css('quote_content', '.text::text')
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()
            # yield {
            #     'text': quote.css('.text::text').get(),
            #     'author': quote.css('.author::text').get(),
            #     'tags': quote.css('.tag::text').getall(),
            # }

            author_url = quote.css('.author + a::attr(href)').get()
            self.logger.info('get author page url')
            # go to the author page
            yield response.follow(
                author_url, callback=self.parse_author,
                meta={'quote_item': quote_item}
            )

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_bornlocation', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')
        yield loader.load_item()
        # yield {
        #     'author_name': response.css('.author-title::text').get(),
        #     'author_birthday': response.css('.author-born-date::text').get(),
        #     'author_bornlocation': response.css('.author-born-location::text').get(),
        #     'author_bio': response.css('.author-description::text').get(),
        # }
