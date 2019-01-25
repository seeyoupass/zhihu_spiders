# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    question_title=scrapy.Field()
    tags=scrapy.Field()
    question_detial=scrapy.Field()
    answer=scrapy.Field()
    answer_user=scrapy.Field()
    text=scrapy.Field()
    time=scrapy.Field()
    awesome=scrapy.Field()
    comment_total=scrapy.Field()
    url=scrapy.Field()
    comment_name=scrapy.Field()
    comment_content=scrapy.Field()

class ZhihuTopicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    question_title=scrapy.Field()
    tags=scrapy.Field()
    question_detial=scrapy.Field()
    answer=scrapy.Field()
    answer_user=scrapy.Field()
    text=scrapy.Field()
    time=scrapy.Field()
    awesome=scrapy.Field()
    comment_total=scrapy.Field()
    url=scrapy.Field()


class ZhihuqsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    answer_user=scrapy.Field()
    text=scrapy.Field()
    awesome=scrapy.Field()
    comment_total=scrapy.Field()
