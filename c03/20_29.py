import json
import gzip
from pprint import pprint
import fire
import re

def extract(filename):
    with gzip.open(filename, 'rt', encoding="utf-8") as f:
        return [json.loads(line) for line in f.readlines()]

class Main():
    def __init__(self):
        raw_articles = extract("jawiki-country.json.gz")
        self.articles = dict([(a['title'], a["text"])for a in raw_articles])
        self.english = self.articles["イギリス"]

    def a20(self, display=False):
        pprint(self.english)

    def a21(self):
        for line in self.english.split('\n'):
            if "[[Category:" in line:
                print(line)

    def a22(self):
        pprint(list(set(re.findall(r'(?<=Category:)\w*', self.english))))

    def a23(self):
        section = list(set(re.findall(r'=+\w+=+', self.english)))
        pprint([(re.sub(r'=+', r'', s), s.count('=') // 2 - 1) for s in section])

    def a24(self):
        pprint(list(set(re.findall(r'(?<=ファイル:)[^\|]*', self.english))))

    def a25(self, display=True):
        raw_basic_info = re.findall(r'\{\{基礎情報.*?(?=\n\}\}\n\n)', self.english,
                                    flags=(re.DOTALL | re.MULTILINE))[0].split("\n|")
        basic_info = []
        for info in raw_basic_info:
            if "=" in info:
                basic_info.append(tuple(re.split("\s+=\s*", info)))
        basic_info = dict(basic_info)
        if display:
            pprint(basic_info)
        else:
            return basic_info

    def a26(self, display=True):
        basic_info = self.a25(display=False)
        for key, text in basic_info.items():
            basic_info[key] = re.sub(r'(\'{3}|\'{5})', r'', text)
        if display:
            pprint(basic_info)
        else:
            return basic_info

    def a27(self, display=True):
        basic_info = self.a26(display=False)
        for key, text in basic_info.items():
            basic_info[key] = re.sub(r'(\[{2}|\]{2})', r'', text)
        if display:
            pprint(basic_info)
        else:
            return basic_info

    def a28(self, display=True):
        basic_info = self.a27(display=False)
        markup_regex = r'\{{2}lang\|\w*\||\}{2}' \
                       r'|\<.*\>' \
                       r'|\{{2}.*icon.*\}{2}' \
                       r'|\{{2}'
        for key, text in basic_info.items():
            basic_info[key] = re.sub(markup_regex, r'', text)
        if display:
            pprint(basic_info)
        else:
            return basic_info

    def a29(self, display=False):
        import requests
        basic_info = self.a28(display=False)
        s = requests.Session()
        api_url = "https://en.wikipedia.org/w/api.php"
        params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": "File:" + basic_info["国旗画像"]
        }

        r = s.get(url=api_url, params=params)
        info_json = r.json()
        imageinfo = info_json["query"]["pages"]["23473560"]["imageinfo"][0]
        pprint(imageinfo["url"])

if __name__ == '__main__':
    fire.Fire(Main)
