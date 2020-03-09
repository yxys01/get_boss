# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetBossItem(scrapy.Item):
    dp_name = scrapy.Field()
    dp_type = scrapy.Field()
    dp_founded = scrapy.Field()
    job_name = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    salary = scrapy.Field()
    state = scrapy.Field()
    description = scrapy.Field()
    welfare = scrapy.Field()
    address = scrapy.Field()

