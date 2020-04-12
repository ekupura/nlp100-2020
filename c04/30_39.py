import fire
from pprint import pprint
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import MeCab
matplotlib.rcParams['font.family'] = ['IPAexGothic']

def morph_analysis(sentence):
    mecab = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    mecab.parse('')  # 文字列がGCされるのを防ぐ
    node = mecab.parseToNode(sentence)
    words, poses = [], []
    while node:
        words.append(node.surface)
        poses.append(node.feature.split(",")[0])
        node = node.next
    return words, poses


def plot_top10(word_count, xlabel='', ylabel=''):
    sorted_word_count = sorted(word_count.items(), key=lambda a: a[1], reverse=True)
    top10_word_count = [list(x) for x in zip(*sorted_word_count[:10])]
    labels = top10_word_count[0]
    y = top10_word_count[1]
    x = np.arange(len(y))

    fig, ax = plt.subplots()
    rect = ax.bar(x, y, 0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


class Main:
    def __init__(self):
        self.not_word = ["BOS/EOS", "*", "記号"]
        pass

    def a30(self, display=True):
        with open("neko.txt.mecab") as f:
            neko = f.readlines()
        analyzed_words = [n.split('\t') for n in neko]
        organized = []
        for w in analyzed_words:
            if len(w) == 2:
                f = w[1].split(",")
                o = dict([("surface", w[0]), ("base", f[6]), ("pos", f[0]), ("pos1", f[1])])
                organized.append(o)
        if display:
            pprint(organized)
        else:
            return organized

    def a31(self):
        organized = self.a30(display=False)
        for morph in organized:
            if morph['pos'] == '動詞':
                print(morph['surface'])

    def a32(self):
        organized = self.a30(display=False)
        for morph in organized:
            if morph['pos'] == '動詞':
                print(morph['base'])

    def a33(self):
        organized = self.a30(display=False)
        for i in range(1, len(organized)-1):
            if organized[i]['surface'] == 'の' and organized[i]['pos1'] == "連体化":
                print("{}の{}".format(organized[i-1]['surface'], organized[i+1]['surface']))

    def a34(self):
        organized = self.a30(display=False)
        previous_index = None
        for i, v in enumerate(organized):
            if v["pos"] == "名詞":
                if previous_index is None:
                    previous_index = i
            else:
                if previous_index is not None:
                    if i - previous_index > 1:
                        print("".join([o["surface"] for o in organized[previous_index:i]]))
                    previous_index = None

    def a35(self, display=True):
        organized = self.a30(display=False)
        word_count = defaultdict(int)
        for morph in organized:
            if morph["pos"] not in self.not_word:
                word_count[morph["surface"]] = word_count[morph["surface"]] + 1
        if display:
            pprint(word_count)
        else:
            return word_count

    def a36(self, output=True):
        word_count = self.a35(display=False)
        plot_top10(word_count, xlabel="単語", ylabel="出現頻度")

    def a37(self, output=True):
        with open("neko.txt") as f:
            neko = f.readlines()
        words_list, poses_list = [], []
        for s in neko:
            w, p = morph_analysis(s)
            words_list.append(w)
            poses_list.append(p)
        co_occurrence = defaultdict(int)
        for words, poses in zip(words_list, poses_list):
            if "猫" in words:
                for w, p in zip(words, poses):
                    if p not in self.not_word:
                        co_occurrence[w] = co_occurrence[w] + 1
        if "猫" in co_occurrence.keys():
            co_occurrence.pop("猫")
        plot_top10(co_occurrence, xlabel="単語", ylabel="共起頻度")

    def a38(self, output=True):
        word_count = self.a35(display=False)
        x = list(word_count.values())
        plt.hist(x, bins=30, range=(0, 30))
        plt.xlim(1, 30)
        plt.xlabel("単語の出現頻度")
        plt.ylabel("単語の種類")
        plt.show()

    def a39(self):
        word_count = self.a35(display=False)
        sorted_count = sorted(word_count.values(), reverse=True)
        x = np.arange(len(sorted_count))
        fig, ax = plt.subplots()
        ax.plot(x, sorted_count, '.')
        ax.set_xscale('log')
        ax.set_yscale('log')
        plt.xlabel("順位(対数)")
        plt.ylabel("出現頻度（対数）")
        plt.show()

if __name__ == "__main__":
    fire.Fire(Main)