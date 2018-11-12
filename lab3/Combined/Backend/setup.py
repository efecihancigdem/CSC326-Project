#In this setup the crawler will crawl all the webs provided in file urls.txt
#afterwards it will upload all the information onto persistent storage
#Only need to run this setup once

#before you run setup, you should go to your ubuntu shell, run command
#               $ sudo apt-get install redis-server
#to install redis server
#as well as
#               $ pip install redis
#to install python api for redis server

import pageRank
import crawler
import redis
import sys

def print_page_rank(result_page_rank):
    sorted_by_score = sorted(result_page_rank.items(), key=lambda t: t[1])
   # url_sorted_by_score=[]
  #  for pair in reversed(sorted_by_score):
   #     url_sorted_by_score.append(r.lindex('_document_index', int(pair[0])))
    for pageIndex, pageScore in reversed(sorted_by_score):
        if pageIndex==0:
            continue
        print "Page url: " + r.lindex('_document_index', pageIndex) + ". Page score: " + str(pageScore)

def do_a_search_redis(search_word, printall=False):
    '''This function takes in the word you want to search and return a list of urls ranking from
        the best match to the worst match (element 0 is best match and element last is worst)'''
    r = redis.Redis('localhost')
    search_word_id= r.hget('_lexicon_dic', search_word)
    if search_word_id==None:
        print "Could not find word"
        return
    url_id_list=set()
    if printall:
        for i in range (r.llen('_document_index')):
            url_id_list.update(i)
    else:
        url_id_list=r.hget("_inverted_index", search_word_id)
    #the url_id_list we get is a string of the form set(...), convert it into anactual set
    url_id_list=eval(url_id_list)
    url_id_scores={}
    for url_id in url_id_list:
        numb=r.hget('page_rank', url_id)
        if numb==None:
            continue
        url_id_scores[url_id]=float(numb)
    # sort the dictionary of url ids based on their score
    sorted_by_score=sorted(url_id_scores.items(), key=lambda t:t[1])

    url_sorted_by_score = []
    for pair in reversed(sorted_by_score):
        url_sorted_by_score.append(r.lindex('_document_index', int(pair[0])))

    return url_sorted_by_score

try:
    r=redis.Redis('localhost',port='6379')
    r.ping()
except redis.exceptions.ConnectionError:
    print "Your redis server is not setup correctly, make sure you are using localhost and port 6379 for redis server"
    sys.exit()

bot = crawler.crawler(None, "urls.txt")
bot.crawl(depth=1)
result_page_rank=pageRank.page_rank(bot._url_link)
bot.save_to_redis(result_page_rank)
print do_a_search_redis('place')
print_page_rank(result_page_rank)
print "set up complete"



#Now copy this function to your front end, you can use it if you import redis
