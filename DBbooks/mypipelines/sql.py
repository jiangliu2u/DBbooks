import pymysql
from DBbooks import settings

MYSQL_HOST = settings.MYSQL_HOST
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB, port=3306, charset='utf8')
cursor = db.cursor()


class Sql:
    @classmethod
    def insert_douban_book(cls, name, author, time, rate,item):
        sql = 'INSERT INTO douban (name,author,time,rate) VALUES (%s,%s,%s,%s,%s)'
        cursor.execute(sql, (item['name'],item['author'],item['time'],item['rate']))
        db.commit()
