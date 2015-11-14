# coding: utf-8

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer
analyzer = RegexAnalyzer(ur"([\u4e00-\u9fa5])|(\w+(\.?\w+)*)")  
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
ix = create_in("indexdir", schema)
writer = ix.writer()
writer.add_document(title=u"1st documment", path=u"/supposeToBePath/a",
	content=u"This is the first document we've added.")
writer.add_document(title=u"2nd documment", path=u"/supposeToBePath/b",
	content=u"The second one is even more interesting.")
writer.add_document(title=u"3rd documment", path=u"/supposeToBePath/c",
	content=u"我想写点中文。比方说：有没有什么更有意思的事情会发生？")
writer.commit()

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema).parse(u"发生")
	results = searcher.search(query)
	print results
	print results[0]
