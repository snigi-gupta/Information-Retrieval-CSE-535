# -*- coding: utf-8 -*-


import json
# if you are using python 3, you should
import urllib.request
# import urllib2
from googletrans import Translator
import re
from urllib.parse import quote
translator = Translator()

lang = ['en', 'de', 'ru']

# change the url according to your own corename and query
# inurl = 'http://localhost:8983/solr/corename/select?q=*%3A*&fl=id%2Cscore&wt=json&indent=true&rows=1000'
infn = 'test_queries.txt'
outfn = 'test_lmoutput_2.txt'


# change query id and IRModel name accordingly
qid = ''
IRModel='default'


def parser():
    query_list = []
    with open(infn, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    for line in all_lines:
        q_en = ""
        q_ru = ""
        q_de = ""

        # removing newline character from each line
        line.replace("\n", "")

        # split line into query id and query
        qid = line[:3]
        query = line[4:-1]

        # Get language of the query using Translator from googletrans library
        q_lang = translator.detect([query])[0].lang
        print("Q: {} ---- QID: {} ---- Language: {}".format(query, qid, q_lang))

        # using translated json
        with open("query.json", "r", encoding="utf-8") as f:
            all_queries = json.load(f)
            # print(all_queries)
            for q in all_queries:
                q_lang = q['lang']
                if q_lang == "en":
                    q_en = query
                if q_lang == "de":
                    q_de = query
                if q_lang == "ru":
                    q_ru = query

        # Transalate the queries into other languages
        for l in lang:
            if l != q_lang:
                trans_lang = translator.translate(query, dest=l).text
                if l == "en":
                    q_en = trans_lang
                if l == "de":
                    q_de = trans_lang
                if l == "ru":
                    q_ru = trans_lang

        query_dict = {"qid": qid, "text": query, "lang": q_lang, "text_en": q_en, "text_de": q_de, "text_ru": q_ru}
        # print(query_dict)
        query_list.append(query_dict)
    print(query_list)

    with open("query.json", 'w', encoding="utf-8") as f:
        json.dump(query_list, f, ensure_ascii=False)
    print("Parsing Done!")


def solr():

    core_name = "core2_lm"
    # localhost = "http://ec2-13-58-105-74.us-east-2.compute.amazonaws.com:8983/solr/"
    localhost = "http://52.15.182.115:8983/solr/"
    select_q = "/select?q="
    fl_score = "&fl=id%2Cscore&wt=json&indent=true&rows=20"
    inurl = ""

    with open("test_queries.txt", "r", encoding="utf-8") as f:
        all_queries = f.readlines()
    outf = open(outfn, "a+")
    outf.truncate(0)

    for q in all_queries:
        # removing newline character from each line
        q = q.replace("\n", "")

        q_en = ""
        q_de = ""
        q_ru = ""

        qid = q[:3]
        query = q[4:]
        # q_lang = q['lang']
        hashtags = re.findall(r"#(\w+)", query)
        retweets = re.findall(r"@(\w+)", query)

        query = query.replace(":", "\:")
        # # without optimization
        # q_en = query
        # q_en = quote(q_en)
        # q_de = query
        # q_de = quote(q_de)
        # q_ru = query
        # q_ru = quote(q_ru)

        # with optimization
        q_en = "(" + query + ")"
        q_en = quote(q_en)
        q_de = "(" + query + ")"
        q_de = quote(q_de)
        q_ru = "(" + query + ")"
        q_ru = quote(q_ru)

        # create amalgamated query in all translated language
        # query = q_en + " " + q_de + " " + q_ru
        # query = query.replace(" ", "%20")
        # print("amalgamated QUERY--->", query)

        # q_en = q_en.replace(":", "\:")
        # q_en = quote(q_en)
        # q_en = q_en.replace(" ", "%20")
        # print("quoted QUERY--->", q_en)

        # q_de = q_de.replace(":", "\:")
        # q_de = quote(q_de)
        # q_de = q_de.replace(" ", "%20")
        # print("quoted QUERY--->", q_de)

        # q_ru = q_ru.replace(":", "\:")
        # q_ru = quote(q_ru)
        # q_ru = q_ru.replace(" ", "%20")
        # print("quoted QUERY--->", q_ru)

        if hashtags:
            hashtags = '%20'.join(["tweet_hashtags%3A%20" + h for h in hashtags])

        if retweets:
            retweets = '%20'.join(["@" + x for x in retweets])
        # print(hashtags)

        or_seperator = "%20OR%20"
        boost = "&defType=dismax&qf=text_en%5E1.5%20text_de%5E1.2%20text_ru%5E0.2"
        if hashtags:
            # # without optimization
            # inurl = localhost + core_name + select_q + "text_txt_en:" + q_en + or_seperator + \
            #         "text_txt_de:" + q_de + or_seperator + "text_txt_ru:" + q_ru + or_seperator + hashtags + fl_score

            # with optimization
            inurl = localhost + core_name + select_q + "text_txt_en:" + q_en + or_seperator + "text_en:" + q_en +\
                    or_seperator + "text_txt_de:" + q_de + or_seperator + "text_de:" + q_de + or_seperator +\
                    "text_txt_ru:" + q_ru +  or_seperator + "text_ru:" + q_ru + hashtags + fl_score
            print("Has Hashtags!")
            print("QNo. {} {}".format(qid, inurl))
        else:
            # # without optimization
            # inurl = localhost + core_name + select_q + "text_txt_en:" + q_en + or_seperator + \
            #         "text_txt_de:" + q_de + or_seperator + "text_txt_ru:" + q_ru + fl_score

            # with optimization
            inurl = localhost + core_name + select_q + "text_txt_en:" + q_en + or_seperator + "text_en:" + q_en +\
                    or_seperator + "text_txt_de:" + q_de + or_seperator + "text_de:" + q_de + or_seperator +\
                    "text_txt_ru:" + q_ru + or_seperator + "text_ru:" + q_ru  + fl_score

            print("QNo. {} {}".format(qid, inurl))

        # outf = open(outfn, 'a+')
        # data = urllib2.urlopen(inurl)
        # if you're using python 3, you should use
        data = urllib.request.urlopen(inurl)
        docs = json.load(data)['response']['docs']
        # the ranking should start from 1 and increase
        rank = 1
        for doc in docs:
            outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
            rank += 1
    outf.close()

# parser()
solr()
print("Done!")
