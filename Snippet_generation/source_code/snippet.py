import traceback
from os.path import exists
import os
import operator
from bs4 import BeautifulSoup
from colorama import *

CURRENT_DIRECTORY = os.getcwd()
CACM = path = os.path.join(CURRENT_DIRECTORY,'cacm')
DOC_SCORE_PATH = path = os.path.join(CURRENT_DIRECTORY,'doc_score')

def processed_query(unprocessed_query):
    try:
        temp_list = []
        query = unprocessed_query[unprocessed_query.find('</DOCNO>')+8:unprocessed_query.find('</DOC>')]
        query = query.strip()
        temp_list = query.split()
        query = " ".join(temp_list)
        unprocessed_query = unprocessed_query[unprocessed_query.find('</DOC>')+6:]
        return unprocessed_query,query
    except Exception as e:
        print(traceback.format_exc())


def processing_query():
    try:
        if exists(CURRENT_DIRECTORY+"\\unprocessed_query.txt"):
            os.remove(CURRENT_DIRECTORY+"\\unprocessed_query.txt")
        unprocessed_query = open(CURRENT_DIRECTORY+"\\cacm.query",'r').read()
        query_file = open(CURRENT_DIRECTORY+"\\unprocessed_query.txt",'a')
        while unprocessed_query.find('<DOC>')!=-1:
            unprocessed_query, query = processed_query(unprocessed_query)
            if(unprocessed_query.find('<DOC>')==-1):
                query_file.write(query)
            else:
                query_file.write(query+"\n")
    except Exception as e:
        print(traceback.format_exc())

def generate_snippet_with_trigrams(term_list,file_name):
    try:
        lookahead = 40
        posttail = 50
        content = open(CACM+"\\"+file_name+".html",'r').read()
        soup = BeautifulSoup(content, "html.parser")
        soup.prettify().encode("utf-8")
        given_file = soup.find('pre').get_text().encode("utf-8")
        for i in range(len(term_list) - 2):
            term = term_list[i]+" "+term_list[i+1]+" "+term_list[i+2]
            if(given_file.find(term)!=-1):
                start_index = max(given_file.index(term)-lookahead, 0)
                if start_index!=0:
                    while start_index > 0:
                        if given_file[(start_index-1):start_index] not in [" ","\n"]:
                            start_index-=1
                        else:
                            break
                sum = given_file.index(term) +  len(term) + posttail
                end_index = min(sum, len(given_file))
                if end_index!=len(given_file):
                    while end_index < len(given_file):
                        if given_file[end_index:(end_index+1)] not in [" ","\n"]:
                            end_index+=1
                        else:
                            break
                first = given_file[start_index:given_file.index(term)]
                second = given_file[given_file.index(term):(given_file.index(term)+len(term))]
                third = given_file[(given_file.index(term)+len(term)):end_index]
                return first, second, third
        return False, False, False
    except Exception as e:
        print(traceback.format_exc())

def generate_snippet_with_bigrams(term_list,file_name):
    try:
        lookahead = 40
        posttail = 50
        content = open(CACM+"\\"+file_name+".html",'r').read()
        soup = BeautifulSoup(content, "html.parser")
        soup.prettify().encode("utf-8")
        given_file = soup.find('pre').get_text().encode("utf-8")
        for i in range(len(term_list) - 1):
            term = term_list[i]+" "+term_list[i+1]
            if(given_file.find(term)!=-1):
                start_index = max(given_file.index(term)-lookahead, 0)
                if start_index!=0:
                    while start_index > 0:
                        if given_file[(start_index-1):start_index] not in [" ","\n"]:
                            start_index-=1
                        else:
                            break
                sum = given_file.index(term) +  len(term) + posttail
                end_index = min(sum, len(given_file))
                if end_index!=len(given_file):
                    while end_index < len(given_file):
                        if given_file[end_index:(end_index+1)] not in [" ","\n"]:
                            end_index+=1
                        else:
                            break
                first = given_file[start_index:given_file.index(term)]
                second = given_file[given_file.index(term):(given_file.index(term)+len(term))]
                third = given_file[(given_file.index(term)+len(term)):end_index]
                return first, second, third
        return False, False, False
    except Exception as e:
        print(traceback.format_exc())

