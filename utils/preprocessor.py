#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 13:40
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

import hashlib
from pypinyin import pinyin, lazy_pinyin, Style


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


def char2pinyin(var_str, style=Style.FINALS_TONE3):
    """
    将汉字（串）转为拼音（串）
    :param style:  该包内指定的返回拼音格式
    :param var_str:  str 类型的字符串
    :return: 汉字转小写拼音
    """
    if isinstance(var_str, str):
        if var_str == 'None':
            return ""
        else:
            tmp = pinyin(var_str, style)
            return " ".join(flatten(tmp))
    else:
        return '类型不对'


def flatten(arr_list):
    assert isinstance(arr_list, list)
    out = []
    for ele in arr_list:
        if isinstance(ele, list):
            out.extend(flatten(ele))
        else:
            out.append(ele)
    return out


if __name__ == "__main__":
    test_str = "窗前明月光"
    print(char2pinyin(test_str))

