import index
from ExtractWords import iterateFiles
import time


def main():
    # directory = "/Users/jackyu/Downloads/ANALYST"
    directory = "/Users/jackyu/Downloads/DEV"

    start = time.time()
    myIndex = index.IndexManager(root="./storage", index_format="csv")
    doc_count = iterateFiles(directory, myIndex)
    finish_partials = time.time()
    print(f"generating all partial indices took {round(finish_partials - start, 2)} seconds")
    myIndex.save_partial_index()

    print("merging indices...")
    myIndex.merge_partial_indices()
    finish_merging = time.time()
    print(f"merging partial indices took {round(finish_merging - finish_partials, 2)} seconds")

    with open("storage/index_full.csv", "r") as file:
        token_count = 0
        for _ in file:
            token_count += 1

    print(token_count, "unique tokens")
    print(doc_count, "documents processed")


if __name__ == "__main__":
    main()
