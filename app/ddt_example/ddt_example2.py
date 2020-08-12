#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/10 11:58
'''
# 一定要和单元测试框架一起用
import unittest, os
from ddt import ddt, data, unpack, file_data

'''NO.3多组分解元素'''


@ddt
class Testwork(unittest.TestCase):

    @data((1, 2, 3), (4, 5, 6))
    @unpack  # 拆分数据
    def test_01(self, value1, value2, value3):  # 每组数据有3个值，所以设置3个形参
        print(value1, value2, value3)


if __name__ == '__main__':
    unittest.main()
