# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi

# 新版 异步的pipeline
# 调用 Twisted 提供的连接池
class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host' : '127.0.0.1',
            'port' : 3306,
            'user' : 'root',
            'password' : '123456',
            'database' : 'jianshu',
            'charset' : 'utf8',
            'cursorclass' : cursors.DictCursor # 字典游标，返回值是字典
        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams) # 使用Twisted 提供的连接池，传入使用的驱动，和连接信息
        self._sql = None # 一个下划线是protected

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
                insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s,%s)
             '''
            return self._sql
        return self._sql

    def process_item(self,item,spider):
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider)

    def insert_item(self,cursor,item): # 执行插入操作
        cursor.execute(self.sql,(item['title'],item['content'],item['author'],item['avatar'],item['pub_time'],item['origin_url'],item['article_id']))

    def handle_error(self,error,item,spider): #异常处理
        print('=' * 10 + "error" + '=' * 10)
        print(error)
        print('=' * 10 + "error" + '=' * 10)




# 此pipeline是老版同步的
class JianshuSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host' : '127.0.0.1',
            'port' : 3306,
            'user' : 'root',
            'password' : '123456',
            'database' : 'jianshu',
            'charset' : 'utf8'
        }
        self.conn = pymysql.connect(**dbparams) # “**” 表示将字典作为多个参数传入
        self.cursor = self.conn.cursor() # 游标实现sql语句
        self._sql = None # 一个下划线是protected

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['content'],item['author'],item['avatar'],item['pub_time'],item['origin_url'],item['article_id']))
        self.conn.commit()
        return item

    @property # @property 装饰器将一个直接访问的属性转变为函数触发式属性
    def sql(self):
         if not self._sql :
             self._sql = '''
                insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s,%s)
             '''
             return self._sql
         return self._sql