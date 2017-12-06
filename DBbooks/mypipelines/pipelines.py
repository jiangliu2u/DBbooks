from DBbooks.items import DbbooksItem
import pymongo
from DBbooks import settings


class DBbooksPipeline(object):
    def process_item(self, item, spider):
        f = open('D:/豆瓣图书250.txt', 'a')
        connection = pymongo.MongoClient('127.0.0.1', 27017)
        douban = connection.douban
        books = douban.books
        books.insert({"bookname": item['name'], "author": item['author'], "time": item['time'], "rate": item['rate'],
                      "quote": item['quote']})
        f.write(str({"bookname": item['name'], "author": item['author'], "time": item['time'], "rate": item['rate'],
                     "quote": item['quote']}))
        f.close()
        return item