def generate_snippet_with_unigram(term_list,file_name):
    try:
        lookahead = 40
        posttail = 50
        content = open(CACM+"\\"+file_name+".html",'r').read()
        soup = BeautifulSoup(content, "html.parser")
        soup.prettify().encode("utf-8")
        given_file = soup.find('pre').get_text().encode("utf-8")
        for term in term_list:
            if(given_file.find(term)!=-1):
                start_index = max(given_file.index(term)-lookahead, 0)
                if start_index!=0:
                    while start_index > 0:
                        if given_file[(start_index-1):start_index] not in [" ","\n"]:
                            start_index-=1
                        else:
                            break
                sum = given_file.index(term) +  len(term) + posttail
                end_index = min(sum, len(given_file))
                if end_index!=len(given_file):
                    while end_index < len(given_file):
                        if given_file[end_index:(end_index+1)] not in [" ","\n"]:
                            end_index+=1
                        else:
                            break
                first = given_file[start_index:given_file.index(term)]
                second = given_file[given_file.index(term):(given_file.index(term)+len(term))]
                third = given_file[(given_file.index(term)+len(term)):end_index]
                return first, second, third
        return False, False, False
    except Exception as e:
        print(traceback.format_exc())


def generate_snippet(query,file_name):
    try:
        term_list = query.split()
        if len(term_list) > 2:
            first, second, third = generate_snippet_with_trigrams(term_list,file_name)
            if first != False:
                print "\t"+file_name
                print first+" "+"\033[44;33m"+second+"\033[m"+" "+third
            else:
                first, second, third = generate_snippet_with_bigrams(term_list,file_name)
                if first != False:
                    print "\t"+file_name
                    print first+" "+"\033[44;33m"+second+"\033[m"+" "+third
                else:
                    first, second, third = generate_snippet_with_unigram(term_list,file_name)
                    if first != False:
                        print "\t"+file_name
                        print first+" "+"\033[44;33m"+second+"\033[m"+" "+third
                    else:
                        print"no query term found in " + file_name
        elif len(term_list) > 1:
            first, second, third = generate_snippet_with_bigrams(term_list,file_name)
            if first != False:
                print "\t"+file_name
                print first+" "+"\033[44;33m"+second+"\033[m"+" "+third
            else:
                first, second, third = generate_snippet_with_unigram(term_list,file_name)
                if first != False:
                    print "\t"+file_name
                    print first+" "+"\033[44;33m"+second+"\033[m"+" "+third
                else:
                    print"no query term found in " + file_name
        else:
            first, second, third = generate_snippet_with_unigram(term_list,file_name)
            if first != False:
                print "\t"+file_name
                print first+" "+"\033[44;33m"+second+"\033[m"+" "+third
            else:
                print"no query term found in " + file_name
    except Exception as e:
        print(traceback.format_exc())

def get_list_of_files(query_id):
    try:
        file_list = []
        doc_score_file = open(DOC_SCORE_PATH+"\\BM25_doc_score.txt")
        for line in doc_score_file.readlines():
            params = line.split()
            if params[0] == str(query_id):
                file_list.append(params[2])
        doc_score_file.close()
        return file_list
    except Exception as e:
        print(traceback.format_exc())

def snippet_generation():
    try:
        init()
        processing_query()
        query_id = 0
        semi_processed_file = open('unprocessed_query.txt','r')
        for query in semi_processed_file.readlines():
            query_id+=1
            list_of_files = get_list_of_files(query_id)
            for file_name in list_of_files:                
                generate_snippet(query,file_name)
    except Exception as e:
        print(traceback.format_exc())
snippet_generation()
