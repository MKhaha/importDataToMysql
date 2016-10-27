#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author guotxie
from random import Random  
from hashlib import md5  
import xlwt  
  
# 获取由4位随机大小写字母、数字组成的salt值  
def create_salt(length = 4):  
    salt = ''  
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'  
    len_chars = len(chars) - 1  
    random = Random()  
    for i in xrange(length):  
        # 每次从chars中随机取一位  
        salt += chars[random.randint(0, len_chars)]  
    return salt  
  
# 获取原始密码+salt的md5值  
def create_md5(pwd,salt):  
    md5_obj = md5()  
    md5_obj.update(pwd + salt)  
    return md5_obj.hexdigest()  
  
# 创建一个xls文件  
book = xlwt.Workbook()  
# 创建一个sheet  
sheet = book.add_sheet('users', cell_overwrite_ok=True)  
# 每列第一行写上列名  
sheet.write(0, 0, 'username')  
sheet.write(0, 1, 'salt')  
sheet.write(0, 2, 'pwd')  
# 生成user数量  
count = 10000  
# 第一个id  
first_id = 311010000  
for i in xrange(count):  
    current_id = str(first_id + i)  
    salt = create_salt()  
    pwd = create_md5(current_id, salt)  
    sheet.write(i+1, 0, current_id)  
    sheet.write(i+1, 1, salt)  
    sheet.write(i+1, 2, pwd)  
# 保存  
book.save('./users.xls')  