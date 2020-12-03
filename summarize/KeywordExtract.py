# -*- coding=utf-8 -*-

# import util
# from Tokenizer import Tokenizer
import summarize.util as util
from summarize.Tokenizer import Tokenizer

class KeywordExtract(object):
    """Textrank提取关键词"""

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

    def get_keywords(self,
                     text: str,
                     topK: int = 10,
                     word_min_len: int = 2,
                     window: int = 2,
                     use_stopwords: bool = True,
                     use_postags_filter: bool = True,
                     seg_tool: str = "jieba"):
        """
        计算关键词

        :param text: str, 待分析文本，utf-8编码
        :param topK: int, 提取关键词的数量，默认为10
        :param word_min_len: int, 提取关键词的最小长度，默认为2
        :param window: int, textrank构建DAG图选取的窗口大小，默认为2
        :param use_stopwords: bool, 是否启用停用词，默认为True
        :param use_postags_filter: bool, 是否启用词性过滤，默认为False
        :param seg_tool: str, 选择使用的分词器，["thu", "pku", "jieba"], 默认jieba分词器

        """
        dic_data = self.seg.segment_for_keyword(text=text,
                                                use_stopwords=use_stopwords,
                                                use_postags_filter=use_postags_filter,
                                                seg_tool=seg_tool)
        vertexs = dic_data["words"]
        sentences = dic_data["sentences"]
        keywords = util.sort_words_by_textrank(vertexs=vertexs,
                                               window=window)
        result = []
        count = 0
        for item in keywords:
            if count >= len(keywords):
                break
            if count >= topK:
                break
            if len(item.get("word")) >= word_min_len:
                result.append((item.get("word"), item.get("weight")))
                count += 1
        return result

    def get_keyphrase(self,
                      text: str,
                      topK: int = 10,
                      word_min_len: int = 2,
                      window: int = 2,
                      use_stopwords: bool = True,
                      use_postags_filter: bool = True,
                      seg_tool: str = "jieba"):
        """提取关键短语，还有一定问题"""
        data = self.seg.segment(text=text,
                                use_stopwords=False,
                                use_postags_filter=False,
                                seg_tool=seg_tool)
        words = data["words"]
        # print(data["sentences"])
        # print(words)
        keywords_list = [item[0] for item in self.get_keywords(text=text, topK=topK*2, seg_tool=seg_tool)]
        keywords_topK = keywords_list[:topK]
        temp_set = set()
        keyphrases = set()
        for sentence_word_list in words:
            pharse = []
            for i in range(len(sentence_word_list)-1):
                word1 = sentence_word_list[i]
                word2 = sentence_word_list[i+1]
                if word1 in keywords_topK and word2 in keywords_topK:
                    if i < len(sentence_word_list)-3:
                        word3 = sentence_word_list[i+2]
                    else:
                        word3 = ""
                    if word3 in keywords_topK:
                        keyphrases.add(word1+word2+word3)
                        # keywords_list.remove(word3)
                        temp_set.add(word3)
                    else:
                        keyphrases.add(word1+word2)
                    # keywords_list.remove(word1)
                    # keywords_list.remove(word2)
                    temp_set.add(word1)
                    temp_set.add(word2)
        phrase_num = len(keyphrases)

        if phrase_num >= topK:
            return list(keyphrases)[:topK]
        else:
            for w in temp_set:
                keywords_list.remove(w)
            result = list(keyphrases)
            result.extend(keywords_list[:topK-phrase_num])
            return result


if __name__ == '__main__':
    test_text = open("test_text.txt", "r", encoding="utf-8").read()
    # print(test_text)
    keyword_extractor = KeywordExtract()
    keywords = keyword_extractor.get_keywords(text=test_text, topK=15, seg_tool="pku", window=2, use_stopwords=True, use_postags_filter=True)
    for k, v in keywords:
        print(k)


    import time
    s_t = time.time()
    for i in range(10):
        keywords2 = keyword_extractor.get_keywords(text=test_text,
                                                   topK=10,
                                                   seg_tool="pku",
                                                   window=2,
                                                   use_stopwords=True,
                                                   use_postags_filter=True)
    e_t = time.time()
    print(f"\n10篇文章提取关键词耗时{e_t-s_t}s。")


    # keyphrases = keyword_extractor.get_keyphrase(text=test_text, topK=10, seg_tool="pku")
    # print(keyphrases)

    # import thulac
    # import jieba
    # thu = thulac.thulac(T2S=False, seg_only=False)
    # thu.cut(test_text)
    # jieba.cut(test_text)
    # s1 = time.time()
    # for i in range(10):
    #     thu.cut(test_text)
    # e1 = time.time()
    # for j in range(10):
    #     jieba.cut(test_text)
    # e2 = time.time()
    # print(f"thu {e1-s1}s, jieba {e2-e1}s")



