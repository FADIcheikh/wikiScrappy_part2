# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.markup import remove_tags
import re
from ..items import WikiscrapyPart2Item


class WikiSpiderSpider(scrapy.Spider):
    name = 'wiki_spider'
    start_urls = ['https://en.wikipedia.org/wiki/January_1']

    def parse(self, response):

        items = WikiscrapyPart2Item()

        events = response.css('#mw-content-text h3+ ul li').extract()
        all_days = response.css('tbody tr td li a::attr(href)').extract()



            #print ('year: '+year+' event: '+event)

        for day in all_days:
            next_url ='https://en.wikipedia.org/'+str(day)
            # recuper day et month
            day = re.search('([A-Za-z]*)_([0-9]*)', day)
            month = day.group(1)
            day = day.group(2)

            for eve in events:
                clean_event = remove_tags(eve)
                year = re.search("([0-9 A-Z a-z \ ]*)\–([a-z A-Z 0-9 \ ,\- \. \" \: \'\(\)]*)", clean_event)

                event = year.group(2)
                year = year.group(1)

                items ['day'] = day
                items ['month'] = month
                items['year'] = year
                items['event'] = event


                yield items

            yield response.follow(next_url, callback=self.parse)