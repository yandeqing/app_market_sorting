#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/10 11:58
'''
# 一定要和单元测试框架一起用
import unittest, os
from ddt import ddt, data, unpack, file_data

'''NO.2多组元素分解'''
@ddt
class Testwork(unittest.TestCase):

    @data([{'name':'lili','age':12},{'sex':'male','job':'teacher'}])
    @unpack
    def test_01(self,a,b):
        print(a,b)

if __name__ == '__main__':
    unittest.main()