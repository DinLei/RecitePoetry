#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/12 23:37
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

context_target = {
    "poems_tags": {
        "url": "http://so.gushiwen.org/shiwen/tags.aspx",
        "xpath": "//div[@class='bookcont']/span/a"
    }
}

sub_links_target = {
    "root_url": "http://so.gushiwen.org",
    "sub_blocks": "//div[@class='typecont']",
    "entity_links": {
        "entity": "./div[@class='bookMl']/strong",
        "sub_links": "./span/a/@href"
    }
}

fix_urls = {
    "tang_poems": "http://so.gushiwen.org/gushi/tangshi.aspx",
    "ancient_poems": "http://so.gushiwen.org/gushi/sanbai.aspx",
    "song_cis": "http://so.gushiwen.org/gushi/songsan.aspx"
}
