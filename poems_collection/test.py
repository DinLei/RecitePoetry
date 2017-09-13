#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 11:52
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


def test(*args, **kwargs):
    print(args)
    print(type(kwargs))
    print(kwargs)

if __name__ == "__main__":
    from poems_collection.poems_crawler_config import *
    from poems_collection.poem_crawler import PoemCrawler

    # test_url1 = "http://so.gushiwen.org/view_64154.aspx"
    # test_url2 = "http://so.gushiwen.org/view_20788.aspx"
    test_url3 = "http://so.gushiwen.org/gushi/tangshi.aspx"
    # print(PoemCrawler.easy_crawler(test_url2, **context_target["poem_detail"]))
    print(PoemCrawler.easy_crawler(test_url3, **sub_links_target))

    # test(a=2)
