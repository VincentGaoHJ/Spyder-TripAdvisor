#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-09 21:10:05
# Project: TripAdvisor

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Attractions-g294212-Activities-Beijing.html#FILTERED_LIST', callback=self.index_page)
        

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('* > .attraction_element').items():
            self.crawl(each('.listing_title')('a').attr('href'),fetch_type='js', callback=self.detail_page)
        self.crawl(response.doc('.next').attr('href'),callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        file = r'D:\documents_python\spyder_TripAdvisor\content.txt'
        with open(file, 'a+') as f:
            for each in response.doc('.partial_entry').items():
                # print(each.text())
                f.write(each.text()+'\n')   #加\n换行显示
        self.crawl(response.doc('.prw_common_responsive_pagination .primary').attr('href'),callback=self.detail_page)
