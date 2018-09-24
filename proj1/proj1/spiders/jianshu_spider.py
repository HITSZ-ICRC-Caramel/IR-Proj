import scrapy
import hashlib
from urllib.parse import urlparse
import os
from proj1.items import Proj1Item
from fake_useragent import UserAgent
from scrapy.selector import Selector

class JianShuSpider(scrapy.Spider):
    name = "jianshu"
    # allowed_domains = 'jianshu.com'
    base_headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
                    'Host': 'www.jianshu.com',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'text/html, */*; q=0.01',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                    'Connection': 'keep-alive',
                    'Referer': 'http://www.jianshu.com'}
    ajax_headers = dict(base_headers, **{"X-PJAX": "true", 'User-Agent': UserAgent().random})

    def start_requests(self):
        urls = [
            'https://www.jianshu.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.base_headers)


    def parse(self, response):
        # print('parse url:', response.url)
        item = Proj1Item()
        # sel = Selector(response)
        # sample = sel.xpath('/*').extract()[0]
        item['url'] = str(response.url)
        item['body'] = str(response.body, 'utf-8')
        yield item
        domain = response.meta.get('domain')
        if not domain:
            parsed_uri = urlparse(response.url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        # print('domain:', domain)
        next_urls = self.get_urls_from_same_domain(domain, response)
        if next_urls:
            for url in next_urls:
                self.log('get url')
                yield scrapy.Request(url, callback=self.parse, meta={'domain': domain}, headers=self.base_headers)


    def get_urls_from_same_domain(self, domain, response):
        # print('----------------------')
        sel = Selector(response)
        urls = set([response.urljoin(href.extract()) for href in sel.xpath('//@href')])
        urls_same_domain = [url for url in urls if url.startswith(domain)]
        return urls_same_domain
