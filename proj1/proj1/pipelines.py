# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import html2text
import os
import urllib.parse as parse

class Proj1Pipeline(object):
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    converter.ignore_images = True
    converter.ignore_tables = True
    converter.ignore_emphasis = True
    cwd = os.getcwd()

    def process_item(self, item, spider):
        item['body'] = self.converter.handle(item['body'])
        parse_uri = parse.urlparse(item['url'])
        if not parse_uri.path.startswith('/p'):
            return item
        path = os.path.join(self.cwd, 'page')
        if not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.join(path, '{}.md'.format(parse_uri.path.split('/')[-1]))
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(item['body'])
        return item
