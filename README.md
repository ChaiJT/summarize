# summarize

一个提取中文关键词和摘要的Python程序。 

A NLP tool for extract keywords and summary from text.


# 使用说明

## 提取关键词


	from summarize.KeywordExtract import KeywordExtract
	test_text = open("test_text.txt", "r", encoding="utf-8").read()	# 读取测试文本
	keyword_extractor = KeywordExtract()
	# 使用TextRank方法
	keywords = keyword_extractor.get_keywords(text=test_text, topK=15, seg_tool="pku", window=2, use_stopwords=True, use_postags_filter=True)
	print(keywords)
	# 使用TF-IDF方法
	keywords2 = keyword_extractor.get_keywords_by_tfidf(text=test_text, topK=15, seg_tool="pku")
	print(keywords2)
	#	结果形如：[(word1,weight1), (word2, weight2)...]

## 提取摘要

	from summarize.SummaryExtract import SummaryExtract
	test_text = open("test_text.txt", "r", encoding="utf-8").read()
	summary_extract = SummaryExtract()
    summary = summary_extract.get_summary(text=test_text, topK=3, seg_tool="pku")
    print(summary)
	#	结果形如：[sentence1, sentence2, sentence3]

# Note
* 程序中使用了[北大的pku分词器](https://github.com/lancopku/pkuseg-python)，需要下载模型包。若不想使用，可选择使用[jieba分词器](https://github.com/fxsjy/jieba),只需修改参数seg_tool为jieba即可。
* 仅为个人学习使用