import pymysql

conn = pymysql.connect(host='10.77.40.27', port=3306, user='tao', passwd='tao', db='py_voucher', charset='utf8')
cur = conn.cursor()
status = cur.execute("delete from t_publish_detail where 1=1")
# cur.execute("insert t_publish_detail_temp select * from t_publish_detail")
conn.commit()
cur.close()
cur = conn.cursor()
# cur.execute("delete from t_publish_detail where 1=1")
cur.close()
conn.close()
