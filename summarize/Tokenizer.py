# -*- coding=utf-8 -*-

# import util
# from Segmentation import cws
import summarize.util as util
from summarize.Segmentation import cws
import codecs
import os
import re


def get_default_stopwords_file():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords_private.txt')


class WordSegmentation(object):
    """分词"""

    def __init__(self, stopwords_file: str = None, allow_speech_tags: list = util.allow_speech_tags):
        """
        Keyword arguments:

        :param stopwords_file    -- 保存停止词的文件路径，utf8编码，每行一个停止词。若不是str类型，则使用默认的停止词
        :param allow_speech_tags  -- 词性列表，用于过滤
        """
        self.default_speech_tag_filter = allow_speech_tags
        self.stop_words = set()
        if type(stopwords_file) is str:
            self.stop_words_file = stopwords_file
        else:
            self.stop_words_file = get_default_stopwords_file()
        for word in codecs.open(self.stop_words_file, mode='r', encoding='utf-8', errors='ignore'):
            self.stop_words.add(word.strip())

    # def thu_seg(self, text: str):
    #     """清华分词工具"""
    #     import thulac
    #     thu = thulac.thulac(T2S=False, seg_only=False)
    #     thulac_result = [item for item in thu.cut(text) if len(item[0].strip()) > 0]
    #     return thulac_result
    #
    # def jieba_seg(self, text: str):
    #     return 0

    def segment(self,
                text: str,
                use_stopwords: bool = True,
                use_postags_filter: bool = False,
                seg_tool: str = "jieba"):
        """
        中文文本分词

        :param text: str, 待分词文本
        :param use_stopwords: bool, 是否启用停用词
        :param use_postags_filter: bool, 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。
        :param seg_tool: str, 选择使用的分词器，["thu", "pku", "jieba"], 默认jieba分词器
        """

        lac_result = cws(text=text, tool=seg_tool)

        if use_postags_filter:
            lac_result = [w for w in lac_result if w[1] in self.default_speech_tag_filter]
        else:
            lac_result = [w for w in lac_result]

        # word_list = [item[0].strip() for item in lac_result if item[1] != "w" and len(item[0].strip()) > 0]
        word_list = [item[0].strip() for item in lac_result if len(item[0].strip()) > 0]

        if use_stopwords:
            word_list = [word for word in word_list if word not in self.stop_words]

        return word_list

    def segment_by_sentences(self,
                             sentences: list,
                             use_stopwords: bool = True,
                             use_postags_filter: bool = True,
                             seg_tool: str = "jieba"):
        """
        将sentences列表中的每个句子转换为由词语构成的列表

        :param sentences: list, 句子列表
        :param use_stopwords: bool, 是否启用停用词
        :param use_postags_filter: bool, 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。
        :param seg_tool: str, 选择使用的分词器，["thu", "pku", "jieba"], 默认jieba分词器

        """
        result = []
        for sentence in sentences:
            word_list = self.segment(text=sentence,
                                     use_stopwords=use_stopwords,
                                     use_postags_filter=use_postags_filter,
                                     seg_tool=seg_tool)
            result.append(word_list)
        return result


class SentenceSegmentation(object):
    """分句"""

    def __init__(self, delimiters=util.sentence_delimiters):
        """
        :param delimiters: 句子分隔符，用来拆分句子,正则格式
        """
        self.delimiters = delimiters

    def segment(self, text: str):
        chunks = re.split(self.delimiters, text)  # 设定切分符号
        subsentences = ["".join(item) for item in zip(chunks[0::2], chunks[1::2])]  # 合并字块和其后的标点符号
        subsentences = [subsent.strip() for subsent in subsentences if len(subsent.strip()) > 0]  # 去除可能出现的空句
        result = subsentences
        result = [s.strip() for s in result if len(s.strip()) > 0]
        return result


class Tokenizer(object):

    def __init__(self,
                 stopwords_file: str = None,
                 allow_speech_tags: list = util.allow_speech_tags,
                 delimiters=util.sentence_delimiters):
        """
        :param stopwords_file: 停用词文件路径
        :param allow_speech_tags: 词性过滤列表
        :param delimiters: 句子分隔符，用来拆分句子，正则格式，如"(\?|!|;|？|！|。|；|……|…|\n)"
        """
        self.ws = WordSegmentation(stopwords_file=stopwords_file,
                                   allow_speech_tags=allow_speech_tags)
        self.ss = SentenceSegmentation(delimiters=delimiters)

    def segment(self,
                text: str,
                use_stopwords: bool = True,
                use_postags_filter: bool = True,
                seg_tool: str = "jieba"):
        """
        中文文本分句分词

        :param text: str, 待分析文本
        :param use_stopwords: bool, 是否启用停用词
        :param use_postags_filter: bool, 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。
        :param seg_tool: str, 选择使用的分词器，["thu", "pku", "jieba"], 默认jieba分词器
        """
        sentences = self.ss.segment(text)
        words = self.ws.segment_by_sentences(sentences=sentences,
                                             use_stopwords=use_stopwords,
                                             use_postags_filter=use_postags_filter,
                                             seg_tool=seg_tool)
        return dict(sentences=sentences, words=words)

    def segment_for_keyword(self,
                            text: str,
                            use_stopwords: bool = True,
                            use_postags_filter: bool = True,
                            seg_tool: str = "jieba"):
        """
        中文文本分词，取消分句，提取关键词专用，为了加速

        :param text: str, 待分析文本
        :param use_stopwords: bool, 是否启用停用词
        :param use_postags_filter: bool, 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。
        :param seg_tool: str, 选择使用的分词器，["thu", "pku", "jieba"], 默认jieba分词器
        """
        sentences = [text]  # 不再进行分句
        words = self.ws.segment_by_sentences(sentences=sentences,
                                             use_stopwords=use_stopwords,
                                             use_postags_filter=use_postags_filter,
                                             seg_tool=seg_tool)
        return dict(sentences=sentences, words=words)


if __name__ == '__main__':
    pass
