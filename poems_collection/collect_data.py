#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 21:40
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


import re
from utils.io_util import save_as_pickle
from utils.preprocessor import hash_index
from utils.sql_util import SqliteOperation
from poems_collection.poems_crawler_config import *
from poems_collection.poem_crawler import PoemCrawler

TEXT_HASH_INDICES = {}
LINKS = []
SAVE_PATH = "../backups"


# 诗文标签爬取
def get_tags():
    sql_conn = SqliteOperation("../poems_data.db")
    tags_url = context_target["poems_tags"]["url"]
    tags_xpath = context_target["poems_tags"]["xpath"]
    tags = PoemCrawler.easy_crawler(tags_url, tags_xpath)
    for data in enumerate(tags):
        sql_conn.insert_one("poems_tags", data)
    sql_conn.close()
    print("All tags has been collected")


# 名句爬取
def get_rhesis():
    sql_conn = SqliteOperation("../poems_data.db")
    rhesis_url_rule = context_target["rhesis"]["sub_pages"]
    pr = context_target["rhesis"]["page_range"]
    detail = context_target["rhesis"]["rhesis_detail"]
    for pn in range(pr[0], pr[1]):
        print("Rhesis:::Is crawling the page-{}...".format(pn))
        main_url = rhesis_url_rule.format(pn)
        outcome = PoemCrawler.easy_crawler(main_url, **detail)
        sentences = outcome["sentences"]
        reference = outcome["reference"]
        assert len(sentences) == len(reference)
        for idx, ref in enumerate(reference):
            ref = re.sub("[《》]", "", ref.strip())
            if ref not in TEXT_HASH_INDICES:
                TEXT_HASH_INDICES[ref] = hash_index(ref)
            poem_id = TEXT_HASH_INDICES[ref]
            sql_conn.insert_one("rhesis", (poem_id, sentences[idx]))
    sql_conn.close()
    print("All rhesis have been collected!")


# 唐诗、古诗、宋词、元曲爬取
def get_ancient_text():
    sql_conn = SqliteOperation("../poems_data.db")
    detail = context_target["text_detail"]
    no_page_turn = fix_urls["no_page_turning"]
    to_page_turn = fix_urls["to_page_turning"]
    classical_part = sub_links_target["classical_ancient_text"]
    total_part = sub_links_target["total_ancient_text"]

    c_count = 0
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

                ref = writer+title
                if ref in TEXT_HASH_INDICES:
                    continue
                else:
                    TEXT_HASH_INDICES[ref] = hash_index(ref)
                text_index = TEXT_HASH_INDICES[ref]
                sql_conn.insert_one("poems_summary", (text_index, title, writer, dynasty, tags, style, tmp_type))

                s_id = 1
                c_count += 1
                for sentence in ancient_text:
                    sql_conn.insert_one("poems_context", (text_index, sentence, s_id))
                    s_id += 1
                if c_count % 100 == 0:
                    print("Classical ancient text collected num: {}...".format(c_count))
    print("Classical ancient texts have been collected!")
    t_count = 0
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

                ref = writer + title
                if ref in TEXT_HASH_INDICES:
                    continue
                else:
                    TEXT_HASH_INDICES[ref] = hash_index(ref)
                text_index = TEXT_HASH_INDICES[ref]
                sql_conn.insert_one("poems_summary", (text_index, title, writer, dynasty, tags, "unk", tmp_type))

                s_id = 1
                t_count += 1
                for sentence in ancient_text:
                    sql_conn.insert_one("poems_context", (text_index, sentence, s_id))
                    s_id += 1
                if t_count % 1000 == 0:
                    print("Other ancient text collected num: {}...".format(t_count))
    print("Other ancient texts have been collected!")
    sql_conn.close()


# 古书籍爬取
def get_books():
    sql_conn = SqliteOperation("../poems_data.db")
    books_url = books_target["books_url"]
    title_xpath = books_target["title"]
    book_one_info = books_target["book_one_info"]
    detail = books_target["detail"]

    for main_url in books_url:
        book_title = PoemCrawler.easy_crawler(main_url, title_xpath)
        section_links = PoemCrawler.sub_links_crawler(main_url, partitioned=True, **book_one_info)
        for sub_links in section_links.values():
            for link in sub_links:
                p_id = 0
                text_detail = PoemCrawler.easy_crawler(link, **detail)
                section_title = text_detail["title"]
                paragraphs = text_detail["paragraph"]
                for pa in paragraphs:
                    p_id += 1
                    sql_conn.insert_one("books", (book_title, section_title, pa, p_id))
        print("《{}》 has been collected.".format(book_title))
    sql_conn.close()
    print("Books have been collected!")

if __name__ == "__main__":
    # from concurrent.futures import ThreadPoolExecutor
    funs = [get_ancient_text, get_rhesis, get_tags]
    for f in funs:
        print("Launch function:【{}】".format(f.__name__))
        f()
    # num_thread = 3
    # executor = ThreadPoolExecutor(num_thread)
    # futures = []
    # for i in range(num_thread):
    #     print("start thread 【{}】 and launch the function 【{}】".format(i, funs[i].__name__))
    #     futures.append(executor.submit(funs[i]))
    # executor.shutdown()
    # for future in futures:
    #     future.result()
    # print("over!")

    save_as_pickle(TEXT_HASH_INDICES, "text_hash_indices.pkl", SAVE_PATH)
    save_as_pickle(LINKS, "links.pkl", SAVE_PATH)


