#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 11:52
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


def test(*args, **kwargs1):
    print("test-args: {}".format(args))
    print("test-kwargs1: {}".format(kwargs1))
    print(test.__name__)
    print("================")

if __name__ == "__main__":
    # import re
    # from poems_collection.poems_crawler_config import *
    # from poems_collection.poem_crawler import PoemCrawler
    from poems_collection.collect_data import get_books
    #
    # tags_url = context_target["poems_tags"]["url"]
    # tags_xpath = context_target["poems_tags"]["xpath"]
    # tags = PoemCrawler.easy_crawler(tags_url, tags_xpath)
    # print(len(tags))
    # print(tags)
    #
    # test_url2 = "http://so.gushiwen.org/view_20788.aspx"
    # print(PoemCrawler.easy_crawler(test_url2, **context_target["text_detail"]))

    # test_url3 = "http://so.gushiwen.org/gushi/tangshi.aspx"
    # test_url4 = "http://so.gushiwen.org/type.aspx?p=300&x=%E8%AF%97"
    # test_url5 = "http://so.gushiwen.org/mingju/Default.aspx?p=5"
    # print(PoemCrawler.sub_links_crawler(test_url4, **sub_links_target["total_ancient_text"]))
    # outcome = PoemCrawler.easy_crawler(test_url5, **context_target["rhesis"]["rhesis_detail"])
    # print(len(outcome))
    # print(outcome)
    # sentences = outcome["sentences"]
    # reference = outcome["reference"]
    # assert len(sentences) == len(reference)
    # for idx, ref in enumerate(reference):
    #     ref = re.sub("[《》]", "", ref.strip())
    #     print(ref, sentences[idx])
    # print(test(test_url3, **sub_links_target))
    # print(PoemCrawler.sub_links_crawler(test_url3, partitioned=True, **sub_links_target["classical_ancient_text"]))

    # test(a=2, b=3)
    # test({"a2": 11, "b2": 22})
    # test(**{"a1": 11, "b1": 22}, **{"a2": 55, "b2": 66})
    # test(*"aa")
    get_books()
