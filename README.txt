Final Project:
Goal: Design and build your information retrieval systems, evaluate and compare their performance levels in terms of retrieval effectiveness
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

SYNOPSIS:

This readme file has references and detailed information regarding how to setup, compile and run the programs in the assignment.
The progrms are discussed below in brief:
-- Task1: Building our own search engines with Cosine Similarity, BM25, tf-idf and Lucene model.
-- Task2: Implementing pseudo-relevance feedback for query expansion on one of the above mentioned models.
-- Task3: Using the same base search engine, implementing stopping and stemming seperately.
-- Phase2: Evaluation in form of MAP, MRR, P@K for k=5 and 20, Precision and Recall.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

GENERAL USAGE NOTES:

-- This file contains instructions about installing softwares and running the programs in Windows Environment.
-- The instructions in the file might not match the installation procedures in other operating systems like Mac OS, Ubuntu OS etc.
-- However, the programs are independent of any operating systems and will run successfully in all platforms once the initial installation has been done. 

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

INSTALLATION GUIDE:

-- Download python 2.7.x from https://www.python.org/download/releases/2.7/
-- From Windows Home go to Control Panel -> System and Security -> System -> Advanced System Settings -> Environment Variables and add two new variables in 'PATH' -> [Home directory of Python]; [Home directory of Python]\Scripts
-- Open Command Prompt and upgrade pip using the following command: 'python -m pip install -U pip'
-- To check whether you have pip installed properly, just open the command prompt and type 'pip'
-- It should not throw an error, rather details regarding pip will be displayed.
-- Install BeautifulSoup by using the command 'pip install beautifulsoup4'
-- If for some reason the installation fails due to the absence of certain package, just install that package using 'pip install name_of_that_package'
-- Install Colorama by downloading colorama-0.3.7.zip file from https://pypi.python.org/pypi/colorama#downloads
-- Open the unzipped folder and open a command prompt in that location and write the given command - 'C:\Python27\python.exe setup.py install'

-- Install JAVA SE6 or above if not already installed in the system from http://www.oracle.com/technetwork/java/javase/index-137561.html#windows
-- From Windows Home go to Control Panel -> System and Security -> System -> Advanced System Settings -> Environment Variables and add new variable in 'PATH' -> [Home directory of Java]\jdk[version number]\bin;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

GENERAL INSTRUCTIONS:

-- Please maintain the folder and file structure inside 'source_code' folder for each of the models, as it is very important for the the codes of both the tasks to work.
-- Each search model folder contains a sub-folder 'cacm'. This folder contains the 3204 raw documents provided for this project :-
	-- Run the python file 'Parser.py' by using the command 'python Parser.py' in windows powershell or command prompt
	-- The corpus will be generated from the cacm documents present in 'cacm' and be stored in 'generated_corpus' document wise. And a processed query file named 'query.txt' will be generated from the raw query file 'cacm.query' in the source_code folder structure itself.
-- Once the Parser.py has parsed all the raw documents, run 'index_generator.py' by using the command 'python index_generator.py' in windows powershell or command prompt.
-- Once the index_generator.py has been run, a model respective doc score would be generated inside the 'doc_score' folder.
-- Copy and paste these respective doc score txts inside Evaluation folder to get the desired evaluation results of the doc score of the search model.
-- Run 'Evaluation.py'
-- The code for Lucene implementation is provided in 'source_code' folder of Lucene along with all the jars needed for the code to run inside folder 'java_jars'
-- Lucene.jar is the runnable jar of the given code which can work independently from a command prompt and doesn't need any IDE setup or dependency on the jars. One can run this executable jar by running the given command in a command prompt 'java -jar Lucene.jar'



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

CONTRIBUTORS and CITATIONS:

-- https://lucene.apache.org/core/4_0_0/core/org/apache/lucene/search/similarities/TFIDFSimilarity.html - TFIDFSimilarity using Lucene Model.
-- https://www.udacity.com/course/intro-to-computer-science--cs101 : Basics of Python Programming
-- https://learnpythonthehardway.org/book/ : Python Programming
-- http://nlp.stanford.edu/IR-book/html/htmledition/dropping-common-terms-stop-words-1.html : For stop words.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

CONTACT DETAILS:

The author of the README can be contacted via:
Phone: (+1) 6173725107
E-Mail: pyne.r@husky.neu.edu