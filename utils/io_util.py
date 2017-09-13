#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 15:20
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

import os
import glob
import pickle
from utils.sql_util import SqliteOperation


def save_to_sqlite(data, database, table):
    """
    将数据存放到对应的表中，自动添加数值索引
    :param data:
    :param database: 数据库路径
    :param table: 数据存放的表
    :return: 无返回
    """
    assert isinstance(data, list)

    sqlite = SqliteOperation(database)
    for element in enumerate(data):
        sqlite.insert_one(table, element)
    sqlite.close()

    print("Save successfully.")


# 读取pickle
def load_pickle(file, file_dir=None):
    try:
        if file_dir:
            file = file_dir + '/' + file
        with open(file, 'rb') as pkl_file:
            return pickle.load(pkl_file)
    except IOError as ioe:
        print(ioe)
        print("nothing get")


# 将文件存储为pickle
def save_as_pickle(file, save_name, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = output_dir+"/"+save_name
    try:
        with open(save_path, 'wb') as output:
            pickle.dump(file, output)
    except IOError as ioe:
        print("nothing get")
        print(ioe)


# 输出指定文件夹下的指定文件
def get_files(file_dir, extension=""):
    if os.path.exists(file_dir):
        return glob.glob(file_dir+"/*"+extension)
    else:
        print("no this dir!")
