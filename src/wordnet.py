# -*- coding: utf-8 -*-
# Wordnet via Python3
#
# ref:
#   WordList_JP: http://compling.hss.ntu.edu.sg/wnja/
#   python3: http://sucrose.hatenablog.com/entry/20120305/p1
import sys, sqlite3
from collections import namedtuple
from pprint import pprint


class Wordnet():

    def __init__(self):
        self.conn = sqlite3.connect("./wnjpn.db")
        self.Word = namedtuple('Word', 'wordid lang lemma pron pos')
        self.Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')
        self.Synset = namedtuple('Synset', 'synset pos name src')

    def _get_words(self, lemma):
        cur = self.conn.execute("select * from word where lemma=?", (lemma,))
        return [self.Word(*row) for row in cur]

    def _get_senses(self, word):
        cur = self.conn.execute("select * from sense where wordid=?", (word.wordid,))
        return [self.Sense(*row) for row in cur]

    def _get_synset(self, syn_set):
        cur = self.conn.execute("select * from synset where synset=?", (syn_set,))
        return self.Synset(*cur.fetchone())

    def _get_words_from_synset(self, synset, lang):
        cur = self.conn.execute(
            "select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;",
            (synset, lang))
        return [self.Word(*row) for row in cur]

    def _get_words_from_senses(self, sense, lang="jpn"):
        synonym = {}
        for s in sense:
            lemmas = []
            syns = self._get_words_from_synset(s.synset, lang)
            for sy in syns:
                lemmas.append(sy.lemma)
            synonym[self._get_synset(s.synset).name] = lemmas
        return synonym

    def get_synonym(self, word):
        synonym = {}
        words = self._get_words(word)
        if words:
            for w in words:
                sense = self._get_senses(w)
                s = self._get_words_from_senses(sense)
                synonym = dict(list(synonym.items()) + list(s.items()))
        return synonym


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        wordnet = Wordnet()
        synonym = wordnet.get_synonym(sys.argv[1])
        pprint(synonym)
    else:
        print("You need at least 1 argument as a word like below.\nExample:\n  $ python3 wordnet_jp 楽しい")
