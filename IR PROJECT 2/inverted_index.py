from collections import Counter
import sys

class Node:

    # constructor for initializing Node
    def __init__(self,docid,tfreq):
        self._docid = docid
        self._tfreq = tfreq
        self._nextnode = None

    def __str__(self):
        return 'docid: {}, termFrequency: {}'.format(self._docid, self._tfreq)
    def __repr__(self):
        return 'docid: {}'.format(self._docid)

    # function to get data present in the Node
    def get_data(self):
        return self._docid, self._tfreq

    # function to go to the next node present in the Node
    def get_next(self):
        return self._nextnode

    # function to set the pointer to next Node
    def set_next(self, nextnode):
        self._nextnode = nextnode

class LinkedList:

    # constructor to initialize the linked list
    def __init__(self):
        self._head = None
        self._tail = None

    # function to insert a new Node with data(docid,tfreq)
    def insert(self, docid, tfreq):
        new_node = Node(docid,tfreq)

        # if first Node, set head and tail to that Node
        if self._head == None:
            self._head = new_node
            self._tail = new_node
        # else set tail to next Node and make the new Node as tail
        else:
            self._tail.set_next(new_node)
            self._tail = new_node

    # function to traverse through a list
    def traverse(self):
        # if head is None, then list is empty
        if self._head == None:
            print("empty!")
        # else get head
        else:
            h = self._head
            # while head exits (traverse till end of list), print data and shift head to next node
            while h:
                print(h.get_data(),'-->', end=" ")
                h = h.get_next()

    # function to get postings (docid,tfreq)
    def postings(self):
        postings = []
        if self._head == None:
            print("empty")
        else:
            h = self._head
            while h:
                postings.append(h.get_data())
                h = h.get_next()
        return postings


    def __str__(self):
        return self._head.get_data()
    def __repr__(self):
        return '{}'.format(self._head.get_data())

# start of program
# read command line arguments
if len(sys.argv) != 4:
    print("FAILURE: No argument!")
    print("Enter <corpus_path> <output_file_path> <input_file_path>")
    sys.exit(1)  # abort because of error
else:
    input_corpus = str(sys.argv[1])
    output_file_path = str(sys.argv[2])
    input_file_path = str(sys.argv[3])
    print("Corpus file:\t", input_corpus)
    print("Output file:\t", output_file_path)
    print("Input file:\t", input_file_path)


# read file and split docids and sentences
with open(input_corpus, "r") as f:
    doc_list = [content.split('\t') for content in f.read().split("\n") if content != '']

index = []
inverted_index = {}
print(len(doc_list))
# for each doc split doc and terms in a sentence and count total terms in the doc
for doc in doc_list:
    index.append([doc[0],doc[1].split(' '),len(doc[1].split(' '))])

# sort the index increasing order docids
index = sorted(index)
total_num_of_docs = len(doc_list)

# for each doc in index, count the number of terms, for each term, create a Node of docids,tfreq and hence create a list
"""
doc has ['1078', ['I', 'could', 'not', 'such', 'words', .... , 'guise.'], 22]
term_counter has Counter({'I': 2, 'could': 1, 'not': 1, 'such': 1, 'words': 1, ...., 'guise.': 1})
"""
for doc in index:
    term_counter = Counter(doc[1])
    for term, tfreq in term_counter.items():
        if term not in inverted_index:
            # initialize linked list
            inverted_index[term] = {'docids': LinkedList(), 'dfreq': 0}
        # calculate term frequency
        tfreq = tfreq/doc[2]
        # insert Node
        inverted_index[term]['docids'].insert(doc[0],tfreq)
        # increase dfreq counter by 1
        inverted_index[term]['dfreq'] = inverted_index[term].get('dfreq') + 1


# function to get the query terms
def get_query_terms(the_query):
    # query of which postings need to be listed
    the_query = the_query

    # split the query into query terms
    query_terms = the_query.split(' ')
    return query_terms

# function to write postings into a file
def write_postings_tofile():
    for i in range(len(query_terms)):
        f.write("GetPostings\n")
        f.write("%s\n" % (query_terms[i]))
        f.write("Postings list: ")
        # Posting list has the fomat print(postings[i][0])
        # Writng posting list of each query in a file
        f.write("%s\n" % (' '.join(j[0] for j in postings[i][0])))

# function to calculate tfidf
def get_tfidf(df,tf,total_docs):

    df = df
    tf = tf
    total_docs = total_docs
    idf = total_docs/df
    tfidf = tf*idf
    return tfidf


