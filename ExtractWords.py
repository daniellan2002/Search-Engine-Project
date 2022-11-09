import os
import json
from bs4 import BeautifulSoup

d = "DEV"

def iterateFiles(parentDirectory):

    documentCount = 0

    for directory in os.listdir(parentDirectory):
        d = os.path.join(parentDirectory,directory)
        if os.path.isdir(d):
            for filename in os.listdir(d):
                f = os.path.join(d,filename)
                if os.path.isfile(f):

                    # returns text body of file (type str)
                    #extractWords(f)
                    print(f)
                    documentCount += 1

                    # tokenizer returns a dictionary
    return documentCount


def extractWords(file):
    f = open(file)
    data = json.load(f)
    soup = BeautifulSoup(data['content'], 'html.parser')
    f.close()
    return soup.get_text()


if __name__ == "__main__":
    file = "DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json"
    directory = "ANALYST"
    directory2 = "DEV"
    dir = "ANALYST/www_cs_uci_edu"
    #print(iterateFiles(directory))
    for i in os.listdir(dir):
        extractWords(os.path.join(dir,i))
