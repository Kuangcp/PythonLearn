import MySQLdb
import datetime

conn= MySQLdb.connect(
        host='118.31.14.157',
        port = 3306,
        user='myth',
        passwd='ad',
        db ='weixin',
        )
cur = conn.cursor()
result = cur.execute("delete from goods where (date_format(goods.end_time, '%Y-%m-%d %H:%i:%s')<current_timestamp())=1 ;")
print(datetime.datetime.now(), "一共自动删除：", end="")
print(result, "条商品数据")
cur.close()
conn.commit()
conn.close()