# function to perform DaatAnd
def perform_DaatAnd():

    and_first_postings = sorted_postings[0]
    and_noc = 0 # number of comparisons
    and_result = []
    and_index = [0] * len(sorted_postings)
    for i in range(len(and_first_postings[0])):
        and_all_tfidfs = []
        # get df of first posting
        and_df_firstposting = and_first_postings[1]
        flag = 0
        for j in range(1,len(sorted_postings)):
            # get df of second posting
            and_df_secondposting = sorted_postings[j][1]
            for k in range(and_index[j],len(sorted_postings[j][0])):
                if and_first_postings[0][i][0] > sorted_postings[j][0][k][0]:
                    # print("docid {} > docid {}".format(and_first_postings[0][i][0],sorted_postings[j][0][k][0]))
                    and_noc += 1
                elif and_first_postings[0][i][0] < sorted_postings[j][0][k][0]:
                    # print("docid {} < docid {}".format(and_first_postings[0][i][0],sorted_postings[j][0][k][0]))
                    and_index[j] = k
                    and_noc += 1
                    break
                else:
                    # print("docid {} = docid {}".format(and_first_postings[0][i][0],sorted_postings[j][0][k][0]))
                    and_index[j] = k+1
                    and_noc += 1
                    flag += 1
                    and_tfidf_secondposting = get_tfidf(and_df_secondposting,sorted_postings[j][0][k][1],total_num_of_docs)
                    and_all_tfidfs.append(and_tfidf_secondposting)
                    break
            if flag == len(sorted_postings)-1:
                print("************************")
                print("Found docid {} in all {} postings".format(and_first_postings[0][i][0],flag+1))
                print("************************")
                # append tfidf of first posting
                and_tfidf_firstposting = get_tfidf(and_df_firstposting,and_first_postings[0][i][1],total_num_of_docs)
                and_all_tfidfs.append(and_tfidf_firstposting)
                print("all_tfidfs = ", and_all_tfidfs)
                and_sum_tfidfs = sum(and_all_tfidfs)
                print("sum_tfidfs = ",and_sum_tfidfs)
                result_list = list(and_first_postings[0][i])
                result_list[1] = and_sum_tfidfs
                and_result.append(result_list)
    print("Number of comparisions: ",and_noc)
    print("DAAT-AND",and_result)
    return and_noc, and_result

# function to write DaatAnd results into a file
def write_DaatAnd_tofile(and_noc,and_result):
        f.write("DaatAnd\n")
        f.write("%s\n" % (' '.join(qterm for qterm in query_terms)))
        if and_result == []:
            f.write("Results: empty\n")
        else:
            f.write("Results: %s\n" % (' '.join(r[0] for r in and_result)))

        f.write("Number of documents in results: %s\n" % (len(and_result)))
        f.write("Number of comparisons: %s\n" % (and_noc))

        # TF-IDF
        f.write("TF-IDF\n")
        and_result = sorted(and_result, key= lambda x: x[1], reverse = True)
        if and_result == []:
            f.write("Results: empty\n")
        else:
            f.write("Results: %s\n" % (' '.join(r[0] for r in and_result)))

