import MySQLdb

db = MySQLdb.connect(host='127.0.0.1', port=3360, user='root', password='jiushi', db='test',charset='utf8mb4')

cursor = db.cursor()

cursor.execute("SELECT * from ms_xxl_job_qrtz_trigger_log limit 3")
rows = cursor.fetchall()
for row in rows :
    print(row[1],row[3],row[5])
