#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author guotxie

from collections import Counter
from getDataListFromVoaDataBase import getDataListFromVoaDataBase
import numpy as np
import matplotlib.pyplot as plt


def localPrint(str=""):
	'''
	decode chinese to utf-8, and encode it to gbk
	'''
	print str.decode("utf-8").encode("gbk")

def formatSizeString(sizeString):
	'''
	transfer size format, such as 'XXXL' to '3XL'
	'''
	switcher = {u'XXL':u'2XL', u'XXXL':u'3XL', u'XXXXL':u'4XL'}
	if sizeString in switcher:
		return switcher.get(sizeString, u'')
	return sizeString


def sortOutData(dataDict):
	'''
	sort out data, delete null record
	'''
	dataAfterSortOut = {}
	numberOfNullRecord = 0
	for (key, value) in dataDict.iteritems():
		stripString = key.strip()
		if stripString != u'':
			formatString = formatSizeString(stripString)
			if formatString not in dataAfterSortOut:
				dataAfterSortOut[formatString] = value
			else:
				dataAfterSortOut[formatString] += value
		else:
			numberOfNullRecord += value
	"""
	str = "the number of null: %d" % numberOfNullRecord
	print str
	print dataAfterSortOut
	"""
	return dataAfterSortOut

def plotBar(dataDict):
	'''
	plot size vs amount of purchase
	'''
	sizeList = [u'S', u'M', u'L', u'XL', u'2XL', u'3XL', u'4XL']
	x_pos = np.arange(len(sizeList))
	numberOfBuyer = []
	for size in sizeList:
		if size in dataDict:
			numberOfBuyer.append(dataDict[size])
	print numberOfBuyer

	width = 0.5
	plt.bar(x_pos, numberOfBuyer, width, color='orange')
	plt.xticks(x_pos+width/2, sizeList)
	plt.xlabel("size")
	plt.ylabel("purchase amount")
	plt.show()



def getSizeList():
	'''
	get data from database, plot some of them
	'''
	query = "select %s from test" % "尺码"
	(count, sizeList) = getDataListFromVoaDataBase(query)

	str = "总共有 %s 条记录" % count
	localPrint(str)
	str = "空记录数为：%s" % (count - len(sizeList))
	localPrint(str)

	sizeDict = dict(Counter(sizeList))
	print sizeDict
	dataAfterSortOut = sortOutData(sizeDict)
	print dataAfterSortOut
	plotBar(dataAfterSortOut)

if __name__ == "__main__":
    getSizeList()