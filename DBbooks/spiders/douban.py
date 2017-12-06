import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from DBbooks.items import DbbooksItem
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib


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
            # quote = table.find('span', class_='inq').get_text()
            items['quote'] = 'aaa'
            yield items

    @staticmethod
    def close(spider, reason):
        send_email()


def send_email():
    sender = '****'
    receivers = ['jiangliu2u@163.com']
    mail_user = sender
    mail_pass = '*****'#邮箱客户端的授权码
    message = MIMEMultipart()
    message['From'] = Header("江流", 'utf-8')
    message['To'] = Header("测试", 'utf-8')
    subject = '豆瓣图书250'
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText('利用smtplib发送包含scrapy的items的文本文件', 'plain', 'utf-8'))
    att1 = MIMEText(open('D://1.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="DoubanBooks.txt"'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    message.attach(att1)
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.set_debuglevel(1)
        smtpObj.connect('smtp.qq.com', 465)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
