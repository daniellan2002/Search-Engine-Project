import sys
import re
import os


### TODO
### x Handle User Input Errors -> (Non English) & (Non Text Files)


# Runtime Complexity Evaluations
# This function will traverse through at most n tokens in the text file, assuming
# each word in the file is a token to be recorded. So the runtime complexity for
# this function will be linear, or O(N), where N is the number of words in the text file.
def tokenize(long_str: str) -> list:
    storage = []

    for n in re.split(r'[^a-zA-Z0-9]', long_str):
        if n.isalpha():
            storage.append(n.lower())
        elif n.isdigit():
            storage.append(n)

    return storage


# Runtime Complexity Evaluations
# This function will traverse through at most n tokens to record each unique token, given by
# the parameter list, assuming each word in the file is a token to be recorded. So the runtime
# complexity for this function will be linear, or O(N), where N is the number of words in the text file.
def computeWordFrequencies(tokens: list) -> dict:
    collection = dict()
    # split each line into words
    for each in tokens:
        # token = re.sub(r"[^a-zA-Z0-9]", "", each)
        if each not in collection:
            collection[each] = 1
        else:
            collection[each] += 1

    return collection


# Runtime Complexity Evaluations
# This function will also be O(N) for its runtime complexity as the function just goes through
# each token recorded and prints them out.
def printFrequencies(frequencies_map: dict):
    for token, freq in frequencies_map.items():
        print(token, "->", freq)


# The main function will have a time complexity of O(N), because although the this function goes
# through the list of tokens twice, once to tokenize them, and once to record them, they happen
# parallel to each other's operation. So O(2N) can be simplified to O(N).
def main_run():
    '''
        Runs the text processing application
    '''
    try:

        ### Example Case
        a_ver_long_string = "hello this is not a very long string, you got juked \n jk it is sort of long, but it's not terribly long 135 90 80 /,/.,"

        all_tokens = tokenize(a_ver_long_string)

        frequencies = computeWordFrequencies(all_tokens)

        printFrequencies(frequencies)
    except:
        print("Unexpected Input: Aborting...")


if __name__ == '__main__':
    main_run()