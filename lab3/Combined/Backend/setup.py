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
print_page_rank(result_page_rank)
print "set up complete"



#Now copy this function to your front end, you can use it if you import redis
