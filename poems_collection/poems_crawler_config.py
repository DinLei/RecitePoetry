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

    "text_detail": {
        "title": "//div[@class='cont']/h1",
        "dynasty": "//div[@class='sons'][1]/div[@class='cont']/p[@class='source']/a[1]",
        "writer": "//div[@class='sons'][1]/div[@class='cont']/p[@class='source']/a[2]",
        "ancient_text": "substring-before(//textarea[@id='txtare{}'],'——')",
        "tags": "//div[@class='sons'][1]/div[@class='tag']/a"
    },

    "rhesis": {
        "sub_pages": "http://so.gushiwen.org/mingju/Default.aspx?p={}",
        "page_range": [1, 144],
        "rhesis_detail": {
            "sentences": "//div[@class='main3']/div[@class='left']/div[@class='sons']/div[@class='cont']/a[1]",
            "reference": "//div[@class='main3']/div[@class='left']/div[@class='sons']/div[@class='cont']/a[2]"
        }
    }
}

sub_links_target = {
    "classical_ancient_text": {
        "root_url": "http://so.gushiwen.org",
        "sub_blocks": "//div[@class='typecont']",
        "sub_links": {
            "block_name": "string(./div[@class='bookMl']/strong)",
            "sub_links": "./span/a/@href"
        }
    },

    "total_ancient_text": {
        "root_url": "http://so.gushiwen.org",
        "sub_links": "//div[@class='sons']/div[@class='cont']/p[1]/a/@href"
    }
}

fix_urls = {
    "no_page_turning": {
        "tang_poems_300": "http://so.gushiwen.org/gushi/tangshi.aspx",
        "ancient_poems_300": "http://so.gushiwen.org/gushi/sanbai.aspx",
        "song_cis_300": "http://so.gushiwen.org/gushi/songsan.aspx",
    },
    "to_page_turning": {
        "total_poems": {
            "url": "http://so.gushiwen.org/type.aspx?p={}&x=%E8%AF%97",
            "page_range": [1, 500]
        },
        "total_cis": {
            "url": "http://so.gushiwen.org/type.aspx?p={}&x=%E8%AF%8D",
            "page_range": [1, 500]
        },
        "total_qus": {
            "url": "http://so.gushiwen.org/type.aspx?p={}&x=%E6%9B%B2",
            "page_range": [1, 130]
        }
    }
}

type_mapper = {
    "tang_poems_300": "诗",
    "ancient_poems_300": "诗",
    "song_cis_300": "词",
    "total_poems": "曲",
    "total_cis": "词",
    "total_qus": "曲",
}

books_target = {
    "book_one_info": {
        "root_url": "http://so.gushiwen.org",
        "sub_blocks": "//div[@class='bookcont']",
        "sub_links": {
            "block_name": "string(./div[@class='bookMl']/strong)",
            "sub_links": "./div/span/a/@href"
        },
    },

    "title": "//div[@class='sonspic']/div[@class='cont']/h1",
    "books_url": [
        "http://so.gushiwen.org/guwen/book_102.aspx",
        "http://so.gushiwen.org/guwen/book_114.aspx"
    ],
    "detail": {
        "title": "//div[@class='cont']/h1",
        "paragraph": "//div[@class='contson']/p"
    }
}


