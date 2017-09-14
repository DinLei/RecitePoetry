#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/12 21:27
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


"""
古诗文爬取总站点——古诗文网：http://www.gushiwen.org/
抓取文献范围：
（ 1）**** 唐诗三百      ： http://so.gushiwen.org/gushi/tangshi.aspx
（ 2）***  古诗三百      ： http://so.gushiwen.org/gushi/sanbai.aspx
（ 3）**   宋词三百      ： http://so.gushiwen.org/gushi/songsan.aspx
（ 4）***  名句集        ： http://so.gushiwen.org/mingju/
（ 5）**   诗词标签一览  ： http://so.gushiwen.org/shiwen/tags.aspx
（ 6）*** 《声律启蒙》   ： http://so.gushiwen.org/guwen/book_114.aspx
（ 7）*** 《笠翁对韵》   ： http://so.gushiwen.org/guwen/book_102.aspx
（ 8）**   全古诗        ： http://so.gushiwen.org/type.aspx?p={}&x=%E8%AF%97
（ 9）**   全古词        ： http://so.gushiwen.org/type.aspx?p={}&x=%E8%AF%8D
（10）**   全古曲        ： http://so.gushiwen.org/type.aspx?p={}&x=%E6%9B%B2
（11）*    高中文言文    ： http://so.gushiwen.org/wenyan/gaowen.aspx
"""

import re
import requests
from lxml import etree
from collections import Iterable


class PoemCrawler:
    """
    兼爬虫、保存一体
    存储数据库指定SQLite
    爬取方法: requests + xpath，需要提供爬取URL和指定内容的xpath
    """
    @staticmethod
    def easy_crawler(url, *xpath_rules, **xpath_dict):
        """
        进入一个页面，爬取这个页面下的内容，get获取方式，指定内容用text即可获取
        :param url: 网页的地址
        :param xpath_dict: 指定内容的xpath
        :return: 返回爬取内容
        """
        if xpath_rules:
            fruits = []
            target_nodes = PoemCrawler.bulls_eye(url, *xpath_rules)
            if not isinstance(target_nodes, list):
                target_nodes = [target_nodes]
            for element in target_nodes:
                if isinstance(element, list):
                    outcomes = []
                    for node in element:
                        if node.text:
                            content = node.text
                        elif node.tail:
                            content = node.tail
                        else:
                            continue
                        outcomes.append(content.strip())
                    fruits.append(outcomes[0] if len(outcomes) == 1 else outcomes)
                else:
                    if isinstance(element, str):
                        tmp = re.split("[。，！？]", element.strip())
                        fruits.append([x for x in tmp if len(x) > 0])
                        continue
                    else:
                        if element.text:
                            content = element.text
                        elif element.tail:
                            content = element.tail
                        else:
                            continue
                        fruits.append(content.strip())
            return fruits

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
            fruits[key] = outcomes[0] if len(outcomes) == 1 else outcomes
        return fruits

    @staticmethod
    def bulls_eye(url, *xpath_rules, **xpath_dict):
        """
        bulls_eye意为靶心——抓取到指定的内容
        :param url: single-html-page
        :param xpath_rules: xpath规则，列表格式
        :param xpath_dict: xpath规则，字典格式
        :return: nothing
        """
        req = requests.get(url)
        req.encoding = "utf-8"
        html = req.text
        selector = etree.HTML(html)
        target_nodes = None
        if xpath_rules:
            if len(xpath_rules) == 1:
                return selector.xpath(xpath_rules[0])
            target_nodes = []
            for rule in xpath_rules:
                print("rule is {}".format(rule))
                target_nodes.append(selector.xpath(rule))
        if xpath_dict:
            target_nodes = {}
            for key, rule in xpath_dict.items():
                if key == "ancient_text":
                    find = re.search(r"view_(\d+).aspx", url)
                    assert find
                    idx = find.groups()[0]
                    rule = rule.format(idx)
                target_nodes[key] = selector.xpath(rule)
        return target_nodes

    @staticmethod
    def sub_links_crawler(url, partitioned=False, **sub_links_dict):
        """
        进入一个页面，抓取这个页面下的指定次级链接；
        而且在一级页面下我们要分别爬取好几个格式相同的版块。
        :param url: 网页的地址
        :param partitioned: 判断这个页面是否需要分块进行内容爬取
        :param sub_links_dict: 包含次级链接的信息字典
        :return: 次级链接集
        """
        assert isinstance(sub_links_dict, dict)
        root_url = sub_links_dict["root_url"]
        sub_links = sub_links_dict["sub_links"]
        if partitioned:
            forum_dict = {}
            block_nodes = PoemCrawler.bulls_eye(url, sub_links_dict["sub_blocks"])
            assert isinstance(block_nodes, Iterable)
            for block in block_nodes:
                entity = block.xpath(sub_links["block_name"])
                links = block.xpath(sub_links["sub_links"])
                num_links = len(links)
                if entity and num_links > 0:
                    new_links = [root_url+sl for sl in links]
                    forum_dict[entity] = new_links
            return forum_dict
        else:
            link_nodes = PoemCrawler.bulls_eye(url, sub_links)
            assert isinstance(link_nodes, list)
            num_links = len(link_nodes)
            if num_links > 0:
                return [root_url + ln for ln in link_nodes]
