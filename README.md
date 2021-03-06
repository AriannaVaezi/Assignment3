# Assignment3

Search engine:

Part 1: Creating the index.
  First goes through all the files and creates the mulipart index in the for term: posting.
    The posting includes the id, the number of times the posting appears, and if the posting is an important word
  Then combines all the smaller indicies into one larger text file index, in which each line contains a list of postings.
    The word and the location in the index of the word is saved in a txt file.
  Then it creates a faster index by sorting sorting and cutting down the posting list.
     Again, the word and the location in the index of the word is saved in a txt file.
  Then the words and locations are combined into a json file, creating the index index.
  Finally, the ids and the urls saved in a json file.
  
  When the program is run, index_creater(), index_merger(), index_optimizer(), indexindex_creater(), and id_index_creater() are called in that order.
  
Part 2: Searching
  First the id and index of the index are loaded.
  Then the user imputs a query and a list of all the terms is returned.
  The that query is put through the search functions where a list of queue is returned
    single_search is the fastest process for a query with a single word
    double_search is the next fastest for a query with two words
    multi_search is for queries with more than two words
  Finally, the first 5 results from the list or queue is printed.
  
  When the program is run, take_query_input(), and the search function are called.
    
    
