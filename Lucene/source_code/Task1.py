import re
from glob import glob
import operator
import os
from bs4 import BeautifulSoup
import traceback

CURRENT_DIRECTORY = os.getcwd()
INPUT_FOLDER = path = os.path.join(CURRENT_DIRECTORY,'downloaded_docs')
OUTPUT_FOLDER_PATH = path = os.path.join(CURRENT_DIRECTORY,'generated_corpus')

def leftstrip(word):
    while(word[:1] == "-" or word[:1] == "." or word[:1] == ","):
        num_format = re.compile("^[\-]?[0-9]*\.?[0-9]+$")
        isnumber = re.match(num_format,word)
        if isnumber:
            break
        elif word[:1] == "-" or word[:1] == "." or word[:1] == ",":
            word = word[1:]
        else:
            break
    return word

def strippunc(word):
    if ((word[((len(word)) - 1):(len(word))] == ",") or (word[((len(word)) - 1):(len(word))] == ".") or (word[((len(word)) - 1):(len(word))] == "-")):
        word = word[:(len(word)-1)]
    else:
        word
    return leftstrip(word)


def process_files():
    file_to_terms = {}
    urls={}
    try:
        counter=1
        num_of_files = len(glob(os.path.join(INPUT_FOLDER,'*.txt')))
        for file in glob(os.path.join(INPUT_FOLDER,'*.txt')):
            perc = float((counter/float(num_of_files)))*100
            print "Processing %s - Completed %r%%" %(file[(file.rindex('\\'))+1:],round(perc,2))
            url = open(file,'r').readline()
            urls.update({file:url})
            file_to_terms[file] = open(file, 'r').read().lower()
            content = file_to_terms[file]
            if (content.find('<span class="mw-headline" id="see_also">')!=-1):
                content=content[:content.index('<span class="mw-headline" id="see_also">')]
            elif (content.find('<span class="mw-headline" id="references">')!=-1):
                content=content[:content.index('<span class="mw-headline" id="references">')]
            if (content.find('<div class="toc" id="toc">')!=-1):
                first_content=content[:content.index('<div class="toc" id="toc">')]
                second_content=content[content.find('</div>', (content.find('</div>',(content.index('<div class="toc" id="toc">') + 1)) + 1)):]
                content = first_content+second_content
            soup = BeautifulSoup(content, "html.parser")
            soup.prettify().encode("utf-8")
            data = soup.findAll('div', attrs={'id':'bodycontent'})
            body=""
            for div in data:
                body+=div.get_text().encode("utf-8")
            title_text = soup.find('title').get_text().encode("utf-8")
            main_header = soup.find('h1').get_text().encode("utf-8")
            total_text = title_text + main_header + body #Appending title, header and body of the htmls.
            file_to_terms[file] = total_text
            pattern = re.compile('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']')
            file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
            file_to_terms[file] = file_to_terms[file].split()
            temp_list = []
            for terms in file_to_terms[file]: #Stripping of the characters which needs to be handled specially
                temp_list.append(strippunc(terms))
            while '' in temp_list:   #Removing empty strings
                del temp_list[temp_list.index('')]
            file_to_terms[file] = temp_list
            counter+=1
    except Exception as e:
        print(traceback.format_exc())
    return file_to_terms,urls



def write_files():
    try:
        LINK_FILENAME=[]
        counter=1
        file_to_terms,urls = process_files()
        for term_file in file_to_terms.keys():
            article_id = (urls[term_file].split("/wiki/")[1])
            file_name=re.sub(r'[\W]*-*_*', '', article_id)
            if file_name not in LINK_FILENAME:
                LINK_FILENAME.append(file_name)
            else:
                while(file_name in LINK_FILENAME):
                    file_name = file_name+str(counter)
                    counter = counter + 1
                LINK_FILENAME.append(file_name)
            out_file  = open(OUTPUT_FOLDER_PATH+"\\"+file_name+".txt",'w')
            tokens=" ".join(file_to_terms[term_file]) #Coverting a list to string with spaces as delimiters
            out_file.write(tokens)
            out_file.close()
    except Exception as e:
        print(traceback.format_exc())


write_files()
