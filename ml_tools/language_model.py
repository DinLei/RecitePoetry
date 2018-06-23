#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-21 下午11:43
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


class LanguageModel:
    """
    语言模型基类
    """
    def __init__(self):
        self.__unigram = None
        self.__prob_model = None

    def train(self, data):
        pass

    def predict(self, sent):
        pass

    def get_vocabulary(self):
        if isinstance(self.__unigram, dict):
            return set(self.__unigram.keys())
        else:
            return set()


class TrigramModel(LanguageModel):
    """
    三元语法模型，使用二元、一元插值、折减平滑处理
    *: 首部填充值，代表开始
    $: 尾部填充值，代表结束
    """
    def __init__(self):
        self.__bigram = None
        self.__trigram = None
        # super(TrigramModel, self).__init__()
        LanguageModel.__init__(self)

    def __init_single_model(self):
        if not self.__unigram:
            self.__unigram = {"total_num": 0}
        if not self.__bigram:
            self.__bigram = {"total_num": 0}
        if not self.__trigram:
            self.__trigram = {"total_num": 0}

    def train(self, data):
        """
        加载训练数据，构造模型
        :param data: 句子的集合
        :return: void
        """
        self.__init_single_model()
        for sent in data:
            arr = list(sent)
            arr.insert(0, "*")
            arr.insert(0, "*")
            arr.append("$")
    pass
