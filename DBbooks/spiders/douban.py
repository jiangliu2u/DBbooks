import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from DBbooks.items import DbbooksItem
import time


class DBbooks(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['https://movie.douban.com/top250?start=']
    base_url = 'https://book.douban.com/top250?start='

    def start_requests(self):
        for i in range(0, 9):
            url = self.base_url + str(i * 25)
            yield Request(url, self.parse)

    def parse(self, response):
        items = DbbooksItem()
        all_tables = BeautifulSoup(response.text, 'lxml').find('div', class_='indent').find_all('table')
        for table in all_tables:
            title = table.find('div', class_='pl2').find('a')['title']  # 书名
            items['name'] = title
            info = table.find('p', class_='pl').get_text()  # 作者，出版社，时间等信息
            info_list = []
            info_list1 = info.split('/')
            for j in info_list1:
                h = j.replace(' ', '')
                info_list.append(h)
            items['author'] = info_list[0]
            if len(info_list) == 4:  # 外文书籍有翻译人员，信息长度为4
                items['time'] = info_list[2]
            else:
                items['time'] = info_list[3]
            rating_nums = table.find('span', class_='rating_nums').get_text()
            items['rate'] = rating_nums
            # rating_people1 = table.find('span', class_='pl').get_text().replace('\n', '')
            # rating_people = rating_people1.replace(' ', '')
            quote = table.find('span', class_='inq').get_text()
            items['quote'] = quote
            yield items
