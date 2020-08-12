#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/10 11:58
'''
# 一定要和单元测试框架一起用
import unittest, os
from ddt import ddt, data, unpack, file_data

'''NO.1单组元素'''


@ddt
class Testwork(unittest.TestCase):

    @data(1, 2, 3)
    def test_01(self, value):  # value用来接收data的数据
        print(value)


if __name__ == '__main__':
    unittest.main()
