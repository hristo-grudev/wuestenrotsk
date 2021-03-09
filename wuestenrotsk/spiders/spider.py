import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import WuestenrotskItem
from itemloaders.processors import TakeFirst


class WuestenrotskSpider(scrapy.Spider):
	name = 'wuestenrotsk'
	start_urls = ['https://www.wuestenrot.sk/aktuality']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news news--list grid"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="pagination__arrow ml-4 "]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="text-center "]/text()').get()
		description = response.xpath('//div[@class="fr-view"]//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[contains(@class, "mb-lg-15")]/text()').get()

		item = ItemLoader(item=WuestenrotskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
