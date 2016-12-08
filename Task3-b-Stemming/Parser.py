import os
from os.path import exists
CURRENT_DIRECTORY = os.getcwd()
INPUT_FOLDER = path = os.path.join(CURRENT_DIRECTORY,'generated_corpus')
page = open("cacm_stem.txt").read()

start_link = page.find('#')
while start_link != -1:
    doc_id = page[start_link + 2: page.find("\n",start_link + 2)]
    print doc_id
    end_link = page.find('#',page.find("\n",start_link + 2))
    contents = page[start_link + 2 : end_link]
    if len(doc_id) == 1:
        output_filename = "CACM-000" + doc_id
    if len(doc_id) == 2:
        output_filename = "CACM-00" + doc_id
    if len(doc_id) == 3:
        output_filename = "CACM-0" + doc_id
    if len(doc_id) == 4:
        output_filename = "CACM-" + doc_id
    print output_filename 
    output_file = open(INPUT_FOLDER+"\\"+output_filename+".txt",'w')
    output_file.write(contents)
    start_link = page.find('#',end_link)

query_file = open("cacm_stem.query.txt").read()
output_file = open("query.txt",'w')
output_file.write(query_file)
