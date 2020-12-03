# -*- coding=utf-8 -*-

import numpy as np
import networkx as nx
import math
import sys
import os


# sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
sentence_delimiters = "(\?|!|;|？|！|。|；|……|…|\n)"
# 清华分词工具词性 http://thulac.thunlp.org/demo
thu_allow_speech_tags = ["n", "np", "ns", "ni", "nz", "v", "t", "i", "j"]
# 北大分词工具词性 https://github.com/lancopku/pkuseg-python/blob/master/tags.txt
pku_allow_speech_tags = ["n", "nr", "ns", "nt", "nx", "nz", "vn", "vd", "vx", "t", "v", "i", "l", "j"]    # "a", "z", "an"
# 结巴分词工具词性 https://github.com/fxsjy/jieba
jieba_allow_speech_tags = ["n", "nr", "ns", "nt", "nw", "nz", "vn", "vd", "t"]   # "a", "an",

default_allow_speech_tags = []
default_allow_speech_tags.extend(thu_allow_speech_tags)
default_allow_speech_tags.extend(pku_allow_speech_tags)
default_allow_speech_tags.extend(jieba_allow_speech_tags)
allow_speech_tags = set(default_allow_speech_tags)


def combine(word_list: list, window: int=2):
    """
    构造在window下的单词组合，用来构造DAG图中单词的边。

    :param word_list: list of str, 一句话中单词组成的列表
    :param window: int, 用来构造单词之间边时的窗口大小
    """
    if window < 2:
        window = 2
    for i in range(1, window):
        if i >= len(word_list):
            break
        word_list_shift = word_list[i:]
        word_pairs = zip(word_list, word_list_shift)
        for word_pair in word_pairs:
            yield word_pair


def sort_words_by_textrank(vertexs: list, window: int=2):
    """
    使用TextRank算法计算单词的关键程度，并按从大到小排序

    :param vertexs: 二维列表，子列表代表句子，子列表元素代表句子中的单词，这些单词用来构建DAG图中的节点
    :param window: int，一个句子中window窗内的单词，认为两两之间存在边
    :return: list of dict, 返回关键词及权重的排序列表
    """
    sorted_words = []
    word2index = {}
    index2word = {}
    words_num = 0
    vertexs = vertexs   # vertexs: 二维列表，子列表代表句子，子列表元素代表句子中的单词，这些单词用来构建DAG图中的节点
    edges = vertexs     # edges: 二维列表，子列表代表句子，子列表元素代表句子中的单词，这些单词位置关系构建DAG图中的边

    # 构建词和索引的映射
    for word_list in vertexs:
        for word in word_list:
            if word not in word2index:
                word2index[word] = words_num
                index2word[words_num] = word
                words_num += 1

    # 构建词语的DAG图
    graph = np.zeros((words_num, words_num))
    for word_list in edges:
        for word1, word2 in combine(word_list, window):
            index1 = word2index[word1]
            index2 = word2index[word2]
            graph[index1][index2] += 1.0
            graph[index2][index1] += 1.0
    nx_graph = nx.from_numpy_matrix(graph)

    # pagerank算法计算词语权重（关键程度）
    word_scores = nx.pagerank(G=nx_graph, alpha=0.85, max_iter=100, tol=1.0e-6)

    # 按词语权重从大到小排序
    sorted_word_scores = sorted(word_scores.items(), key=lambda item: item[1], reverse=True)
    for index, score in sorted_word_scores:
        item = dict(word=index2word[index], weight=score)
        sorted_words.append(item)

    return sorted_words


def get_similarity(word_list1: str, word_list2: str):
    """
    用于计算两个句子相似度的函数，依据是共现词

    :param word_list1: list, 单词组成的列表，代表一个句子
    :param word_list2: list, 单词组成的列表，代表一个句子
    :return: float, 相似度值
    """
    words = list(set(word_list1 + word_list2))
    vector1 = [float(word_list1.count(word)) for word in words]
    vector2 = [float(word_list2.count(word)) for word in words]

    vector3 = [vector1[x] * vector2[x] for x in range(len(vector1))]
    vector4 = [1 for num in vector3 if num > 0.]    # 有待考虑
    # vector4 = [num for num in vector3 if num > 0.]
    co_occur_num = sum(vector4)

    if abs(co_occur_num) <= 1e-12:
        return 0.

    denominator = math.log(float(len(word_list1))) + math.log(float(len(word_list2)))  # 分母

    if abs(denominator) < 1e-12:
        return 0.

    return co_occur_num / denominator


def sorted_sentences_by_textrank(sentences: list, words: list):
    """
    使用TextRank算法计算句子的关键程度，并按从大到小排序

    :param sentences: list，元素是句子
    :param words: list, 二维列表，子列表和sentences中的句子对应，子列表元素是句子中的词语
    """
    sorted_sentences = []
    sentences_num = len(sentences)

    # 构建句子的有向无环图
    graph = np.zeros((sentences_num, sentences_num))
    for x in range(sentences_num):
        for y in range(x, sentences_num):   # ?这会出现x和x的相似度，自环
            similarity = get_similarity(words[x], words[y])
            graph[x][y] = similarity
            graph[y][x] = similarity
    nx_graph = nx.from_numpy_matrix(graph)

    # pagerank算法计算句子权重（关键程度）
    sentence_scores = nx.pagerank(G=nx_graph, alpha=0.85, max_iter=100, tol=1.0e-6)

    # 按句子权重从大到小排序
    sorted_sentence_scores = sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)
    for index, score in sorted_sentence_scores:
        item = dict(sentence=sentences[index], weight=score)
        sorted_sentences.append(item)

    return sorted_sentences


if __name__ == '__main__':
    pass
