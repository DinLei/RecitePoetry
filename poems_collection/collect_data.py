#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 21:40
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


from utils.io_util import save_as_pickle
from utils.preprocessor import hash_index
from utils.sql_util import SqliteOperation
from poems_collection.poems_crawler_config import *
from poems_collection.poem_crawler import PoemCrawler

TEXT_HASH_INDICES = set()
LINKS = []
SQLITE = SqliteOperation("../poems_data.db")
SAVE_PATH = "../backups"


# 诗文标签爬取
def get_tags():
    tags_url = context_target["poems_tags"]["url"]
    tags_xpath = context_target["poems_tags"]["xpath"]
    tags = PoemCrawler.easy_crawler(tags_url, tags_xpath)


# 唐诗、古诗、宋词、元曲爬取
def get_ancient_text():
    detail = context_target["text_detail"]
    no_page_turn = fix_urls["no_page_turning"]
    to_page_turn = fix_urls["to_page_turning"]
    classical_part = sub_links_target["classical_ancient_text"]
    total_part = sub_links_target["total_ancient_text"]

    for t_type, main_url in no_page_turn.items():
        tmp_type = type_mapper[t_type]
        classical_links = PoemCrawler.sub_links_crawler(main_url, partitioned=True, **classical_part)
        for style, sub_links in classical_links.items():
            LINKS.extend(sub_links)
            for link in sub_links:
                text_detail = PoemCrawler.easy_crawler(link, **detail)
                title = text_detail["title"]
                dynasty = text_detail["dynasty"]
                writer = text_detail["writer"]
                ancient_text = text_detail["ancient_text"]
                tags = "|".join(text_detail["tags"])
                text_index = hash_index(writer+title)
                if text_index in TEXT_HASH_INDICES:
                    continue
                TEXT_HASH_INDICES.add(text_index)
                SQLITE.insert_one("poems_summary", (text_index, title, writer, dynasty, tags, style, tmp_type))

                s_id = 1
                for sentence in ancient_text:
                    SQLITE.insert_one("poems_context", (text_index, sentence, s_id))
                    s_id += 1

    for t_type, url_info in to_page_turn.items():
        tmp_type = type_mapper[t_type]
        url_rule = url_info["url"]
        pr = url_info["page_range"]
        for pn in range(pr[0], pr[1]+1):
            main_url = url_rule.format(pn)
            one_page_links = PoemCrawler.sub_links_crawler(main_url, partitioned=False, **total_part)
            LINKS.extend(one_page_links)
            for link in one_page_links:
                text_detail = PoemCrawler.easy_crawler(link, **detail)
                title = text_detail["title"]
                dynasty = text_detail["dynasty"]
                writer = text_detail["writer"]
                ancient_text = text_detail["ancient_text"]
                tags = "|".join(text_detail["tags"])
                text_index = hash_index(writer+title)
                if text_index in TEXT_HASH_INDICES:
                    continue
                TEXT_HASH_INDICES.add(text_index)
                SQLITE.insert_one("poems_summary", (text_index, title, writer, dynasty, tags, "unk", tmp_type))

                s_id = 1
                for sentence in ancient_text:
                    SQLITE.insert_one("poems_context", (text_index, sentence, s_id))
                    s_id += 1

save_as_pickle(TEXT_HASH_INDICES, "text_hash_indices.pkl", SAVE_PATH)
save_as_pickle(LINKS, "links.pkl", SAVE_PATH)

