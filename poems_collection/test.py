#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 11:52
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


def test(*args, **kwargs1):
    print("test-args: {}".format(args))
    print("test-kwargs1: {}".format(kwargs1))
    print("================")

if __name__ == "__main__":
    from poems_collection.poems_crawler_config import *
    from poems_collection.poem_crawler import PoemCrawler

    # test_url1 = "http://so.gushiwen.org/view_64154.aspx"
    # test_url2 = "http://so.gushiwen.org/view_20788.aspx"
    # test_url3 = "http://so.gushiwen.org/gushi/tangshi.aspx"
    # test_url4 = "http://so.gushiwen.org/type.aspx?p=300&x=%E8%AF%97"
    test_url5 = "http://so.gushiwen.org/mingju/Default.aspx?p=5"
    # print(PoemCrawler.sub_links_crawler(test_url4, **sub_links_target["total_ancient_text"]))
    outcome = PoemCrawler.easy_crawler(test_url5, **context_target["rhesis"]["rhesis_detail"])
    print(len(outcome))
    print(outcome)
    # print(test(test_url3, **sub_links_target))
    # print(PoemCrawler.sub_links_crawler(test_url3, **sub_links_target))
    #
    # test(a=2, b=3)
    # test({"a2": 11, "b2": 22})
    # test(**{"a1": 11, "b1": 22}, **{"a2": 55, "b2": 66})
