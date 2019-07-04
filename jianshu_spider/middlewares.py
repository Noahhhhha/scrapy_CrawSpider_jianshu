# -*- coding: utf-8 -*-

from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

# 返回response，截断scrapy框架下一步发送到Download
# 让scrapy框架只负责url的发送和pipeline存储
class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"D:\soft\chromedriver.exe")

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(1) # 需要让scrapy异步框架等等selenium
        try:
            while True:
                showMore = self.driver.find_element_by_class_name('show-more')  # 这个元素（展开更多）可能不存在，所以trycatch
                showMore.click()
                time.sleep(0.3)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response # 截断scrapy