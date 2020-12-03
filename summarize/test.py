
# from textrank4zh import TextRank4Keyword
#
# test_text = open("test_text.txt", "r", encoding="utf-8").read()
#
#
# tr4w = TextRank4Keyword()
# tr4w.analyze(text=test_text,lower=True, window=2, pagerank_config={'alpha':0.85})
#
# for item in tr4w.get_keywords(10, word_min_len=1):
#     print(item.word, item.weight)
#
# import time
#
# s_t = time.time()
# for i in range(10):
#     tr4w.get_keywords(10, word_min_len=1)
# e_t = time.time()
# print(f"\n10篇文章提取关键词耗时{e_t-s_t}s。")

