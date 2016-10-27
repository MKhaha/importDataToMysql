#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author guotxie

from collections import Counter
from getDataListFromVoaDataBase import getDataListFromVoaDataBase
import numpy as np
import matplotlib.pyplot as plt

import math


def localPrint(str=""):
	'''
	decode chinese to utf-8, and encode it to gbk
	'''
	print str.decode("utf-8").encode("gbk")

def transferData(dataDict):
	'''
	transfer key string to int
	'''
	dataAfterTransfer = {}
	for (key, value) in dataDict.iteritems():
		dataAfterTransfer[int(key.encode('utf-8'))] = value
	return dataAfterTransfer

def plotBar(dataDict):
	priceList = dataDict.keys()
	priceList.sort()
	x_pos = np.arange(len(priceList))
	numberOfBuyer = []
	for price in priceList:
		numberOfBuyer.append(dataDict[price])
	print numberOfBuyer

	width = 1
	plt.figure(figsize = (10, 10))
	plt.bar(x_pos, numberOfBuyer, width, color='orange')
	plt.xticks(x_pos + width / 2, priceList, rotation=40)
	plt.xlabel("price")
	plt.ylabel("purchase amount")
	plt.show()

def sortOutData(dataDict, sectionCount=10):
	dataDictSorted = sorted(dataDict.iteritems(), key = lambda pair:pair[0], reverse=False)
	print dataDictSorted
	pirceKeys = dataDict.keys()
	minPriceKey = min(pirceKeys)
	maxPriceKey = max(pirceKeys)
	delta = float(maxPriceKey - minPriceKey) / sectionCount
	dataAfterSortOut = {}
	leftNum = minPriceKey
	for i in range(sectionCount):
		if i == sectionCount - 1:
			rightNum = maxPriceKey
		else:
			rightNum = leftNum + delta
		middleNum = leftNum + delta / 2
		priceSectionCount = 0
		for (key, value) in dataDict.iteritems():
			if key >= leftNum and key <= rightNum:
				priceSectionCount += value
		dataAfterSortOut[int(math.floor(leftNum))] = priceSectionCount
		leftNum = rightNum
	print dataAfterSortOut
	return dataAfterSortOut


def getPriceList():
	query = "select %s from test" % "金额"
	(count, priceList) = getDataListFromVoaDataBase(query)
	str = "总共有 %s 条记录" % count
	localPrint(str)
	str = "空记录数为：%s" % (count - len(priceList))
	localPrint(str)

	return priceList


def pricePlot():
	'''
	get data from database, plot some of them
	'''
	priceList = getPriceList()
	sizeDict = dict(Counter(priceList))
	print sizeDict
	dataAfterTransfer = transferData(sizeDict)
	localPrint(str)
	print dataAfterTransfer
	dataAfterSortOut = sortOutData(dataAfterTransfer, 30)

	plotBar(dataAfterSortOut)

if __name__ == "__main__":
    pricePlot()