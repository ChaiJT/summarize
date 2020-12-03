import sys
import os
abs_path = os.path.abspath("..")
sys.path.append(abs_path)

from summarize.SummaryExtract import SummaryExtract


if __name__ == '__main__':
    test_text = open("test_text.txt", "r", encoding="utf-8").read()
    # print(test_text)
    summary_extract = SummaryExtract()
    summary = summary_extract.get_summary(text=test_text, topK=3, seg_tool="pku")
    print("".join(summary))

    import time

    s = time.time()
    for i in range(10):
        summary_extract.get_summary(text=test_text, topK=3, seg_tool="pku")
    e = time.time()
    print(f"提取10篇文章摘要耗时{e-s}s")