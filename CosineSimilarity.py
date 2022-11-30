from index import IndexManager
import math
from tokenizer import tokenize


def cosineScore(query: str, index_manager: IndexManager):
    queryTerms = tokenize(query)
    rankedDocuments = []
    scores = dict()
    length = dict()
    q_length = 0
    for term in set(queryTerms):
        # fetching postings list for term
        idf, postingsList = index_manager.get_term_info(term)

        # Query Term frequency
        TFtq = queryTerms.count(term)

        # Query term weight
        WTtq = (1 + math.log(TFtq, 10)) * idf
        q_length += WTtq ** 2

        for doc_id, WTtd in postingsList:
            scores[doc_id] = scores.get(doc_id, 0) + WTtd * WTtq

            # W1^2 + W2^ + ... + Wn^2
            length[doc_id] = length.get(doc_id, 0) + WTtd ** 2

    # sqrt(  W1^2 + W2^ + ... + Wn^2  )
    # normalizing document scores
    for d in scores.keys():
        scores[d] = scores[d] / (math.sqrt(length[d]) * math.sqrt(q_length))
        if scores[d] < 0 or scores[d] > 1:
            print(f"similarity is out of range: {round(scores[d], 2)}", index_manager.get_url(d))

    # rank the documents by their score
    for d, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        rankedDocuments.append(index_manager.get_url(d))

    return rankedDocuments

