# coding: utf-8

import jieba
from whoosh.analysis import Tokenizer,Token
class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value
        t = Token(positions, chars, removestops=removestops, mode=mode,
            **kwargs)
        #seglist=jieba.cut(value,cut_all=False)                       #使用结巴分词库进行分词
        seglist = jieba.cut_for_search(value)                         #使用结巴分词库搜索引擎模式进行分词
        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos=start_pos+value.find(w)
            if chars:
                t.startchar=start_char+value.find(w)
                t.endchar=start_char+value.find(w)+len(w)
            yield t                                               #通过生成器返回每个分词的结果token

def ChineseAnalyzer():
    return ChineseTokenizer()




from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer


#重点在这里，将原先的RegexAnalyzer(ur”([\u4e00-\u9fa5])|(\w+(\.?\w+)*)”),改成这句，用中文分词器代替原先的正则表达式解释器。
analyzer=ChineseAnalyzer()

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