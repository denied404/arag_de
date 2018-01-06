# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AragDeItem(scrapy.Item):
    name = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    street = scrapy.Field()
    zip_city = scrapy.Field()
    city = scrapy.Field()
    zipcode = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    mobile = scrapy.Field()
    email = scrapy.Field()
    homepage = scrapy.Field()
    image_url = scrapy.Field()
    job_position = scrapy.Field()
    company = scrapy.Field()
    pass
