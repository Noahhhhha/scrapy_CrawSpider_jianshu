# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem
import re

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        # 有点链接是相对路径写的，所以可能没有域名，所以前面补*
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        avatar = response.xpath("//a[@class='avatar']/img/@src").get()
        author = response.xpath("//span[@class='name']/a/text()").get()
        pub_time = response.xpath("//span[@class='publish-time']/text()").get().replace("*","")
        # article_id 是藏在url中的
        article_id = response.url.split("?")[0].split("/")[-1]
        # 内容中包含了布局标签
        content = response.xpath("//div[@class='show-content']").get()

        word_count = int(re.findall(r"\d+",response.xpath("//span[@class='wordage']/text()").get())[0]) # 这里不加int转也可以，会自动转
        comment_count = re.findall(r"\d+",response.xpath("//span[@class='comments-count']/text()").get())[0]
        read_count = re.findall(r"\d+",response.xpath("//span[@class='views-count']/text()").get())[0]
        like_count = re.findall(r"\d+",response.xpath("//span[@class='likes-count']/text()").get())[0]
        subjects = ",".join(response.xpath("//div[@class='include-collection']/a/div/text()").getall())

        item = ArticleItem(
            title = title,
            avatar = avatar,
            author = author,
            pub_time = pub_time,
            origin_url = response.url,
            article_id = article_id,
            content = content,
            subjects = subjects,
            word_count = word_count,
            comment_count = comment_count,
            read_count = read_count,
            like_count = like_count
        )

        yield item
