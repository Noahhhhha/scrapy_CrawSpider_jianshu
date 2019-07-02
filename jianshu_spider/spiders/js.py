# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem

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

        item = ArticleItem(
            title = title,
            avatar = avatar,
            author = author,
            pub_time = pub_time,
            origin_url = response.url,
            article_id = article_id,
            content = content
        )

        yield item
