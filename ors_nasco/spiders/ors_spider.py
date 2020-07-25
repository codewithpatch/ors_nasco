# -*- coding: utf-8 -*-
import os
from urllib.parse import urljoin

import scrapy


class OrsSpiderSpider(scrapy.Spider):
    name = 'ors_spider'

    def __init__(self, page_url='', url_file=None, *args, **kwargs):
        self.start_urls = ['https://www.orsnasco.com/storefrontCommerce/']

        if not page_url and url_file is None:
            TypeError('No page URL or URL file passed.')

        if url_file is not None:
            with open(url_file, 'r') as f:
                self.start_urls = f.readlines()
        if page_url:
            # Replaces the list of URLs if url_file is also provided
            self.start_urls = [page_url]

        super().__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.page_login)

    def page_login(self, response):
        token_name = "org.apache.struts.taglib.html.TOKEN"
        token = response.xpath('//*[@name="{}"]/@value'.format(token_name)).extract_first()

        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'usr_name': 'andrew@alpine.supply',
                'usr_password': 'Ors1234!',
                'org.apache.struts.taglib.html.TOKEN': token
            },
            callback=self.after_login
        )

    def after_login(self, response):
        product_categories = response.css(
            '#bs-example-navbar-collapse-1 .navbar__item:nth-child(1) a::text'
        ).re('^\s+(.+)')
        product_category_links = response.css(
            '#bs-example-navbar-collapse-1 .navbar__item:nth-child(1)::attr(href)'
        ).extract()

        for category_link in product_category_links:
            absolute_url = urljoin(self.start_urls[0], category_link)
            yield scrapy.Request(url=absolute_url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        pass