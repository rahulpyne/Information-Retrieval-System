from os.path import exists

RELEVANT_DICT = {}
RANK_DICT = {}
NO_OF_QUERIES = 0
FILE_NAME = ""

def populate_dict():
    global NO_OF_QUERIES,FILE_NAME
    FILE_NAME = raw_input(">\tEnter the file name of the doc_score with proper extension\n")
    if exists(FILE_NAME):
        file_relevant = open('cacm.rel', 'r')
        file_rank_list = open (FILE_NAME, 'r')

        for line in file_relevant.readlines():
            query_key = line.split()[0]
            if not RELEVANT_DICT.has_key(query_key):
                RELEVANT_DICT[query_key] = [line[:-1]]
            else:
                content = RELEVANT_DICT.get(query_key)
                content.append(line[:-1])

        file_relevant.flush()
        file_relevant.close()

        for line in file_rank_list.readlines():
            query_key = line.split()[0]
            if not RANK_DICT.has_key(query_key):
                RANK_DICT[query_key] = [line[:-1]]
            else:
                content = RANK_DICT.get(query_key)
                content.append(line[:-1])

        NO_OF_QUERIES = len(RANK_DICT)
        file_rank_list.flush()
        file_rank_list.close()
    else:
        print "The file does not exist"


def evaluate_MRR():

    query_ID = 1
    reciprocal_ranking = 0

    while query_ID != NO_OF_QUERIES+1:

        if not RELEVANT_DICT.get(str(query_ID)):
            reciprocal_ranking += 0
            query_ID += 1
            continue

        relevant_doc_list = RELEVANT_DICT[str(query_ID)]
        ranked_doc_list = RANK_DICT[str(query_ID)]

        for doc in ranked_doc_list:
            flag_break = False
            docID = doc.split()[2]
            for rel_doc in relevant_doc_list:
                if docID == rel_doc.split()[2]:
                    reciprocal_ranking += 1.0 / float(doc.split()[3])
                    #print "The reciprocal ranking is " + str(reciprocal_ranking)
                    flag_break = True
                    break
            if flag_break == True:
                break
        query_ID += 1

    mean_reciprocal_ranking = reciprocal_ranking / float(NO_OF_QUERIES)
    print "The mean reciprocal ranking is: " + str(mean_reciprocal_ranking)

def evaluate_pk_measure():

    pk_dictionary_5 = {}
    pk_dictionary_20 = {}
    query_ID = 1

    while query_ID != NO_OF_QUERIES+1:

        if not RELEVANT_DICT.get(str(query_ID)):
            pk_dictionary_5[query_ID] = 0.0
            pk_dictionary_20[query_ID] = 0.0
            query_ID += 1
            continue

        relevant_doc_list = RELEVANT_DICT[str(query_ID)]
        top_5_ranked_doc_list = RANK_DICT[str(query_ID)][:5]
        top_20_ranked_doc_list = RANK_DICT[str(query_ID)][:20]
        #print ranked_doc_list

        rel_doc_counter_top5 = 0
        for doc in top_5_ranked_doc_list:
            docID = doc.split()[2]
            for rel_doc in relevant_doc_list:
                if docID == rel_doc.split()[2]:
                    rel_doc_counter_top5 += 1

        pk_dictionary_5[query_ID] = rel_doc_counter_top5 / 5.0

        rel_doc_counter_top20 = 0
        for doc in top_20_ranked_doc_list:
            docID = doc.split()[2]
            for rel_doc in relevant_doc_list:
                if docID == rel_doc.split()[2]:
                    rel_doc_counter_top20 += 1

        pk_dictionary_20[query_ID] = rel_doc_counter_top20 / 20.0

        query_ID += 1

    print "Printing p@k value for K=5..."
    print pk_dictionary_5
    print "Printing p@k value for K=20..."
    print pk_dictionary_20


def evaluate_precision_and_recall():

    precision_dict = {}
    recall_dict = {}
    sum_average_precision = 0
    for query in RANK_DICT:
        average_precision = 0
        doc_counter = 0
        doc_found = 0
        precision_sum = 0

        if not RELEVANT_DICT.get(str(query)):
            precision_dict[query] = []
            recall_dict[query] = []
            continue


        relevant_doc_list = RELEVANT_DICT[query]
        relevant_doc_count = len(relevant_doc_list)
        precision_dict[query] = []
        recall_dict[query] = []
        for doc in RANK_DICT[query]:
            doc_counter +=1
            docID = doc.split()[2]
            doc_found_flag = False
            for rel_doc in relevant_doc_list:
                if docID ==  rel_doc.split()[2]:
                    doc_found_flag = True
                    break;
            if doc_found_flag:
                doc_found += 1
                precision = float(doc_found) / float(doc_counter)
                precision_sum = precision_sum + precision
                #print "The precision for " + str(docID) + " is: " + str(precision)
                precision_dict[query].append({docID : precision})
                recall = float(doc_found) / float(relevant_doc_count)
                #print "The recall for " + str(docID) + " is: " + str(recall)
                recall_dict[query].append({docID : recall})
            else:
                precision = float(doc_found) / float(doc_counter)
                #print "The precision for " + str(docID) + " is: " + str(precision)
                precision_dict[query].append({docID : precision})
                recall = float(doc_found) / float(relevant_doc_count)
                #print "The recall for " + str(docID) + " is: " + str(recall)
                recall_dict[query].append({docID : recall})
        average_precision = average_precision + float(precision_sum) / float(doc_found)
        sum_average_precision = sum_average_precision + average_precision
        #print "The average precision for " + str(query) + " is: " + str(average_precision)

    print "Printing precision dictionary..."
    print precision_dict
    print "Printing recall dictionary..."
    print recall_dict
    mean_average_precision = float(sum_average_precision) / float(NO_OF_QUERIES)
    print "The mean average precision is: " + str(mean_average_precision)


# main function
def main():

    populate_dict()
    print "Evaluating MRR..."
    evaluate_MRR()
    print "Evaluating p@k..."
    evaluate_pk_measure()
    print "Evaluating precision and recall..."
    evaluate_precision_and_recall()


if __name__ == "__main__": main()
