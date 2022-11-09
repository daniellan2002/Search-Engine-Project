import sys
import re
import os

### TODO 
### x Refine tokenizer (Numbers and Chars) -> DONE
### x Handle User Input Errors -> (Non English) & (Non Text Files) 
### 3. Write Big O run time analysis


def tokenize(text_file_path:str) -> list:

    all_tokens = helper(text_file_path)

    return list(computeWordFrequencies(all_tokens).keys())

# Runtime Complexity Evaluations
# This function will traverse through at most n tokens in the text file, assuming
# each word in the file is a token to be recorded. So the runtime complexity for
# this function will be linear, or O(N), where N is the number of words in the text file.
def helper(text_file_path:str) -> list:

    storage = []

    reader = None
    try:
        with open(text_file_path, 'r') as reader:
            for line in reader.readlines():
                for n in re.split(r'[^a-zA-Z0-9]', line):
                    if (n.isalpha()):
                        storage.append(n.lower())
                    elif (n.isdigit()):
                        storage.append(n)
    except OSError:
        print("OS ERROR")
    except ValueError:
        print("VALUE ERROR")
    finally:
        if reader != None:
            reader.close()
    
    return storage

# Runtime Complexity Evaluations
# This function will traverse through at most n tokens to record each unique token, given by 
# the parameter list, assuming each word in the file is a token to be recorded. So the runtime 
# complexity for this function will be linear, or O(N), where N is the number of words in the text file.
def computeWordFrequencies(tokens:list) -> dict:

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
def printFrequencies(frequencies_map:dict):

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

        file_path = sys.argv[1]

        all_tokens = helper(file_path)

        frequencies = computeWordFrequencies(all_tokens)

        printFrequencies(frequencies)
    except:
        print("Unexpected Input: Aborting...")

    


if __name__ == '__main__':
    main_run()