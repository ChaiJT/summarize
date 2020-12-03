# -*- coding=utf-8 -*-


import pkuseg
import jieba.posseg

# import thulac
# thu = thulac.thulac(T2S=False, seg_only=False)

pku = pkuseg.pkuseg(model_name="news", user_dict="default", postag=True)


def cws(text: str, tool: str="jieba"):
    """
    中文分词及词性标注

    :param text: str, 待分词文本
    :param tool: "thu" — 清华分词器；
                 "pku" — 北大分词器；
                 "jieba" — 结巴分词器；
    """
    func_dic = {"pku": pku_seg,
                "jieba": jieba_seg}
    # print("*********调用了一次分词*********")
    return func_dic.get(tool, "jieba")(text)

'''
def thu_seg(text: str):     # 测试一文437ms
    """清华分词工具"""
    thulac_result = [item for item in thu.cut(text) if len(item[0].strip()) > 0]
    # print("****************\n使用清华分词器\n****************")
    return thulac_result
'''

def jieba_seg(text: str):   # 测试一文5ms
    """结巴分词工具"""
    words = jieba.posseg.cut(text)
    jieba_result = [(word, nature) for word, nature in words if len(word.strip()) > 0]
    # print("****************\n使用结巴分词器\n****************")
    return jieba_result


def pku_seg(text: str):     # 测试一文13.5ms
    """北大分词工具"""
    pku_result = pku.cut(text)
    # print(pku_result)
    # print("****************\n使用北大分词器\n****************")
    return pku_result


def ltp(text: str):     # 测试一文 gpu18ms， cpu56ms
    """LTP分词工具"""
    return 0


if __name__ == '__main__':
    test_text = open("test_text.txt", "r", encoding="utf-8").read()
    print(jieba_seg(test_text))

    import time
    s1 =time.time()
    for i in range(1):
        jieba_seg(test_text)
    e1 = time.time()
    print(f"分析耗时{e1-s1}s")

