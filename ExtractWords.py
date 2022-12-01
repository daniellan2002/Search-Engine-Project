import os
import json
from bs4 import BeautifulSoup
import tokenizer


def iterateFiles(parentDirectory, index):

    documentCount = 0

    for directory in os.listdir(parentDirectory):
        d = os.path.join(parentDirectory,directory)
        if os.path.isdir(d):
            for filename in os.listdir(d):
                f = os.path.join(d,filename)
                if os.path.isfile(f):

                    # returns text body of file (type str)
                    text, url = extractWords(f, {"title": 5, "h1": 3, "h2": 2, "h3": 1})
                    # list of tokens
                    tokens = tokenizer.tokenize(text)
                    # update the inverted index
                    index.update_index(tokens, url)

                    # increment document count
                    documentCount += 1

    return documentCount


def extractWords(file, importance: dict):
    f = open(file)
    data = json.load(f)
    # "lxml" option processes HTML docs faster, and handles broken HTML better
    soup = BeautifulSoup(data['content'], "lxml")
    url = data['url']
    f.close()

    text = soup.get_text()
    for tag_type in importance.keys():
        important_tags = soup.find_all(tag_type)
        for _ in range(importance[tag_type]):
            text += "\n" + " ".join(tag.get_text() for tag in important_tags)
    return text, url


if __name__ == "__main__":
    p = "/Users/jackyu/Downloads/DEV/hack_ics_uci_edu/0f96f6f6999f8c8d6618a797a55bcbc8298d012b451b916d0fb08a77dd08c98a.json"
    results = extractWords(p)
    print(results)
