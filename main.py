from index import IndexManager
from ExtractWords import iterateFiles
from tokenizer import tokenize
from BooleanQuery import boolean_search
from CosineSimilarity import cosineScore
import time
import os
import sys


NUM_DOCS = 55393
def main_M1():
    # directory = "/Users/jackyu/Downloads/ANALYST"
    directory = "/Users/jackyu/Downloads/DEV"

    start = time.time()
    index_manager = IndexManager(NUM_DOCS, root="./storage")

    doc_count = iterateFiles(directory, index_manager)
    finish_partials = time.time()
    print(f"generating all partial indices took {round(finish_partials - start, 2)} seconds")
    index_manager.save_partial_index()

    print("merging indices... ", end='')
    index_manager.merge_partial_indices()
    finish_merging = time.time()
    print(f"done. Took {round(finish_merging - finish_partials, 2)} seconds")

    with open("storage/index_full.csv", "r") as file:
        token_count = 0
        for _ in file:
            token_count += 1

    print(token_count, "unique tokens")
    print(doc_count, "documents processed")


def main_M2n3():
    topk = 5
    index_manager = None
    try:
        print("Initializing index... ", end="")
        index_manager = IndexManager(NUM_DOCS, root="./storage")
        print("done")
        print("press 'control C' to quit searching")
        while True:
            query = input("\nyour search query: ")
            start_time = time.time()
            urls = cosineScore(query, index_manager)
            # urls = boolean_search(query, index_manager)
            search_time = time.time() - start_time
            print("search took {:2f} milliseconds. {} results for \"{}\"".format(search_time*1000, len(urls), " ".join(tokenize(query))))
            for i, link in enumerate(urls, 1):
                if i > topk:
                    break
                print(f"\t{i}:\t{link}")
    except KeyboardInterrupt:
        print("\ngoodbye ;)")
    finally:
        if index_manager is not None:
            index_manager.close()


if __name__ == "__main__":
    # https://gist.github.com/mkolod/853cda9950b898d056ac149abc45417a
    # Set hash seed and restart interpreter.
    # It is necessary if the same index file (which contain hash values of urls as doc_id) is shared on different devices.
    if not os.environ.get('PYTHONHASHSEED'):
        os.environ['PYTHONHASHSEED'] = '1234'
        os.execv(sys.executable, ['python3'] + sys.argv)
    # main_M1()
    main_M2n3()
