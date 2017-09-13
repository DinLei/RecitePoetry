#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/12 23:37
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

import sqlite3


class SqliteOperation:
    """
    operations for sqlite
    """
    def __init__(self, dbname):
        self.__dbname = dbname
        self.__conn = None
        self.__cur = None
        try:
            self.__conn = sqlite3.connect(self.__dbname)
            self.__cur = self.__conn.cursor()
            print("Opened database {} successfully".format(self.__dbname))
        except Exception as e:
            print(e)
            print("can not get {}, please check your environment.".format(self.__dbname))

    def get_data_by_sql(self, sql, to_list=False):
        tmp = self.__conn.execute(sql)
        data = tmp.fetchall()
        if to_list:
            return [x for x in data]
        return data

    def get_data_by_field(self, fields, tbname):
        if isinstance(fields,list):
            fields_names = ','.join(fields)
        elif isinstance(fields,str):
            fields_names = fields
        tmp = self.__conn.execute("select "+fields_names+" from "+tbname)
        data = tmp.fetchall()
        if len(data[0]) == 1:
            return [x[0] for x in data]
        return data

    def count_table_record(self, tbname):
        try:
            count = self.__cur.execute("select count(1) from "+tbname)
            return count.fetchall()[0][0]
        except Exception as e:
            print(e)
            print("there is something wrong with table: "+tbname)

    def insert_one(self, tbname, data=None):
        sql = "insert into "+tbname+" values ("
        try:
            if isinstance(data, list):
                sql += "?," * (len(data) - 1) + "?)"
            else:
                sql += "?)"
                data = (data,)
            self.__cur.execute(sql, data)
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print("insert failed")
            print(e.with_traceback(tbname))

    def insert_batch(self, tbname, data=None):
        sql = "insert into " + tbname + " values ("
        try:
            tmp = data[0]
            if isinstance(tmp, list) or isinstance(tmp, tuple):
                sql += "?," * (len(tmp) - 1) + "?)"
            else:
                sql += "?)"
                data = [(x,) for x in data]
            for row in data:
                self.__cur.execute(sql, row)
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print("insert failed")
            print(e.with_traceback(tbname))

    def update_one(self, tbname, field, data):
        try:
            self.__conn.execute("update "+tbname+" set "+
                                field[0]+" = ? where "+field[1]+" = ?", data)
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print(e.with_traceback(tbname))
            print("update failed")

    def updata_batch(self, tbname, field, data):
        try:
            for row in data:
                self.__conn.execute("UPDATE "+tbname+" set "+
                                    field[0]+" = ? where "+field[1]+"=?", row)
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print(e.with_traceback(tbname))
            print("update failed")

    def delete_all(self, tbname):
        try:
            self.__conn.execute("delete from "+tbname)
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print(e.with_traceback(tbname))
            print("delete fail")

    def delete_all_by_condition(self, tbname, field, condition):
        try:
            self.__conn.execute("delete from "+tbname+" where "+field+" = ?", condition)
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print(e.with_traceback(tbname))
            print("delete fail")

    def get_dbname(self):
        return self.__dbname

    def show_tables(self):
        try:
            tables=self.__conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return tables.fetchall()
        except Exception as e:
            print(e)
            print("no tables can get")

    def close(self):
        if self.__conn is not None:
            self.__conn.commit()
            self.__conn.close()
        else:
            print("on effect connect")

    def commit(self):
        if self.__conn is not None:
            self.__conn.commit()
        else:
            print("on effect connect")

if __name__ == "__main__":
    sq = SqliteOperation("/home/envs/.conda/envs/clw/smartemail/email_training_data.db")
