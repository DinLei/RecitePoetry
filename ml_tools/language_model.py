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

    def train(self, development_data):
        pass

    def load_corpus(self, corpus):
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
    三元语法模型，使用二元、一元插值平滑处理
    *: 首部填充值，代表开始
    $: 尾部填充值，代表结束
    """
    def __init__(self):
        self.__bigram = None
        self.__trigram = None
        LanguageModel.__init__(self)
        # super(TrigramModel, self).__init__()

    def __clean_up_single_model(self):
        if not self.__unigram:
            self.__unigram = {"total_num": 0, "grams": dict()}
        else:
            self.__unigram["total_num"] += sum(self.__unigram["grams"].values())
        if not self.__bigram:
            self.__bigram = {"total_num": 0, "grams": dict()}
        else:
            self.__bigram["total_num"] += sum(self.__bigram["grams"].values())
        if not self.__trigram:
            self.__trigram = {"total_num": 0, "grams": dict()}
        else:
            self.__trigram["total_num"] += sum(self.__trigram["grams"].values())

    def load_corpus(self, corpus):
        """
        加载训练数据，构造模型
        :param corpus: 句子的集合，构造ngram的语料
        :return: void
        """
        self.__clean_up_single_model()
        for sent in corpus:
            arr = list(sent)
            arr.insert(0, "*")
            arr.insert(0, "*")
            arr.append("$")
            for ind in range(len(arr)):
                if ind < len(arr) - 2:
                    token3 = "".join(arr[ind: ind+3])
                    if token3 not in self.__trigram["grams"]:
                        self.__trigram["grams"][token3] = 0
                    self.__trigram["grams"][token3] += 1
                if 1 < ind < len(arr) - 1:
                    token1 = arr[ind]
                    if token1 not in self.__unigram["grams"]:
                        self.__unigram["grams"][token1] = 0
                    self.__unigram["grams"][token1] += 1
                if 0 < ind < len(arr):
                    token2 = "".join(arr[ind: ind + 2])
                    if token2 not in self.__bigram["grams"]:
                        self.__bigram["grams"][token2] = 0
                    self.__bigram["grams"][token2] += 1
        self.__clean_up_single_model()
    pass
