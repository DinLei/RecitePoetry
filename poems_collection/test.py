#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 11:52
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

import requests
from lxml import etree


def bulls_eye(url, xpath_rule):
    req = requests.get(url)
    req.encoding = "utf-8"
    html = req.text
    selector = etree.HTML(html)
    return selector.xpath(xpath_rule)


def easy_crawler(url, xpath_rule):
    target_nodes = bulls_eye(url, xpath_rule)
    for node in target_nodes:
        if node.text:
            tmp = node.text
        elif node.tail:
            tmp = node.tail
        else:
            continue
        yield tmp.strip()

if __name__ == "__main__":
    url1 = "http://so.gushiwen.org/view_47873.aspx"
    xr1 = "//div[@id='contson47873']/p | //div[@id='contson47873']/p/br | //div[@id='contson47873']"
    tmp1 = easy_crawler(url1, xr1)
    tmp2 = [x for x in tmp1]
    print(tmp1)
    print(tmp2)
    print(len(tmp2))
