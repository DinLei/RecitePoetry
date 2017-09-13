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
        self._dbname = dbname
        self._conn = None
        self._cur = None
        try:
            self._conn = sqlite3.connect(self._dbname)
            self._cur = self._conn.cursor()
            print("Opened database {} successfully".format(self._dbname))
        except Exception as e:
            print(e)
            print("can not get {}, please check your environment.".format(self._dbname))

    @property
    def db_conn(self):
        return self._conn

    @db_conn.setter
    def db_conn(self, sqlite_db):
        self._conn = SqliteOperation(sqlite_db)

    def get_data_by_sql(self, sql, to_list=False):
        tmp = self._conn.execute(sql)
        data = tmp.fetchall()
        if to_list:
            return [x for x in data]
        return data

    def get_data_by_field(self, fields, tbname):
        if isinstance(fields,list):
            fields_names = ','.join(fields)
        elif isinstance(fields,str):
            fields_names = fields
        tmp = self._conn.execute("select "+fields_names+" from "+tbname)
        data = tmp.fetchall()
        if len(data[0]) == 1:
            return [x[0] for x in data]
        return data

    def count_table_record(self, tbname):
        try:
            count = self._cur.execute("select count(1) from "+tbname)
            return count.fetchall()[0][0]
        except Exception as e:
            print(e)
            print("there is something wrong with table: "+tbname)

    def insert_one(self, tbname, data=None):
        sql = "insert into "+tbname+" values ("
        try:
            if isinstance(data, list) or isinstance(data, tuple):
                sql += "?," * (len(data) - 1) + "?)"
            else:
                sql += "?)"
                data = (data,)
            self._cur.execute(sql, data)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
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
                self._cur.execute(sql, row)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print("insert failed")
            print(e.with_traceback(tbname))

    def update_one(self, tbname, field, data):
        try:
            self._conn.execute("update "+tbname+" set " +
                                field[0]+" = ? where "+field[1]+" = ?", data)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print(e.with_traceback(tbname))
            print("update failed")

    def update_batch(self, tbname, field, data):
        try:
            for row in data:
                self._conn.execute("UPDATE "+tbname+" set " + field[0]+" = ? where "+field[1]+"=?", row)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print(e.with_traceback(tbname))
            print("update failed")

    def delete_all(self, tbname):
        try:
            self._conn.execute("delete from "+tbname)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print(e.with_traceback(tbname))
            print("delete fail")

    def delete_all_by_condition(self, tbname, field, condition):
        try:
            self._conn.execute("delete from "+tbname+" where "+field+" = ?", condition)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print(e.with_traceback(tbname))
            print("delete fail")

    @property
    def dbname(self):
        return self._dbname

    def show_tables(self):
        try:
            tables = self.db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return tables.fetchall()
        except Exception as e:
            print(e)
            print("no tables can get")

    def close(self):
        if self._conn is not None:
            self._conn.commit()
            self._conn.close()
        else:
            print("on effect connect")

    def commit(self):
        if self._conn is not None:
            self._conn.commit()
        else:
            print("on effect connect")

