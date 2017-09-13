#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 11:52
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

if __name__ == "__main__":
    from poems_collection.poem_crawler import PoemCrawler
    from poems_collection.poems_crawler_config import context_target

    title = context_target["details"]["title"]
    dynasty = context_target["details"]["dynasty"]
    writer = context_target["details"]["writer"]
    content = context_target["details"]["content"]
    tags = context_target["details"]["tags"]

    my_crawler = PoemCrawler()
    test_url = "http://so.gushiwen.org/view_64154.aspx"
    t1 = my_crawler.easy_crawler(test_url, title)
    d1 = my_crawler.easy_crawler(test_url, dynasty)
    w1 = my_crawler.easy_crawler(test_url, writer)
    tg1 = my_crawler.easy_crawler(test_url, tags)
    c1 = my_crawler.easy_crawler(test_url, content, idx_info=True)

    print(t1)
    print(d1)
    print(w1)
    print(tg1)
    print(c1)
