import json
from bs4 import BeautifulSoup
import os
import sys
import re
import math
from collections import defaultdict
import nltk
from nltk.stem.porter import PorterStemmer #information on how to use this lirbrary found at https://www.tutorialspoint.com/python_data_science/python_stemming_and_lemmatization.htm 


def parse_title(query: str) -> list:
    'Parses the title of a document'
    query_tokens = list()
    nltk_tokens =  nltk.word_tokenize(query)
    porter_stemmer = PorterStemmer()
    for w in nltk_tokens:
        if not re.match(r'^(\W|_)$', w):
            w = re.sub(r'^[\W_]+|[\W_]+$', '', w).lower()
            query_tokens.append(porter_stemmer.stem(w))
    return set(query_tokens)


def index_creater() -> int:
    'Creates the inital index in parts'
    index = defaultdict(list) # in memory index
    id_number = 1 # ID number
    index_number = 1 # number of small indexes created
    with open('id.txt', 'a') as f:


        # going through all the files in dev
        for root, dirs, files in os.walk('DEV'):
            for name in files:

                # Keeping track of which ID corresponds to which document
                path = os.path.join(root, name)
                with open('id.txt', 'a') as g:
                        g.write(f'{path}\n')
                
                if os.path.getsize(path) > 2000000: 
                    id_number +=1
                    continue # Making sure files aren't too big to read

                with open(path) as f:
                    # Getting the tokens
                    data = json.load(f)
                    soup = BeautifulSoup(data['content'], features="html.parser")
                    porter_stemmer = PorterStemmer()
                    nltk_tokens =  nltk.word_tokenize(soup.get_text())

                    # Getting the title
                    title_text = set()
                    for title in soup.find_all('title'):
                        title_text = title_text.union(parse_title(title.get_text()))
                    
                    # Keeping track of the amount of times a token appears and the location of the tokens
                    tokens_num = defaultdict(int)
                    tokens_loc = defaultdict(list)


                    for i in range(len(nltk_tokens)):
                        if not re.match(r'^(\W|_)$', nltk_tokens[i]):
                            w = re.sub(r'^[\W_]+|[\W_]+$', '', nltk_tokens[i]).lower()
                            tokens_num[porter_stemmer.stem(w)] += 1
                            tokens_loc[porter_stemmer.stem(w)].append(i)


                    # Appending the posting to the index
                    # posting : (id_number : int, number of times token appears : int, is token important : bool)
                    for token in tokens_num.keys():
                        index[token].append((id_number, tokens_num[token], token in title_text))
                    
                    #if sys.getsizeof(index) > 20000000:
                    if id_number % 18465 == 0:
                        with open(f'index{str(index_number)}.json', 'w') as f:
                            json.dump(index, f)
                            index_number += 1
                            index = defaultdict(list)

                id_number +=1

    with open(f'index{str(index_number)}.json', 'w') as f:
        json.dump(index, f)
        index_number += 1
        index = defaultdict(list)

    return index_number


def index_merger():
    ' Merges the indicies'

    index_index = dict()

    with open('index1.json') as f:
        index1 = json.load(f)
    with open('index2.json') as f:
        index2 = json.load(f)
    with open('index3.json') as f:
        index3 = json.load(f)

    position = 0
    for term in index1.keys():
        termlist = index1[term]
        if term in index2: termlist += index2[term]
        if term in index3: termlist += index3[term]
        index_tuple = tuple((position, len(termlist)))
        with open('terms.txt','a') as f:
            try:
                f.write(f'{term}\n')
            except:
                f.write('\n')
        with open('tuples.txt','a') as f:
            f.write(f'{index_tuple}\n')

        index_index[term] = (index_tuple)

        with open('index.txt', 'a') as f:
            f.write(f'{termlist}\n')
            position = f.tell()

    for term in index2.keys():
        if term not in index_index: termlist = index2[term]
        if term in index3: termlist += index3[term]
        index_tuple = tuple((position, len(termlist)))


        with open('terms.txt','a') as f:
            try:
                f.write(f'{term}\n')
            except:
                f.write('\n')
        with open('tuples.txt','a') as f:
            f.write(f'{index_tuple}\n')
        index_index[term] = (index_tuple)

        with open('index.txt', 'a') as f:
            f.write(f'{termlist}\n')
            position = f.tell()
    
    for term in index3.keys():
        if term not in index_index: termlist = index3[term]
        index_tuple = tuple((position, len(termlist)))

        with open('terms.txt','a') as f:
            try:
                f.write(f'{term}\n')
            except:
                f.write('\n')
        with open('tuples.txt','a') as f:
            f.write(f'{index_tuple}\n')

        index_index[term] = (index_tuple)

        with open('index.txt', 'a') as f:
            f.write(f'{termlist}\n')
            position = f.tell()

    with open('indexindex.json', 'w') as f:
        json.dump(index_index,f)

def indexindex_creater():
    'Creates an index for the index'
    index_index = dict()
    with open('terms.txt') as f:
        with open('fasttuples.txt') as g:
            for line in f:
                term = str(line.strip())
                tup = eval(str(g.readline()).strip())
                print(term,tup)
                if term not in index_index:
                    index_index[term] = tup
    with open('fastindexx.json', 'w') as f:
        json.dump(index_index, f)

def index_optimizer():
    ' Creates a sorted, faster index'
    position = 0
    with open('index.txt') as f:
        for line in f:
            postings = eval(line.strip())
            for posting in postings:
                posting[1] = round((1 + math.log(posting[1]) * math.log(float(55393)/len(postings))), 3)
            postings = sorted(postings, key = lambda t: (-int(t[2]), -t[1], t[0]))[:100]
            with open('fasttuples.txt', 'a') as f:
                f.write(f'{(position, len(postings))}\n')
            with open('fastindex.txt', 'a') as f:
                f.write(f'{postings}\n')
                position = f.tell()
            
def id_index_creator():
    'Creates a dictionary for all the ids'
    id_dict = dict()
    with open('id.txt') as f:
        num = 1
        for line in f:
            with open(line.strip()) as g:
                jsn = json.load(g)
                id_dict[num] = jsn['url']
            num+= 1
    with open('ids.json', 'w') as f:
        json.dump(id_dict, f)




if __name__ == '__main__':

    index_number = index_creater() # Creates the index
    index_merger() # merges index
    index_optimizer() #optimizes merged index
    indexindex_creater() # creates the index for the index
    id_index_creator() # creates the dict of ids
