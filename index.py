import shelve
import sys
from pathlib import Path
from hashlib import sha256
from urllib.parse import urlparse


class IndexManager:
    """
    Stores an inverted index containing Term Frequency scores. Also stores a mapping from doc_id to url.
    To store data into permanent disk storage, use save_partial_index & save_url_map methods.
    """
    def __init__(self, prefix="index", root=".", max_index_size=1000000, url_hash_function=hash):
        self._prefix = prefix
        self._root = root
        self._max_index_size = max_index_size
        self._hash_function = url_hash_function

        self._RAM_reset()
        self._url_map = dict()
        # assert Path(self._root).is_dir()
        Path(self._root).mkdir(exist_ok=True, parents=True)

    def update_index(self, tokens, url):
        # hash the url to get integer document id
        doc_id = self._hash_function(url)
        self._url_map[doc_id] = url

        # compute word frequency for the given document
        word_freq = dict()
        for token in tokens:
            word_freq[token] = word_freq.get(token, 0) + 1

        # update the index whose postings store term frequency (tf)
        for token, freq in word_freq.items():
            posting = (doc_id, freq)
            self._tf_index_size += self._get_iterable_size(posting)
            if token not in self._tf_index:
                self._tf_index_size += sys.getsizeof(token)
                self._tf_index[token] = [posting]
            else:
                self._tf_index[token].append(posting)
        # if index in RAM is too large, save to disk
        if self._tf_index_size + sys.getsizeof(self._tf_index) > self._max_index_size:
            self.save_partial_index()

    def save_partial_index(self):
        db = shelve.open(self._get_partial_index_file_name(self._partial_index_count))
        for token in self._tf_index:
            db[token] = self._tf_index[token]

        db.close()
        print("index occupies", self._tf_index_size + sys.getsizeof(self._tf_index), "bytes.")
        print("saved to disk as " + self._get_partial_index_file_name(self._partial_index_count))
        self._RAM_reset()

    def save_url_map(self):
        db = shelve.open(self._root + "/URL_map.shelve")
        for doc_id, url in self._url_map.items():
            db[doc_id] = url
        db.close()

    def _RAM_reset(self):
        self._tf_index = dict()
        self._partial_index_count = sum(1 for _ in Path(self._root).glob("index_*.shelve*"))
        self._tf_index_size = 0
        print(self._partial_index_count)

    def print_index(self, index_id):
        index_db = shelve.open(self._get_partial_index_file_name(index_id))
        url_db = shelve.open(self._root + "/URL_map.shelve")
        for token in index_db.keys():
            print(token, ":", )
            for doc_id, count in index_db[token]:
                print(count, "->", url_db[doc_id])
            print()

        index_db.close()
        url_db.close()

    @staticmethod
    def _get_iterable_size(obj):
        """
        Can only calculate size of iterable objects whose elements don't store reference to other objects.
        In other words, no support for nested list, nested tuple, etc."""
        size = sys.getsizeof(obj)
        size += sum(sys.getsizeof(element) for element in obj)
        return size

    def _get_partial_index_file_name(self, index_num):
        return self._root + f"/index_{index_num}.shelve"


# function from assignment 2
def url_hash(url):
    parsed = urlparse(url)
    return sha256(
        f"{parsed.netloc}/{parsed.path}/{parsed.params}/"
        f"{parsed.query}/{parsed.fragment}".encode("utf-8")).hexdigest()


if __name__ == "__main__":
    """Example usage"""
    # create and update index
    index_manager = IndexManager(root="./storage", url_hash_function=url_hash)
    index_manager.update_index("this is Jack speaking typing and testing the code snippet".split(), "https://first-url.com")
    index_manager.update_index("this is the content of the second url".split(), "https://2nd-url.com")

    # must save to disk
    index_manager.save_partial_index()
    index_manager.save_url_map()

    # inspect the index
    index_manager.print_index(0)
