import csv
import argparse
import itertools
from janome.tokenizer import Tokenizer

from wordnet import Wordnet

parser = argparse.ArgumentParser(description="1行ずつファイルを読み取って類義語のtextをたくさん作る")
parser.add_argument('--textpath', help='テキストのファイルパス.デフォルトは./text.csv', default='./text.csv')
parser.add_argument('--dbpath', help='dbデータのpath.デフォルトは./wnjpn.db', default='./wnjpn.db')

args = parser.parse_args()

if __name__ == '__main__':
    text_path = args.textpath
    db_path = args.dbpath
    wordnet = Wordnet()
    t = Tokenizer()
    with open(text_path) as f:
        reader = csv.reader(f)
        # TODO: lambdaで書き換えたい
        for row in reader:
            text = row[0]
            print(text)
            synonyms_by_word = []
            for token in t.tokenize(text):
                token_word = token.surface
                words = [token_word]
                synonyms_list = wordnet.get_synonym(token_word)
                for synonyms in synonyms_list.values():
                    words.extend(synonyms)
                synonyms_by_word.append(list(set(words)))
            print(synonyms_by_word)
            # 直積なので膨大な計算量が発生するので注意
            synonyms_texts = list(itertools.product(*synonyms_by_word))
            print(synonyms_texts)

            # 1行だけ試したい場合は下記breakをつけておく。全行試すならbreakをコメントアウト
            break

