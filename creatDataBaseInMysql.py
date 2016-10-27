#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author guotxie

'''
创建数据库：库名为入参
在数据库中创建表，表名为入参
注：暂时不考虑合并单元格
'''
import re
import MySQLdb
import logging

from readConf import getMysqlConnectionParameter

def unicodeToUtf8(transferString):
	return transferString.encode("utf-8")

def connectMysql(configFilePath):
	'''
	与数据库创建连接
	'''
	mysqlParameterDict = getMysqlConnectionParameter(configFilePath)
	# print mysqlParameterDict
	# print unicodeToUtf8(mysqlParameterDict["host"])
	conn = MySQLdb.connect(host=unicodeToUtf8(mysqlParameterDict["host"]), 
						   user=unicodeToUtf8(mysqlParameterDict["user"]), 
						   passwd=unicodeToUtf8(mysqlParameterDict["passwd"]),
						   use_unicode=True,
						   charset=unicodeToUtf8(mysqlParameterDict["charset"]),)
	cursor = conn.cursor()
	return [conn, cursor]


def creatDatabase(cursor, dbname):
	'''
	创建数据库
	'''
	query = "drop database if exists %s" % dbname
	cursor.execute(query)
	query = "create database %s" % dbname
	cursor.execute(query)

def useDataBase(cursor, dbname):
	'''
	使用特定数据库
	'''
	query = "use %s" % dbname
	cursor.execute(query)

def releaseConnect(conn, cursor):
	cursor.close()
	conn.close()

def replaceSpecialChar(string):
	'''
	正则表达式替换路径特殊字符'/'、'\'和'.'字符为'_'
	'''
	pattern = "[\\|/\|\.]"
	replaceString = "_"
	stringAfterRe = re.sub(pattern, replaceString, string);
	return stringAfterRe


def creatTable(cursor, tableName, attributesList):
	'''
	根据表名和属性，创建数据库表
	'''
	tableAttribute = ""
	(attribute, value) = attributesList[0]
	tableAttribute = "%s varchar(%d)" % (attribute, value)
	for (attribute, value) in attributesList[1:]:
		tempString = ",%s varchar(%d)" % (attribute, value)
		tableAttribute += tempString

	query = "create table if not exists %s(%s)" % (replaceSpecialChar(tableName), replaceSpecialChar(tableAttribute))
	cursor.execute(query)


def insertRecordIntoDataTable(conn, cur, tableName, records, colNum):
	'''
	'''
	try:
		tableNameAfterRe = replaceSpecialChar(tableName)
		# 构造插入数据的字符串
		recordString = "%s, " * colNum
		recordString = recordString[0:-2]
		sql = 'insert into %s values(%s)' % (tableNameAfterRe, recordString)
		# 一条条插入
		'''
		for record in records:
			cur.execute(sql, record)
			conn.commit()
		'''
		# 批量插入  
		cur.executemany(sql, records)
		conn.commit()
	except Exception as e:
		print e
		logging.warning('insert data error in table:%s exception: %s' % (tableNameAfterRe, e))
		conn.rollback()
	logging.debug('[insert table %s] total: %d' % (tableNameAfterRe, len(records)))


def test():
	configFilePath = r"E:\xieguotao\work\python\plotVoa\mysql.conf"
	# 创建mysql链接
	[conn, cursor] = connectMysql(configFilePath)
	# 创建数据库
	creatDatabase(cursor = cursor, dbname = "中文test")
	# 关闭连接，释放资源
	cursor.close()
	conn.close()

if __name__ == "__main__":
    test()
