from glob import glob
import operator
import os
from os.path import exists
import traceback
from math import sqrt
from math import log


CURRENT_DIRECTORY = os.getcwd()
INPUT_FOLDER = path = os.path.join(CURRENT_DIRECTORY,'generated_corpus')
OUTPUT_FOLDER_PATH = path = os.path.join(CURRENT_DIRECTORY,'doc_score')
DOC_NAME ={} # mapping doc name and ids
QUERY_ID = 0

def generate_index():
    inverted_index = {}
    tokens_per_doc = {}
    try:
        counter=1
        num_of_files = len(glob(os.path.join(INPUT_FOLDER,'*.txt')))
        for file in glob(os.path.join(INPUT_FOLDER,'*.txt')):
            perc = float((counter/float(num_of_files)))*100
            print "Processing %s - Completed %r%%" %(file[(file.rindex('\\'))+1:],round(perc,2))
            DOC_NAME.update({counter:file.split('generated_corpus\\')[1][:-4]})
            doc_id = counter
            doc= open(file, 'r').read()
            tokens_per_doc.update({doc_id:len(doc.split())})
            for term in doc.split():
                if not inverted_index.has_key(term):
                    doc_term_freq ={doc_id:1}
                    inverted_index.update({term:doc_term_freq})
                elif not inverted_index[term].has_key(doc_id):
                    inverted_index[term].update({doc_id:1})
                else:
                    inverted_index[term][doc_id] += 1
            counter+=1
        total_num_of_docs = counter-1
        for term in inverted_index:
            idf = 1.0 + log(float(total_num_of_docs) / float(len(inverted_index[term].keys()) + 1)) # implmenting log(N/(n+1)) and adding 1.0 to prevent sending 0.
            for doc in inverted_index[term]:
                normalized_tf = float(inverted_index[term][doc])/float(tokens_per_doc[doc]) # normalizing tf by dividing tf by number of tokens in that document
                inverted_index[term][doc] = normalized_tf * idf # normalizing term frequencies relative to the number of tokens in each doc
    except Exception as e:
        print(traceback.format_exc())
    return inverted_index,total_num_of_docs

def generate_doc_vsm_score(query,inverted_index,total_num_of_docs):
    try:
        query_term_freq = {}
        query_term_list = query.split()
        reduced_inverted_index = {} # this inverted_index contains only those terms which are present in query
        doc_magnitude = {} # stores the document magnitude for all the terms
        for term in query_term_list:
            if not query_term_freq.has_key(term):
                query_term_freq.update({term:1})
            else:
                query_term_freq[term]+=1
        #normalizing the term frequency in query and also reducing the inverted_index with only required terms in query
        for term in query_term_freq:
            query_term_freq[term] = float(query_term_freq[term])/float(len(query_term_list)) # normalizing the term frequencies in query relative to total number of tokens in query
            if inverted_index.has_key(term):
                reduced_inverted_index.update({term:inverted_index[term]})
            else:
                reduced_inverted_index.update({term:{}})
        #using inverted_index to get doc_magnitude for each document present in reduced_inverted_index
        for term in reduced_inverted_index:
            for doc_id in reduced_inverted_index[term]:
                if not doc_magnitude.has_key(doc_id):
                    doc_id_mag = fetch_doc_mag(doc_id,inverted_index) #getting doc_magnitude for all the term from main inverted_index for a given doc_id
                    doc_magnitude.update({doc_id:doc_id_mag})

        cosine_similarity(query_term_freq,reduced_inverted_index,total_num_of_docs,doc_magnitude)
    except Exception as e:
        print(traceback.format_exc())

def fetch_doc_mag(doc_id,inverted_index):
    doc_magnitude = 0
    for term in inverted_index:
        if inverted_index[term].has_key(doc_id):
            doc_magnitude += inverted_index[term][doc_id]**2
    return sqrt(doc_magnitude)


def cosine_similarity(query_term,inverted_index,total_num_of_docs,doc_magnitude):
    dot_product = {}
    query_magnitude = 0
    doc_score = {}
    try:
        for term in inverted_index: # inverted_index.keys() and query_term.keys() are same
            idf = 1.0 + log(float(total_num_of_docs) / float(len(inverted_index[term].keys()) + 1)) # implmenting log(N/(n+1)) and adding 1.0 to prevent sending 0.
            query_term[term] *= idf # implementing tf*idf for query terms
            query_magnitude += (query_term[term]**2) # generating the query_magnitude
            for doc_id in inverted_index[term]:
                # generating the dot_product per doc_id
                if not dot_product.has_key(doc_id):
                    dot_product.update({doc_id:(query_term[term] * inverted_index[term][doc_id])})
                else:
                    dot_product[doc_id] += (query_term[term] * inverted_index[term][doc_id])

        query_magnitude = sqrt(query_magnitude)

        for doc in doc_magnitude: # doc_magnitude and dot_product has same keys
            vsm_denominator = query_magnitude * doc_magnitude[doc]
            doc_score.update({doc:(float(dot_product[doc])/float(vsm_denominator))})

        sorted_doc_score = sorted(doc_score.items(), key=operator.itemgetter(1), reverse=True)
        write_doc_score(sorted_doc_score)
    except Exception as e:
        print(traceback.format_exc())

def write_doc_score(sorted_doc_score):
    try:
        if(len(sorted_doc_score)>0):
            out_file  = open(OUTPUT_FOLDER_PATH+"\\VSM_doc_score.txt",'a')
            for i in range(min(100,len(sorted_doc_score))):
                doc_id,doc_score = sorted_doc_score[i]
                out_file.write(str(QUERY_ID) + " Q0 "+ DOC_NAME[doc_id] +"(doc_id = "+ str(doc_id)+") " + str(i+1) + " " + str(doc_score) +" Vector_Space_Model\n")
            out_file.write("\n\n")
            out_file.close()
            print "\nDocument Scoring for Query id = " +str(QUERY_ID) +" has been generated inside VSM_doc_score.txt"
        else:
            print "\nTerm not found in the corpus"
    except Exception as e:
        print(traceback.format_exc())


def start():
    try:
        global QUERY_ID
        inverted_index,total_num_of_docs = generate_index()
        print "========================================================"
        print "\n\t     Inverted Index generated\n"
        print "========================================================"
        print "\n\t      Query Processing begins\n"
        print "========================================================"
        #Removing the existing VSM_doc_score.txt to prevent appending the new results with the old one.
        if exists(OUTPUT_FOLDER_PATH+"\\VSM_doc_score.txt"):
            os.remove(OUTPUT_FOLDER_PATH+"\\VSM_doc_score.txt")
        query_file = open("query.txt", 'r')
        for query in query_file.readlines():
            QUERY_ID+=1
            query = query.lstrip()
            query = query.rstrip()
            generate_doc_vsm_score(query.lower(),inverted_index,total_num_of_docs)
    except Exception as e:
        print(traceback.format_exc())

start()
