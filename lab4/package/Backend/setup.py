#In this setup the crawler will crawl all the webs provided in file urls.txt
#afterwards it will upload all the information onto persistent storage
#Only need to run this setup once

#before you run setup, you should go to your ubuntu shell, run command
#               $ sudo apt-get install redis-server
#to install redis server
#as well as
#               $ pip install redis
#to install python api for redis server
#To restart redis server, use
#sudo service redis-server restart

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

def do_a_search_redis(search_word, titles, first_20_words):
    '''This function takes in the word you want to search and return a list of urls ranking from
        the best match to the worst match (element 0 is best match and element last is worst)'''
    r = redis.Redis('localhost')
    #this is a dictionary that stores the key as url_id and their score as value
    url_id_scores = {}
    for word in search_word:
        search_word_id= r.hget('_lexicon_dic', word)
        if search_word_id==None:
            print "Word not found: ", word
            continue
        url_id_list=set()

        url_id_list=r.hget("_inverted_index", search_word_id)
        #the url_id_list we get is a string of the form set(...), convert it into anactual set
        url_id_list=eval(url_id_list)
        for url_id in url_id_list:
            numb=r.hget('page_rank', url_id)
            if numb==None:
                continue
            if url_id in url_id_scores:
                url_id_scores[url_id] += float(numb)
            else:
                url_id_scores[url_id]=float(numb)
    # try to get the length of the url_id_scores, if it doesn't exist, none of the words are found

    length=len(url_id_scores)
    if not length:
        print "No results found"
        return
    # sort the dictionary of url ids based on their score
    sorted_by_score=sorted(url_id_scores.items(), key=lambda t:t[1])

    url_sorted_by_score = []
    for pair in reversed(sorted_by_score):
        url_sorted_by_score.append(r.lindex('_document_index', int(pair[0])))

    # append the title and description of each website
    for id in url_sorted_by_score:
        print
        titles.append(r.hget('_document_title', id))
        first_20_words.append(r.hget('_first_20_words', str(id)))

    # the return variable is a list of searched urls sorted by their score
    return url_sorted_by_score


try:
    r=redis.Redis('localhost',port='6379')
    r.ping()
except redis.exceptions.ConnectionError:
    print "Your redis server is not setup correctly, make sure you are using localhost and port 6379 for redis server"
    sys.exit()
#
# bot = crawler.crawler(None, "urls.txt")
# bot.crawl(depth=1)
# result_page_rank=pageRank.page_rank(bot._url_link)
# bot.save_to_redis(result_page_rank)
# print_page_rank(result_page_rank)
# print "set up complete"
titles=[]
first_20_words=[]
print do_a_search_redis(['asdf', 'amzfdfdsa'], titles, first_20_words)

print titles
print first_20_words




#Now copy this function to your front end, you can use it if you import redis
