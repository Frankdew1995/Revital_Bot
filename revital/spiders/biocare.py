# -*- coding: utf-8 -*-
import scrapy
from revital.items import RevitalItem



class BiocareSpider(scrapy.Spider):
    name = 'biocare'
    allowed_domains = ['revital.co.uk']
    start_urls = ['http://www.revital.co.uk/biocare?limit=100']

    def parse(self, response):
        urls = response.css("a.product-teaser ::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse_details)
        #following pagination links
        for i in range(2,4):
            base_url = 'http://www.revital.co.uk/biocare?limit=100&p={}'
            next_page_url = base_url.format(i)
            yield scrapy.Request(url = next_page_url,callback = self.parse)





    def parse_details(self,response):
        item = RevitalItem()
        item['upc'] = response.css("ul.product-details-list > li::text")[3].extract()
        item['name'] = response.css("div.col-sm-6 > h1::text").extract()
        item['price'] = response.css("span.price::text")[0].extract()
        item['img'] = response.css("a.thumb-link > img::attr(src)")[0].extract()
        yield item






