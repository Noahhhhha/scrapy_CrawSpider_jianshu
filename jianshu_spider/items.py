# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    author = scrapy.Field()
    avatar = scrapy.Field() # 作者头像
    pub_time = scrapy.Field() # 发布时间
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    word_count = scrapy.Field() # 文章字数
    subjects = scrapy.Field() # 专题