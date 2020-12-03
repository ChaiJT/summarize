# -*- coding=utf-8 -*-

# import util
# from Tokenizer import Tokenizer
import summarize.util as util
from summarize.Tokenizer import Tokenizer


class SummaryExtract(object):
    """Textrank 提取摘要"""

    def __init__(self,
                 stopwords_file = None,
                 allow_speech_tags = util.allow_speech_tags,
                 delimiters = util.sentence_delimiters):
        """
        :param stopwords_file: 停用词文件路径
        :param allow_speech_tags: 词性过滤列表
        :param delimiters: 句子分隔符，用来拆分句子
        """
        self.seg = Tokenizer(stopwords_file=stopwords_file,
                             allow_speech_tags=allow_speech_tags,
                             delimiters=delimiters)

    def get_summary(self,
                    text: str,
                    topK: int = 3,
                    with_weight: bool = False,
                    seg_tool: str = "jieba"):
        """
        抽取摘要

        :param text: str, 待分析文本，utf-8编码
        :param topK: int, 提取关键句子的数量，默认为10
        :param with_weight: bool, 是否返回句子权重
        :param seg_tool: str, 选择使用的分词器，["thu", "pku", "jieba"], 默认jieba分词器

        """
        dic_data = self.seg.segment(text=text,
                                    use_stopwords=True,
                                    use_postags_filter=True,
                                    seg_tool=seg_tool)
        sentences = dic_data["sentences"]
        words = dic_data["words"]
        key_sentencees = util.sorted_sentences_by_textrank(sentences, words)

        result = []
        count = 0
        for item in key_sentencees:
            if count >= len(key_sentencees):
                break
            if count >= topK:
                break
            if with_weight:
                result.append((item.get("sentence"), item.get("weight")))   # list of tuple
            else:
                result.append(item.get("sentence"))     # list of str
            count += 1
        return result


if __name__ == '__main__':
    test_text = open("test_text.txt", "r", encoding="utf-8").read()
    print(test_text)
    summary_extract = SummaryExtract()
    summary = summary_extract.get_summary(text=test_text, topK=3, seg_tool="pku")
    print(summary)

    import time

    s = time.time()
    for i in range(10):
        summary_extract.get_summary(text=test_text, topK=3, seg_tool="pku")
    e = time.time()
    print(f"提取10篇文章摘要耗时{e-s}s")
