from index import IndexManager
import math


def computeWeight(termFrequency, documentFrequency, totalDocuments):
    IDF = math.log(totalDocuments / documentFrequency, 10)
    weightedTF = 1 + math.log(termFrequency, 10)
    return weightedTF * IDF


# K is the number of top documents to list out
def cosineScore(queryTerms: list, index_manager: IndexManager, K):
    rankedDocuments = []
    scores = dict()
    length = dict()
    for term in set(queryTerms):

        # Query Term frequency
        TFtq = queryTerms.count(term)

        # Query term weight
        WTtq = computeWeight(TFtq, index_manager.get_doc_freq(term), index_manager.doc_count ) # clarify working methods

        # fetching postings list for term
        postingsList = index_manager.get_postings(term)
        doc_freq = index_manager.get_doc_freq(term)

        for doc_id, tf in postingsList:

            # Document term weight
            WTtd = computeWeight(tf, doc_freq, index_manager.doc_count)

            scores[doc_id] = scores.get(doc_id, 0) + WTtd * WTtq

            # W1^2 + W2^ + ... + Wn^2
            length[doc_id] = length.get(doc_id, 0) + math.pow(WTtd, 2)

    

    # normalizing document scores
    for d in scores.keys():
        
        # sqrt(  W1^2 + W2^ + ... + Wn^2  )
        length[d] = math.sqrt(length[d])
        scores[d] = scores[d] / length[d]

    # rank the documents by their score
    i = 0
    for d, _ in sorted(scores.items(), key = lambda x : x[1], reverse=True):
        rankedDocuments.append(index_manager.get_url(d))
        if i == K:
            break

    return rankedDocuments


if __name__ == "__main__":
    print(computeWeight(3,300,8000))






