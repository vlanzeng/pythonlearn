#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# �����ݿ�����
db = MySQLdb.connect("localhost","zengwei","monalida","DEVELOPE" )

# ʹ��cursor()������ȡ�����α� 
cursor = db.cursor()

# ʹ��execute����ִ��SQL���
cursor.execute("SELECT VERSION()")

# ʹ�� fetchone() ������ȡһ�����ݿ⡣
data = cursor.fetchone()

print "Database version : %s " % data

# �ر����ݿ�����
db.close()