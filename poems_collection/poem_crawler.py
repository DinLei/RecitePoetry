#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/12 21:27
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


"""
古诗文爬取总站点——古诗文网：http://www.gushiwen.org/
抓取文献范围：
（1）**** 唐诗三百      ： http://so.gushiwen.org/gushi/tangshi.aspx
（2）***  古诗三百      ： http://so.gushiwen.org/gushi/sanbai.aspx
（3）**   宋词三百      ： http://so.gushiwen.org/gushi/songsan.aspx
（4）**   元曲集        ： http://so.gushiwen.org/type.aspx?p=1&x=元曲
（5）***  名句集        ： http://so.gushiwen.org/mingju/
（6）*    高中文言文    ： http://so.gushiwen.org/wenyan/gaowen.aspx
（7）*** 《声律启蒙》   ： http://so.gushiwen.org/guwen/book_114.aspx
（8）*** 《笠翁对韵》   ： http://so.gushiwen.org/guwen/book_102.aspx
（9）**   诗词标签一览  ： http://so.gushiwen.org/shiwen/tags.aspx
"""

import requests
from lxml import etree
from poems_collection.poems_crawler_config import *


# 进入一个页面，爬取这个页面下的内容，get获取方式
def crawler4get(url, xpath_rule):
    req = requests.get(url)
    req.encoding = "utf-8"
    html = req.text
    selector = etree.HTML(html)
    bulls_eye = selector.xpath(xpath_rule)
    return [x.text for x in bulls_eye]


if __name__ == "__main__":
    tags_url = context_target["poems_tags"]["url"]
    tags_xpath = context_target["poems_tags"]["xpath"]
    tags = crawler4get(tags_url, tags_xpath)
    print(tags[:10])
