#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 11:52
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


def test(*args, **kwargs):
    print("test: {}".format(args))
    print("test: {}".format(type(kwargs)))
    print("test: {}".format(kwargs))
    print("================")

if __name__ == "__main__":
    from poems_collection.poems_crawler_config import *
    from poems_collection.poem_crawler import PoemCrawler

    # test_url1 = "http://so.gushiwen.org/view_64154.aspx"
    # test_url2 = "http://so.gushiwen.org/view_20788.aspx"
    test_url3 = "http://so.gushiwen.org/gushi/tangshi.aspx"
    # print(PoemCrawler.easy_crawler(test_url2, **context_target["poem_detail"]))
    # print(test(test_url3, **sub_links_target))
    print(PoemCrawler.sub_links_crawler(test_url3, **sub_links_target))
    #
    # test(a=2, b=3)
    # test({"a2": 11, "b2": 22})
    # test(**{"a2": 11, "b2": 22})
