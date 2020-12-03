import sys
import os
abs_path = os.path.abspath("..")
sys.path.append(abs_path)

from summarize.KeywordExtract import KeywordExtract


if __name__ == '__main__':
    test_text = open("test_text.txt", "r", encoding="utf-8").read()
    # print(test_text)
    keyword_extractor = KeywordExtract()
    keywords = keyword_extractor.get_keywords(text=test_text, topK=15, seg_tool="pku", window=2, use_stopwords=True, use_postags_filter=True)
    for k, v in keywords:
        print(k)

    import time
    s = time.time()
    for i in range(10):
        keyword_extractor.get_keywords(text=test_text, topK=15, seg_tool="pku")
    e = time.time()
    print(f"计算耗时{e-s}s")
    
    