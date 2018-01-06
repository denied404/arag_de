import json
import urllib
from lxml import etree
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from arag_de.recaptcha_solver import solve_captcha  
from arag_de.items import AragDeItem


class AragDeSpider(CrawlSpider):
    SEARCH_URL = 'https://www.arag.de/kontakt/arag-vor-ort/'
    IMAGE_ROOT_URL = 'https://www.arag.de'
    name = 'AragDeSpider'
    allowed_domains = ['arag.de', 'arag-partner.de']
    deutch_abc = ['a', 'b']

    def start_requests(self):
#        for fl in self.deutch_abc:
#            for sl in self.deutch_abc:
        params = {
            'cmd': 'name', 
            'query': 'ba', # fl + sl,
            'g-recaptcha-response': solve_captcha(self.SEARCH_URL)
        }
        url = (self.SEARCH_URL + "?%s") % urllib.urlencode(params)
        yield Request(url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        hrefs = response.xpath('//div[@class="partner"]/div[@class="links"]//p/a/@href').extract()
        for href in hrefs:
            yield Request(self.SEARCH_URL + href, callback=self.parse_people)

    def parse_people(self, response):
        item = AragDeItem() 
        partner = '//div[@class="partnerDetail"]'
        item['name'] = response.xpath(partner + '/p/b/text()').extract_first()
        item['street'] = response.xpath(partner + '/span/p[1]/text()').extract_first()
        item['zipcode'] = response.xpath(partner + '/span/p[2]/span[1]/text()').extract_first()
        item['city'] = response.xpath(partner + '/span/p[2]/span[2]/text()').extract_first()
        item['zip_city'] = item['zipcode'] + ' ' + item['city']
        item['homepage'] = response.xpath(partner + '/span/p[contains(label, "Website")]/a/@href').extract_first()
        image_url = response.xpath(partner + '/img/@src').extract_first()
        if image_url:
            item['image_url'] = self.IMAGE_ROOT_URL + image_url
        item['phone'] = response.xpath(partner + '/span/p[contains(label, "Tel.:")]/span/text()').extract_first()
        email = response.xpath(partner + '/span/p[contains(label, "Email:")]/a/@href').extract_first()
        item['email'] = email.replace('mailto:', '')
        item['fax'] = response.xpath(partner + '/span/p[contains(label, "Fax:")]/span/text()').extract_first()
        item['mobile'] = response.xpath(partner + '/span/p[contains(label, "Mobil:")]/span/text()').extract_first()
        
        if item['homepage']:
            yield Request(item['homepage'], callback=self.parse_website, meta=item)
        else:
            yield item

    def parse_website(self, response):
        item = AragDeItem() 
        ga_div = '//div[@id="googleAdress"]'
        for k in item.fields:
            item[k] = response.meta.get(k)
        item['job_position'] = response.xpath(ga_div + '/p[2]/text()').extract_first()
        item['company'] = response.xpath(ga_div + '/div[1]/p[@class="name"]/b/text()').extract_first()
        yield item
