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


class PoemCrawler:
    """
    兼爬虫、保存一体
    存储数据库指定SQLite
    爬取方法: requests + xpath，需要提供爬取URL和指定内容的xpath
    """
    @staticmethod
    def easy_crawler(url, **xpath_dict):
        """
        进入一个页面，爬取这个页面下的内容，get获取方式，指定内容用text即可获取
        :param url: 网页的地址
        :param xpath_rule: 指定内容的xpath
        :return: 返回爬取内容
        """
        assert isinstance(xpath_dict, dict)
        target_nodes = PoemCrawler.bulls_eye(url, **xpath_dict)

        fruits = {}
        for key, element in target_nodes.items():
            if isinstance(element, str):
                tmp = re.split("[。，！？]", element.strip())
                fruits[key] = [x for x in tmp if len(x) > 0]
                continue
            outcomes = []
            for node in element:
                if node.text:
                    content = node.text
                elif node.tail:
                    content = node.tail
                else:
                    continue
                outcomes.append(content.strip())
            fruits[key] = outcomes
        return fruits

    @staticmethod
    def bulls_eye(url, *xpath_list, **xpath_dict):
        """
        bulls_eye意为靶心——抓取到指定的内容
        :param url: single-html-page
        :param xpath_dict: xpath规则，字典格式
        :return: nothing
        """
        assert isinstance(xpath_dict, dict)
        target_nodes = {}
        req = requests.get(url)
        req.encoding = "utf-8"
        html = req.text
        selector = etree.HTML(html)
        for key, rule in xpath_dict.items():
            print("key is {} and rule is {}".format(key, rule))
            if key == "ancient_text":
                find = re.search(r"view_(\d+).aspx", url)
                assert find
                idx = find.groups()[0]
                rule = rule.format(idx)
            target_nodes[key] = selector.xpath(rule)
        return target_nodes

    @staticmethod
    def sub_links_crawler(url, **sub_links_dict):
        """
        进入一个页面，抓取这个页面下的指定次级链接；
        而且在一级页面下我们要分别爬取好几个格式相同的版块。
        :param url: 网页的地址
        :param sub_links_dict: 包含次级链接的信息字典
        :return: 分版块的次级链接集，字典格式
        """
        assert isinstance(sub_links_dict, dict)
        print("the parameter is {}".format(sub_links_dict))
        forum_dict = {}
        root_url = sub_links_dict["root_url"]
        sub_blocks = sub_links_dict["sub_blocks"]
        entity_links = sub_links_dict["entity_links"]

        target_nodes = PoemCrawler.bulls_eye(url, )
        for element in target_nodes.values():
            print("the element is {}".format(element))
            entity = element.xpath(entity_links["entity"])
            links = element.xpath(entity_links["sub_links"])
            num_links = len(links)
            if len(entity) == 1 and num_links > 0:
                new_links = list(zip([root_url]*num_links, links))
                forum_dict[entity.text] = new_links
        return forum_dict
