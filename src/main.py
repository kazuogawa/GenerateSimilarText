import csv
import argparse
import itertools
import datetime
from functools import reduce
from janome.tokenizer import Tokenizer

from wordnet import Wordnet

parser = argparse.ArgumentParser(description="1行ずつファイルを読み取って類義語のtextをたくさん作る")
parser.add_argument('--textpath', help='テキストのファイルパス.デフォルトは./text.csv', default='./text.csv')
parser.add_argument('--dbpath', help='dbデータのpath.デフォルトは./wnjpn.db', default='./wnjpn.db')

args = parser.parse_args()

if __name__ == '__main__':
    starttime = datetime.datetime.today()
    print('start time: ' + str(starttime))
    text_path = args.textpath
    db_path = args.dbpath
    wordnet = Wordnet()
    t = Tokenizer()
    writefile = open('output.txt', 'w')
    combination_num_sum = 0
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
            #synonyms_texts = list(itertools.product(*synonyms_by_word))
            #print('synonyms_texts')
            #print(synonyms_texts)
            #combination_num = len(synonyms_texts)
            len_list = list(map(lambda words: len(words), synonyms_by_word))
            combination_num = reduce(lambda len1, len2: len1 * len2, len_list)
            print('combination num: ' + str(combination_num))
            combination_num_sum += combination_num
            #concat_texts = list(map(lambda words: reduce(lambda word1, word2: word1 + word2, words), synonyms_texts))
            #for text in concat_texts:
            #    writefile.write(text + '\n')
            #print(concat_texts)
            # 1行だけ試したい場合は下記breakをつけておく。全行試すならbreakをコメントアウト
            #break
    writefile.close()
    print('combination_num_sum: ' + str(combination_num_sum))
    endtime = datetime.datetime.today()
    print('endtime: ' + str(endtime))
    print('execute time: ' + str(endtime - starttime))

