import shelve
import csv
import sys
from pathlib import Path
from hashlib import sha256
from urllib.parse import urlparse
import dbm
import math

from tokenizer import computeWordFrequencies


class IndexManager:
    """
    Stores an inverted index containing Term Frequency scores. Also stores a mapping from doc_id to url.
    To store data into permanent disk storage, use save_partial_index & save_url_map methods.
    """
    partial_folder = "partial_index"

    def __init__(self, doc_count, prefix="index", root=".", max_index_size=10_000_000, url_hash_function=hash):
        self.doc_count = doc_count
        self._prefix = prefix
        self._root = root
        self._max_index_size = max_index_size
        self._hash_function = url_hash_function
        self._full_index_file = None
        self._index_format = "csv"
        Path(self._root + "/" + self.partial_folder).mkdir(exist_ok=True, parents=True)

        self._RAM_reset()
        self.url_db = shelve.open(self._root + "/URL_map.shelve")
        self._create_index_of_index()

    def update_index(self, tokens, url):
        # hash the url to get integer document id
        doc_id = self._hash_function(url)
        self.url_db[str(doc_id)] = url
        self.url_db.sync()

        # compute word frequency for the given document
        word_freq = computeWordFrequencies(tokens)

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
        index_path = self._get_index_file_name(self._partial_index_count, is_partial=True)
        with open(index_path, "w") as file:
            writer = csv.writer(file)
            for item in sorted(self._tf_index.items(), key=lambda item: item[0]):
                writer.writerow(item)
        print("\nindex occupies", self._tf_index_size + sys.getsizeof(self._tf_index), "bytes of RAM.")
        print("saved to disk as " + index_path)
        self._RAM_reset()

    # def save_url_map(self):
    #     db = shelve.open(self._root + "/URL_map.shelve")
    #     for doc_id, url in self._url_map.items():
    #         db[doc_id] = url
    #     db.close()

    def merge_partial_indices(self):
        full_index_path = self._get_index_file_name("full")

        # open all the necessary files
        partial_index_files = []
        full_index_file = open(full_index_path, 'w')

        for index_file in Path(self._root + f"/{self.partial_folder}").glob(f"index_*.{self._index_format}*"):
            file = open(index_file, 'r')
            partial_index_files.append(file)

        # remove any reader from the list if reached End of File
        readers = [csv.reader(f) for f in partial_index_files]
        writer = csv.writer(full_index_file)
        frontier = []  # the next lines for each reader
        readers_to_remove = []  # all the readers that reached End of File. They will be removed in each while iteration
        frontier_to_remove = []  # size of frontier should reflect size of readers list. So remove frontier lines whose file reached End of File.

        # initialize the frontier lines
        for f in range(len(readers)):
            try:
                frontier.append(next(readers[f]))
            except StopIteration:
                readers_to_remove.append(readers[f])

        for value in readers_to_remove:
            readers.remove(value)
        readers_to_remove.clear()

        # at this point, we can make sure no reader in the list reached End of File
        # keep merging the indices, unless all files have reached end of file.
        while len(readers) > 0:
            # only process the first element of the sorted frontier (sorted by token in alphabetical order)
            sorted_frontier = sorted(enumerate(frontier), key=lambda pair: pair[1][0])
            last_token = None
            current_postings = []
            for i, (f, line) in enumerate(sorted_frontier):
                token, postings = line

                if i == 0:
                    current_token = token

                # in case the first sorted token has ties, also process the same token that appears in other files.
                if i == 0 or token == last_token:
                    current_postings.extend(eval(postings))
                    last_token = token
                    try:
                        # the current line has been put into the full index, so push the next line into frontier
                        frontier[f] = next(readers[f])
                    except StopIteration:
                        # reader[f] reached end of file. So remove it from readers list, and update frontier, too.
                        readers_to_remove.append(readers[f])
                        frontier_to_remove.append(frontier[f])
                else:
                    break  # break out of the for loop

            for value in readers_to_remove:
                readers.remove(value)
            readers_to_remove.clear()

            for value in frontier_to_remove:
                frontier.remove(value)
            frontier_to_remove.clear()

            doc_freq = len(current_postings)
            sorted_postings = sorted(current_postings, key=lambda posting: posting[1], reverse=True)
            sorted_postings = [posting for posting in map(lambda post: (post[0], 1 + math.log(post[1], 10)), sorted_postings)]
            idf = math.log(self.doc_count / doc_freq, 10)
            writer.writerow([current_token, (idf, sorted_postings)])

    def get_postings(self, term: str) -> list:
        _, postings = self.get_term_info(term)
        return postings

    def get_doc_freq(self, term: str) -> int:
        doc_freq, _ = self.get_term_info(term)
        return doc_freq

    def get_url(self, doc_id: int) -> str:
        return self.url_db[str(doc_id)]

    def get_term_info(self, term: str) -> (int, list):
        try:
            curser = self._index_of_index[self._hash_function(term)]
        except KeyError:
            return 0, []  # the term isn't in the inverted index, so 0 doc_freq, and empty postings list
        self._full_index_file.seek(curser)

        # each line looks like "content here"\n
        # so, ignore the first '"' and the last '"\n'
        info = eval(self._full_index_file.readline()[1:-2])
        return info

    def _RAM_reset(self):
        """
        empty the index stored in RAM, and reset the variables that track the size of the index in RAM
        """
        self._tf_index = dict()
        self._partial_index_count = sum(
            1 for _ in Path(self._root + f"/{self.partial_folder}").glob(f"index_*.{self._index_format}*"))
        self._tf_index_size = 0

    def print_index(self, index_id, is_partial=False):
        choice = input("The index may be super large. Still want to print? y/[n]\n")
        if choice.lower() != "y":
            return
        try:
            url_db = shelve.open(self._root + "/URL_map.shelve", "r")
        except dbm.error:
            raise FileNotFoundError(
                "shelve file " + self._root + "/URL_map.shelve" + " cannot be read with 'r' mode because it doesn't exist")

        index_file_name = self._get_index_file_name(index_id, is_partial=is_partial)
        print("\n", "-" * 10, "reading", index_file_name, "-" * 10)

        with open(index_file_name, "r") as file:
            reader = csv.reader(file)
            for token, postings in reader:
                postings = eval(postings)
                print(token, ":", sep="")
                for doc_id, freq in postings:
                    print("\t", freq, "->", url_db[doc_id])

    def _create_index_of_index(self):
        index_path = self._get_index_file_name("full", is_partial=False)
        self._index_of_index = dict()
        try:
            self._full_index_file = open(index_path, "r")
            while True:
                cursor = self._full_index_file.tell()
                line = self._full_index_file.readline()
                if line == "":
                    break
                words = line.split(",")
                term = words[0]
                self._index_of_index[self._hash_function(term)] = cursor + len(
                    term) + 1  # cursor for the beginning of postings
            self._full_index_file.seek(0)  # reset cursor to start of file
        except FileNotFoundError:
            print("index not found")

    @staticmethod
    def _get_iterable_size(obj):
        """
        Can only calculate size of iterable objects whose elements don't store reference to other objects.
        In other words, no support for nested list, nested tuple, etc."""
        size = sys.getsizeof(obj)
        size += sum(sys.getsizeof(element) for element in obj)
        return size

    def _get_index_file_name(self, index_id, is_partial=False):
        if is_partial:
            return self._root + f"/{self.partial_folder}/index_{index_id}.{self._index_format}"
        else:
            return self._root + f"/index_{index_id}.{self._index_format}"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.url_db.close()
        self._full_index_file.close()


if __name__ == "__main__":
    """Example usage"""
    # create and update index
    index_manager = IndexManager(root="./storage")  # format can change between shelve and csv
    index_manager.update_index("this is jack speaking typing and testing the code snippet".split(),
                               "https://first-url.com")
    index_manager.update_index("this is the content of the second url".split(), "https://2nd-url.com")

    # must save to disk
    index_manager.save_partial_index()

    # stored on another partial index
    index_manager.update_index("the second url sitting on the second partial index".split(),
                               "https://third-url.com")
    index_manager.update_index("here is the last site stored within the second partial index".split(),
                               "https://4th-url.com")

    # save to disk again
    index_manager.save_partial_index()

    # create a full index by merging all partial indices
    index_manager.merge_partial_indices()

    # uncomment to inspect the indices.
    # Be careful, you might print out a GIANT message on the console
    # index_manager.print_index(0, is_partial=True)
    # index_manager.print_index(1, is_partial=True)
    # index_manager.print_index("full")
