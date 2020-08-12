#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/10 11:58
'''
# 一定要和单元测试框架一起用
import unittest, os
from ddt import ddt, data, unpack, file_data


'''NO.2多组未分解元素'''


@ddt
class Testwork(unittest.TestCase):

    @data((1, 2, 3), (4, 5, 6))
    def test_01(self, value):
        print(value)


if __name__ == '__main__':
    unittest.main()

