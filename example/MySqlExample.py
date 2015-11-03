#!/usr/bin/env python
import sys
import datetime
import logging
import MySQLdb
import subprocess
import traceback
import os
import sys

curTime = datetime.datetime.now()
format1='%Y-%m-%d'
format2='%Y%m%d'
format3='%Y%m%d%H'
nday =  0
nhour = 2

###qs database
dbhostname_qs = '10.10.58.45'
dbusername_qs = 'envideo9'
dbpasswd_qs = 'Ro520564'
dbname_qs = 'envideo9'
dbport_qs = 3306
dbcharset_qs = 'utf8'
###p2p database          mysql -h10.10.57.65 -uP2pStatus -pP2pReport -Dpstest
dbhostname_p2p = '10.10.57.65'
dbusername_p2p = 'P2pStatus'
dbpasswd_p2p = 'P2pReport'
dbname_p2p = 'pstest'
dbport_p2p = 3306
dbcharset_p2p = 'utf8'

def readFile(path):
	l = []
	file = open(os.getcwd()+"/"+path)
	for line in file:
		if(trim(line) != ''):
			l.append(line.split());
	file.close()
	return l
def trim(str):
	str = str.lstrip()
	str = str.rstrip()
	str = str.strip()
	return str

###���÷�������ʽ��ʱ��
def fmtDate(ndayago=0, nhourago=0, dtEnd=curTime, fmt=format1):
	'''
	format datetime
	'''
	period = -ndayago - nhourago * 1.0/24
	dt = dtEnd + datetime.timedelta(days=period)
	fmtStr = dt.strftime(fmt)
	return fmtStr

###���÷�������ʼ�����ݿ�
def getDBConnection(db='qs'):
	'''
	get connection
	'''
	if db == 'qs':
		host = dbhostname_qs
		user = dbusername_qs
		password = dbpasswd_qs
		db = dbname_qs
		port = dbport_qs
		charset = dbcharset_qs
	else:
		host = dbhostname_p2p
		user = dbusername_p2p
		password = dbpasswd_p2p
		db = dbname_p2p
		port = dbport_p2p
		charset = dbcharset_p2p
	try:
		conn = MySQLdb.connect(host, user, password, db, port, charset)
		cursor = conn.cursor()
		return conn, cursor
	except Exception, e:
		import traceback
		traceback.print_exc()
		#log.error('get db connection error!')

###ִ��sql
def updateDb(sql):
	conn, cursor = getDBConnection()
	count = cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()

dt = fmtDate(ndayago=nday,nhourago=nhour,fmt=format3)

##��������������sql�����Ϣ
def saveDaily(sql, filed, dt) :
	dtime = dt[0:8]
	dhour = dt[8:10]
	cmd = '''hive -e "%s" > temp''' %sql
	print cmd
	os.popen(cmd)
	l = readFile('temp')
	del l[0]
	for obj in l:
		if (len(obj) == 3): 
			#1009	4.0.0.31	4113
			print obj
			sql = "insert into r_ifox_collect_hour (%s,version,cid,dtime,dhour) values(%s,'%s','%s','%s','%s') on duplicate key update %s=%s" %(filed,obj[2],obj[1],obj[0],dtime,dhour,filed,obj[2])
			updateDb(sql)
			print sql

###�ձ���������������
def saveBreadDownUserPlayer() :
	sql = "select -1,expand2,count(1)  from logtbl_hour where partdt='%s' and  type='breakdown' and expand3='SHPlayer' group by expand2"  %dt
	saveDaily(sql,'breakdown_player', dt)	

###�ձ��������������û���
def saveBreadDownUserPlayerUV() :
	sql = "select -1,expand2,count(1) from(select max(expand2) expand2 from logtbl_hour where partdt='%s' and  type='breakdown' and expand3='SHPlayer' group by expand1)temp group by expand2"  %dt
	saveDaily(sql,'breakdown_player_uv', dt)	
    
###�ձ���������������
def saveBreadDownUserSohuVA() :
	sql = "select -1,expand2,count(1)  from logtbl_hour where partdt='%s' and  type='breakdown' and expand3='SoHuVA' group by expand2"  %dt
	saveDaily(sql,'breakdown_ifox', dt)	

###�ձ���sohuVA�����û���
def saveBreadDownUserSohuVAUV() :
	sql = "select -1,expand2,count(1) from(select max(expand2) expand2 from logtbl_hour where partdt='%s' and  type='breakdown' and expand3='SoHuVA' group by expand1)temp group by expand2"  %dt
	saveDaily(sql,'breakdown_ifox_uv', dt)	
    
def test():
	saveBreadDownUserPlayer()
	saveBreadDownUserPlayerUV()
	saveBreadDownUserSohuVA()
	saveBreadDownUserSohuVAUV()

if __name__ =='__main__':
	test()
