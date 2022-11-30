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
                    text, url = extractWords(f)

                    # list of tokens
                    tokens = tokenizer.tokenize(text)

                    # update the inverted index
                    index.update_index(tokens,url)

                    # increment document count
                    documentCount += 1

    return documentCount


def extractWords(file):
    f = open(file)
    data = json.load(f)
    # "lxml" option processes HTML docs faster, and handles broken HTML better
    soup = BeautifulSoup(data['content'], "lxml")
    url = data['url']
    f.close()
    return soup.get_text(), url


if __name__ == "__main__":
    pass
