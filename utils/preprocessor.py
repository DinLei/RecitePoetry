#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 13:40
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

import hashlib


def gene_index(lens, number):
    """
    构建自增的数值索引生成器
    :param lens: 
    :param number: 
    :return: 
    """
    index = int("1"+"0"*(lens-1))
    count = 0
    while count < number:
        yield index
        count += 1
        index += 1


def hash_index(string):
    """
    构建hash索引
    :param string: 字符串
    :return: 
    """
    assert isinstance(string, str)
    string = string.encode()
    return hashlib.md5(string).hexdigest()
