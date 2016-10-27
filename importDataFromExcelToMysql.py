#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author guotxie

'''
读取指定excel
'''
import sys
import xlrd
import datetime
import re
import random
import logging

import creatDataBaseInMysql

filepath = r'E:\xieguotao\work\python\plotVoa\informationOfBuyer.xlsx'
configFilePath = r"E:\xieguotao\work\python\plotVoa\mysql.conf"
logFilePath = r"E:\xieguotao\work\python\plotVoa\test.log"


def loggingModuleInit():
	logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logFilePath,
                filemode='w')


def getFileNameFromPath(filepath):
	return r'informationOfBuyer'


def creatTableAttributes(sheet):
	attributesList = []
	for cell in sheet.row(0):
		if cell.value:
			attributesList.append((cell.value, 255))
		else:
			attributesList.append(("attribute%d" % int(random.random() * 1000), 255))
	return attributesList

def getCellValue(row):
	for cell in row:
		if cell.ctype == 3:
			# year, month, day, hour, minute, second = xlrd.xldate_as_tuple(cell.value, workBook.datemode)
			# py_date = datetime.datetime(year, month, day, hour, minute, second)
			yield xlrd.xldate.xldate_as_datetime(cell.value, 0)
		else:
			yield cell.value


def getSheetDataList(sheet):
	'''
	获取sheet中的数据，返回一个列表之列表，格式如[[一行数据]...[]]
	'''
	nrows = sheet.nrows
	ncols = sheet.ncols
	param = []
	# excel每个sheet中第一行均为数据库表属性名，实际数据从第二行开始
	for rowNum in xrange(1,nrows):
		# print sheet.row(rowNum)
		listTemp = [value for value in getCellValue(sheet.row(rowNum))]
		# print listTemp
		param.append([value for value in getCellValue(sheet.row(rowNum))])
	# print param
	return param

def readWorkBook(filepath):
	workBook = xlrd.open_workbook(filepath)
	dataBaseName = getFileNameFromPath(filepath)

	# 创建mysql链接
	[conn, cursor] = creatDataBaseInMysql.connectMysql(configFilePath)
	# 创建数据库
	creatDataBaseInMysql.creatDatabase(cursor = cursor, dbname = dataBaseName)
	creatDataBaseInMysql.useDataBase(cursor, dataBaseName)

	# sheet = workBook.sheet_by_index(0)
	for sheet in workBook.sheets():
		# 创建数据库表
		creatDataBaseInMysql.creatTable(cursor, sheet.name, creatTableAttributes(sheet))
		# 获取excel表中数据
		records = getSheetDataList(sheet)
		# 将表中数据导入数据库表中
		creatDataBaseInMysql.insertRecordIntoDataTable(conn, cursor, sheet.name, records, sheet.ncols)

	# 关闭连接，释放资源
	creatDataBaseInMysql.releaseConnect(conn = conn, cursor = cursor)

	'''
	for sheet in workSheets:
		firstRow = sheet.row(0)
		#print firstRow
		for cell in firstRow:
			#print cell.value

	firstSheet = workSheets[0]
	for i in xrange(firstSheet.ncols):
		col = firstSheet.col(i)
		for cell in col[1:]:
			if(i == 0):
				# print cell.value
				if cell.value:
					#year, month, day, hour, minute, second = xlrd.xldate_as_tuple(cell.value, workBook.datemode)
					#py_date = datetime.datetime(year, month, day, hour, minute, second)
					py_date = xlrd.xldate.xldate_as_datetime(cell.value, 0)
					#print py_date
					#print str(py_date)
			else:
				#print sys.getsizeof(cell.value)
	'''

def test():
	loggingModuleInit()
	readWorkBook(filepath)

if __name__ == "__main__":
    test()
