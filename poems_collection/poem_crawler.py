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

import re
import requests
from lxml import etree
from utils.sql_util import SqliteOperation


class PoemCrawler:
    """
    兼爬虫、保存一体
    存储数据库指定SQLite
    爬取方法: requests + xpath，需要提供爬取URL和指定内容的xpath
    """
    def __init__(self, sqlite_db=None):
        self._conn = None

        if sqlite_db:
            self._conn = SqliteOperation(sqlite_db)

    @property
    def db_conn(self):
        return self._conn

    @db_conn.setter
    def db_conn(self, sqlite_db):
        self._conn = SqliteOperation(sqlite_db)

    @staticmethod
    def easy_crawler(url, xpath_rule, idx_info=False):
        """
        进入一个页面，爬取这个页面下的内容，get获取方式，指定内容用text即可获取
        :param url: 网页的地址
        :param xpath_rule: 指定内容的xpath
        :param idx_info: 在抓取古文内容时，需要靠URL中的index来定位
        :return: 返回爬取内容
        """
        if idx_info:
            find = re.search(r"view_(\d+).aspx", url)
            assert find
            idx = find.groups()[0]
            xpath_rule = xpath_rule.format(idx)
        target_nodes = PoemCrawler.bulls_eye(url, xpath_rule)
        if isinstance(target_nodes, str):
            tmp = re.split("[。，！？]", target_nodes.strip())
            return [x for x in tmp if len(x) > 0]
        outcomes = []
        for node in target_nodes:
            if node.text:
                content = node.text
            elif node.tail:
                content = node.tail
            else:
                continue
            outcomes.append(content.strip())
        return outcomes

    @staticmethod
    def bulls_eye(url, xpath_rule):
        """
        bulls_eye意为靶心——抓取到指定的内容
        :param url: 
        :param xpath_rule: 
        :return: 
        """
        req = requests.get(url)
        req.encoding = "utf-8"
        html = req.text
        selector = etree.HTML(html)
        return selector.xpath(xpath_rule)

    @staticmethod
    def sub_links_crawler(url, **sub_links):
        """
        进入一个页面，抓取这个页面下的指定次级链接；
        而且在一级页面下我们要分别爬取好几个格式相同的版块。
        :param url: 网页的地址
        :param sub_links: 包含次级链接的信息字典
        :return: 分版块的次级链接集，字典格式
        """
        forum_dict = {}
        root_url = sub_links["root_url"]
        sub_blocks = sub_links["sub_blocks"]
        entity_links = sub_links["entity_links"]

        bulls_eye = PoemCrawler.bulls_eye(url, sub_blocks)
        for be in bulls_eye:
            entity = be.xpath(entity_links["entity"])
            links = be.xpath(entity_links["sub_links"])
            num_links = len(links)
            if len(entity) == 1 and num_links > 0:
                new_links = list(zip([root_url]*num_links, links))
                forum_dict[entity.text] = new_links
        return forum_dict

    def save_to_sqlite(self, data, table):
        """
        将数据存放到对应的表中
        :param data: 
        :param table: 数据存放的表
        :return: 无返回
        """
        assert self.db_conn is not None
        assert isinstance(data, list)
        assert isinstance(self._conn, SqliteOperation)
        for element in enumerate(data):
            self.db_conn.insert_one(table, element)
        print("Save successfully.")


if __name__ == "__main__":
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

