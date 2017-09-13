#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 13:40
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


def gene_index(lens, number):
    index = int("1"+"0"*(lens-1))
    count = 0
    while count < number:
        yield index
        count += 1
        index += 1
