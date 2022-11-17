import sys
import tokenizer
import index


def get_query_cli() -> list:
    '''
        Can only take words or numbers without punctuations
        -> Returns a list of tokens from the CLI input
    '''
    try:

        file_path = sys.argv[1:]

    except:
        print("Unexpected Input: Aborting...")
    
    return file_path

def parse_input(user_input:str) -> list:

    all_tokens = tokenizer.tokenize(user_input)

    unique_tokens = tokenizer.computeWordFrequencies(all_tokens).keys()

    return list(unique_tokens)

def boolean_search(user_input:str) -> list:

    intersection_ids = []

    # 2.Parse the string into tokens
    tokens = parse_input(user_input)

    postings_mapping = []

    # 3.Create the inverted index
    for each in tokens:
        # Map each token with a list of doc ids -> (token, [ids])
        postings_mapping.append((each, [each[0] for each in index.get_postings(each)]))
    
    # Sort the inverted index by the length of doc id list
    sorted_mapping = sorted(postings_mapping, key=lambda n: n[1])

    intersection_ids = set(sorted_mapping[0][1])

    for each in sorted_mapping:
        intersection_ids = intersection_ids & set(each[1])
    
    return list(intersection_ids)


if __name__ == '__main__':
    # 1.Get the query as a string

    user_query = get_query_cli()

    user_query_custom = "This this this string's filled with punctuations."

    boolean_search(user_query)

    boolean_search(user_query_custom)
