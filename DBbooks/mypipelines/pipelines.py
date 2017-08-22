from DBbooks.items import DbbooksItem
import pymysql
from DBbooks import settings

MYSQL_HOST = settings.MYSQL_HOST
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB


def dbHandle():
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB, port=3306,
                           charset='utf8')
    return conn


class DBbooksPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'INSERT INTO douban(name,author,time,rate,quote) VALUES (%s,%s,%s,%s,%s)'
        cursor.execute(sql, (item['name'], item['author'], item['time'], item['quote'], item['rate']))
        dbObject.commit()
        dbObject.close()
        return item
