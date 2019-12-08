import csv
import argparse

parser = argparse.ArgumentParser(description="1行ずつファイルを読み取って類義語のtextをたくさん作る")
parser.add_argument('textpath', help='テキストのファイルパス.デフォルトは./text.txt', default='./text.txt')
parser.add_argument('dbpath', help='dbデータのpath.デフォルトは./wnjpn.db', default='./wnjpn.db')

args = parser.parse_args()

if __name__ == '__main__':
    text_path = args.textpath
    db_path = args.dbpath
    print(text_path)
    print(db_path)
    with open(args.textpath) as f:
        print(f.read())

