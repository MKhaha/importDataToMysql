#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author guotxie

import MySQLdb

def getDataListFromVoaDataBase(query):
	conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='MKhaha_05050909', db='informationofbuyer', charset='utf8')
	'''
	print database encode format
	print conn.character_set_name()
	'''
	cur = conn.cursor()
	count = cur.execute(query)

	"""
	count = cur.execute("describe test")
	result = cur.fetchall();
	print result
	for item in result:
		for seq in item:
			print seq
		print item
	"""

	dataList = []

	result = cur.fetchall();
	for item in result:
		for seq in item:
			if seq:
				dataList.append(seq)
				
	cur.close()
	conn.close()

	return (count, dataList)

