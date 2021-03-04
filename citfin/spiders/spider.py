import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import CitfinItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class CitfinSpider(scrapy.Spider):
	name = 'citfin'
	start_urls = ['https://www.citfin.eu/category/news-press-releases/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time[@class="entry-date published"]/text()').get()
		date = ''.join([el.strip() for el in date if el.strip()])
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="entry-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=CitfinItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