# function to perform DaatOr
def perform_DaatOr():
    or_first_postings = reverse_sorted_postings[0]
    or_noc = 0 # number of comparisons
    or_result = []
    or_index = [0] * len(reverse_sorted_postings)
    or_all_tfids = {}
    for a in range(len(or_first_postings[0])):
        # get df of first posting
        or_df_firstposting = or_first_postings[1]
        equal_flag = 0
        for b in range(1,len(reverse_sorted_postings)):
            # get df of second posting
            or_df_secondposting = reverse_sorted_postings[b][1]
            # print(or_df_secondposting)
            for c in range(or_index[b],len(reverse_sorted_postings[b][0])):
                or_noc += 1
                if or_first_postings[0][a][0] > reverse_sorted_postings[b][0][c][0]:
                    print("docid {} > docid {}".format(or_first_postings[0][a][0],reverse_sorted_postings[b][0][c][0]))
                    or_index[b] = c+1
                    or_tfidf_secondposting = get_tfidf(or_df_secondposting,reverse_sorted_postings[b][0][c][1],total_num_of_docs)
                    if reverse_sorted_postings[b][0][c][0] not in or_all_tfids:
                        # add tfidf into the dictionary
                        or_all_tfids[reverse_sorted_postings[b][0][c][0]] = or_tfidf_secondposting
                        print("\n")
                    else:
                        # update tfidf in the dictionary
                        or_all_tfids[reverse_sorted_postings[b][0][c][0]] = or_all_tfids.get(reverse_sorted_postings[b][0][c][0]) + or_tfidf_secondposting
                        print("\n")
                        break

                elif or_first_postings[0][a][0] < reverse_sorted_postings[b][0][c][0]:
                    print("docid {} < docid {}".format(or_first_postings[0][a][0],reverse_sorted_postings[b][0][c][0]))
                    break

                else:
                    print("docid {} = docid {}".format(or_first_postings[0][a][0],reverse_sorted_postings[b][0][c][0]))
                    or_index[b] = c+1
                    equal_flag = 1
                    or_tfidf_secondposting = get_tfidf(or_df_secondposting,reverse_sorted_postings[b][0][c][1],total_num_of_docs)
                    if reverse_sorted_postings[b][0][c][0] not in or_all_tfids:
                        or_all_tfids[reverse_sorted_postings[b][0][c][0]] = or_tfidf_secondposting
                        print("\n")
                        break
                    else:
                        or_all_tfids[reverse_sorted_postings[b][0][c][0]] = or_all_tfids.get(reverse_sorted_postings[b][0][c][0]) + or_tfidf_secondposting
                        print("\n")
                        break

        # print (or_first_postings[0][a][0])
        or_all_tfids[or_first_postings[0][a][0]] = or_all_tfids.get(or_first_postings[0][a][0], 0) + get_tfidf(or_df_firstposting,or_first_postings[0][a][1],total_num_of_docs)

    print("Number of comparisions: ",or_noc)
    print("----------------------------------------------------------------------------------------")

    # all comparisons done, including all the left-over postings from each list
    for v in range(len(reverse_sorted_postings)):
        for u in reverse_sorted_postings[v][0]:
            if u[0] not in or_all_tfids:
                or_tfidf_secondposting = get_tfidf(reverse_sorted_postings[v][1],u[1],total_num_of_docs)
                or_all_tfids[u[0]] = or_tfidf_secondposting
                print("{} Inserted!".format(u[0]))

    # converting dict to list
    for key,value in or_all_tfids.items():
        temp = [key,value]
        or_result.append(temp)
    print("\n\n")
    print("DAAT-OR",or_result)
    print("TF-IDF",sorted(or_result, key = lambda t:t[1], reverse=True))
    return or_noc, or_result


def write_DaatOr_tofile(or_noc,or_result):
        f.write("DaatOr\n")
        f.write("%s\n" % (' '.join(qterm for qterm in query_terms)))
        or_result = sorted(or_result, key = lambda x: x[0])
        if or_result == []:
            f.write("Results: empty\n")
        else:
            f.write("Results: %s\n" % (' '.join(r[0] for r in or_result)))

        f.write("Number of documents in results: %s\n" % (len(or_result)))
        f.write("Number of comparisons: %s\n" % (or_noc))

        # TF-IDF
        f.write("TF-IDF\n")
        or_result = sorted(or_result, key= lambda x: x[1], reverse = True)
        if or_result == []:
            f.write("Results: empty\n")
        else:
            f.write("Results: %s\n" % (' '.join(r[0] for r in or_result)))


# open input file and get list of queries
with open(input_file_path,"r") as f:
    query_list = [line for line in f.read().split("\n") if line != '']

with open(output_file_path, "w+") as f:

    # perform operations for each query
    for q in query_list:
        query_terms = get_query_terms(q)
        # print(query_terms)
        postings = []
        sorted_postings = []
        for qterm in query_terms:
            postings.append([inverted_index[qterm]['docids'].postings(),inverted_index[qterm]['dfreq']])
        # print(postings)

        sorted_postings = sorted(postings, key = lambda x: x[1])
        # print(sorted_postings)

        write_postings_tofile()

        print("---------------------------------------")
        print("--------------DAAT-AND-----------------")
        print("---------------------------------------")

        and_noc, and_result = perform_DaatAnd()
        write_DaatAnd_tofile(and_noc, and_result)

        print("---------------------------------------")
        print("---------------DAAT-OR-----------------")
        print("---------------------------------------")
        reverse_sorted_postings = sorted(postings, key = lambda y: y[1], reverse = True)
        # print(reverse_sorted_postings)

        or_noc, or_result = perform_DaatOr()
        write_DaatOr_tofile(or_noc,or_result)
        x = f.tell()
        f.write("\n")
    f.truncate(f.seek(x))    
    #f.truncate(f.tell()-1)
