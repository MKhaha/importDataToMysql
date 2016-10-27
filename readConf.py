#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author guotxie

import ConfigParser

def getMysqlConnectionParameter(configFile, sections="mySection"):
	cf = ConfigParser.ConfigParser()
	cf.read(configFile)
	secs = cf.sections()

	mysqlConfigParserDict = {s:dict(cf.items(s)) for s in cf.sections()}

	mysqlParameterDict = mysqlConfigParserDict[sections]
	return mysqlParameterDict

def test():
	getMysqlConnectionParameter()

if __name__ == "__main__":
    test()