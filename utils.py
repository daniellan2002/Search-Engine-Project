import pickle
import shelve
import os
import sys
from ExtractWords import extractWords


def create_pickle(parentDirectory):
    """
    serialize a set of all urls to a pickle file
    """
    urls = set()
    count = 0
    for directory in os.listdir(parentDirectory):
        d = os.path.join(parentDirectory, directory)
        if os.path.isdir(d):
            for filename in os.listdir(d):
                f = os.path.join(d, filename)
                if os.path.isfile(f):
                    text, url = extractWords(f, dict())
                    urls.add(url)
                    count += 1

                    if count % 100 == 0:
                        print("\r", count, end='')
    with open("urls.pickle", "wb") as file:
        pickle.dump(urls, file)

    print("\r", len(urls))


def transform_pickle(pickle_path):
    """
    Decodes the pickle file containing a set of all urls, and use the 'hash' function to create a shelve mapping from
    doc_id to url.
    """
    with open(pickle_path, "rb") as file:
        urls = pickle.load(file)

    db = shelve.open("storage/URL_map.shelve")
    for url in urls:
        db[str(hash(url))] = url
    db.close()


def set_hash_seed():
    # https://gist.github.com/mkolod/853cda9950b898d056ac149abc45417a
    # Set hash seed and restart interpreter.
    # It is necessary if the same index file (which contain hash values of urls as doc_id) is shared on different devices.
    if not os.environ.get('PYTHONHASHSEED'):
        os.environ['PYTHONHASHSEED'] = '1234'
        os.execv(sys.executable, ['python3'] + sys.argv)


if __name__ == "__main__":
    set_hash_seed()
