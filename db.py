import pymysql
import time
conn = pymysql.connect(host='192.168.0.194', user='root', password='qwerasdf12', db='raspi_db', charset='utf8')
cursor = conn.cursor()
cursor.execute("select * from collect_data")

sql = "INSERT INTO collect_data(TextData, LastUpdate) VALUES ('studystart', NOW())"
cursor.execute(sql)
conn.commit()
time.sleep(600)

sql = "INSERT INTO collect_data(TextData, LastUpdate) VALUES ('studyfinish', NOW())"
cursor.execute(sql)
conn.commit()

conn.close()