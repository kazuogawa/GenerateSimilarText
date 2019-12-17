import csv
import argparse
import random
import itertools
import datetime
from janome.tokenizer import Tokenizer
from functools import reduce

from wordnet import Wordnet

parser = argparse.ArgumentParser(description="1行ずつファイルを読み取って類義語のtextをたくさん作る")
parser.add_argument('--inputpath', help='テキストのinputファイルパス.デフォルトは./input.csv', default='./input.csv')
parser.add_argument('--outputpath', help='テキストのoutputファイルパス.デフォルトは./今日の日付.csv', default='./{}.csv'.format(str(datetime.datetime.today().strftime("%Y%m%d") + '_poems')))
parser.add_argument('--dbpath', help='dbデータのpath.デフォルトは./wnjpn.db', default='./wnjpn.db')
parser.add_argument('--multi', help='倍数デフォルトは10', default=10)

args = parser.parse_args()

if __name__ == '__main__':
    input_path = args.inputpath
    db_path = args.dbpath
    multiple = args.multi
    output_path = args.outputpath
    wordnet = Wordnet()
    t = Tokenizer()
    create_texts = []
    with open(input_path) as f:
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
            synonyms_texts = []
            for i in range(multiple):
                synonyms_texts.append(reduce(lambda choice_synonym1, choice_synonym2: choice_synonym1 + choice_synonym2, list(map(lambda words: reduce(lambda word1, word2: word1 + word2, random.choice(words)), synonyms_by_word))))
            # 直積なので膨大な計算量が発生するので注意
            #synonyms_texts = list(itertools.product(*synonyms_by_word))
            print(synonyms_texts)
            # 重複削除
            create_texts.extend(list(set(synonyms_texts)))
            # 1行だけ試したい場合は下記breakをつけておく。全行試すならbreakをコメントアウト
            #break
    random.shuffle(create_texts)
    with open(output_path, mode='w') as f:
        output_text = reduce(lambda text1, text2: text1 + '\n' + text2, create_texts)
        f.write(output_text)
