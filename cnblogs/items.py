# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 排名
    top = scrapy.Field()
    nickName = scrapy.Field()
    userName = scrapy.Field()
    # 积分
    score = scrapy.Field()
    # 所在页码地址
    pageLink = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章链接
    articleLink = scrapy.Field()
    # 文章内容
    content = scrapy.Field()
