#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/10 11:58
'''
# 一定要和单元测试框架一起用
import unittest, os
from ddt import ddt, data, unpack, file_data

'''NO.2多数据拆分，重点来了'''


@ddt
class Testwork(unittest.TestCase):

    @data({'name': 'lili', 'age': '16'}, {'name': '易水寒', 'age': '13'})
    @unpack
    def test_01(self, name, age):
        print(name, age)


if __name__ == '__main__':
    unittest.main()
