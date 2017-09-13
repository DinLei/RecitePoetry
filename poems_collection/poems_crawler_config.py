#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/12 23:37
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

context_target = {
    "poems_tags": {
        "url": "http://so.gushiwen.org/shiwen/tags.aspx",
        "xpath": "//div[@class='bookcont']/span/a"
    },

    "details": {
        "title": "//div[@class='cont']/h1",
        "dynasty": "//div[@class='sons'][1]/div[@class='cont']/p[@class='source']/a[1]",
        "writer": "//div[@class='sons'][1]/div[@class='cont']/p[@class='source']/a[2]",
        # "content": "//div[@id='contson{}']/p | //div[@id='contson{}']/p/br | //div[@id='contson{}']",
        "content": "substring-before(//textarea[@id='txtare{}'],'——')",
        "tags": "//div[@class='sons'][1]/div[@class='tag']/a"
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
