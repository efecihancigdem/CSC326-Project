#########################################################################
#Project name: Kajima                                                   #
#Authors: Zixuan Nie & Efe Cihan Cigdem                                 #
#Function: Search engine website applciation that hosted in AWS.        #
#          Capable of holding most frequent 20 searches after           #
#          completing Google sign in. USer can sign-out using sign-out  #
#          button in the website.                                       #
#Date: 27/10/2018                                                       #
#########################################################################

import bottle
from bottle import route, run, static_file, request, template , redirect , hook , get, error
from collections import Counter, defaultdict
import os
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
from beaker.middleware import SessionMiddleware
import urllib2
import urllib
import redis
import sys
import os

os.chdir(os.path.dirname(sys.argv[0]))


#session varibales for session management
session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 3000,
    'session.data_dir': './data',
    'session.auto': True
}

#Google variables
CLIENT_ID= "41115492198-68e4f5r58f8toqi72hmgrf8rcjp24066.apps.googleusercontent.com"
CLIENT_SECRET = "_gSgca14PJ3LKVQgyubz5Tms"
SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
REDIRECT_URI = "http://100.24.87.175.xip.io:80/redirect"

#Global variables for Keeping thrack of the session
logged_in = False
user_email = ""

#Gloabl variables that keeps track of the client search history regarding the user's id and email address 
search_history = Counter()
Client_DB = defaultdict(dict)
client_list= []

#new glabal variables for Lab3 
current_query = ""
links = [] #= ["http://www.google.ca", "http://www.apple.com", "http://www.toronto.ca", "http://www.tesla.com","https://www.oneplus.com/ca_en/","https://www.nba.com/lakers/","https://www.utoronto.ca/" ]
link_num=0
total_page = 0
if sys.argv[1] != None:
    global ip_address
    ip_address = sys.argv[1]
else:
    pass

def do_a_search_redis(search_word, titles=[], first_20_words=[]):
    '''This function takes in the word you want to search and return a list of urls ranking from
        the best match to the worst match (element 0 is best match and element last is worst)'''
    r = redis.Redis('localhost')
    #this is a dictionary that stores the key as url_id and their score as value
    url_id_scores = {}
    for word in search_word:
        word=word.lower()
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
        website_title=r.hget('_document_title', id)
        if website_title is not None:
            website_title=website_title[2:-1]
        else:
            website_title=id
        titles.append(website_title)
        first_20_words.append(" ".join(r.hget('_first_20_words', str(id)).split()[0:8]))

    # the return variable is a list of searched urls sorted by their score
    return url_sorted_by_score


@hook('before_request')
# Get the session object from the environ
def setup_request():
    request.session = request.environ['beaker.session']


#The fucntion that handles main page and result page
@route('/')
def display_search():
    # Checking if the user logged in if so does sesion management
    if logged_in == True:
        session_management()
    query = request.query.keywords #getting url query
    if query == "": #Checking if it is home page request or search request
        fileName = 'home_css'
        words = history_word_parse()
        count = history_count_parse()
        return template(fileName,name=words,freq=count,logged_in = logged_in , user= user_email,root_address=ip_address )
    # Parsing the search dividing the word and the frequency into 2 lists as words and count
    parsed_dict = word_count(query)
    words = search_word_parse(parsed_dict)
    count = search_count_parse(parsed_dict)

    ##############################################################################new part for lab3
    current_page = request.query.page_no
    print "page value ="+str(current_page)
    redirect_url_base = "/?keywords="+urllib.quote_plus(query)
    print redirect_url_base
    ##algo here
    lucky = request.query.feeling_lucky
    if lucky == "I am feeling lucky":
        ordered_words = query.split()
        first_link=do_a_search_redis(ordered_words)
        if first_link==None:
            return template('search', name=words, freq=count, query=query, logged_in=logged_in, user=user_email,
                            description=[],
                            website_name=[], link=[], link_num=0, total_page=0,
                            current_page=0, base_link=redirect_url_base, next_link="none",
                            prev_link="none",root_address=ip_address )
        redirect(first_link[0])
    link_name = []
    description = []
    links=[]
    link_num=0
    total_page=0

    if query != current_query:
        global current_query
        current_query = query
        ordered_words = query.split()

        links=do_a_search_redis(ordered_words, link_name, description)
        if links==None:
            return template('search', name=words, freq=count, query=query, logged_in=logged_in, user=user_email,
                            description=[],
                            website_name=[], link=[], link_num=0, total_page=0,
                            current_page=0, base_link=redirect_url_base, next_link="none",
                            prev_link="none",root_address=ip_address )

        link_num = len(links)
        total_page = -(-link_num / 6)
        print "new search is done"
        print "##########################################################" \
              "Here is the values for link_num, total_page and links",link_num,total_page,links

    print "before isinstance"
    if current_page != "": # checking if current_page exist
        ordered_words = current_query.split()
        links = do_a_search_redis(ordered_words, link_name, description)
        link_num=len(links)
        total_page = -(-link_num / 6)
        integer_version = int(current_page)
        if integer_version==1: 
            print "first page"
            next_link=redirect_url_base+"&page_no=2"
            prev_link="none"
        elif integer_version == total_page:
            print "last page"
            next_link="none"
            prev_page = int(current_page)-1
            prev_link=redirect_url_base+"&page_no="+str(prev_page)
        else:
            print "mid pages"
            next_page =int(current_page)+1
            next_link=redirect_url_base+"&page_no="+str(next_page)
            prev_page = int(current_page)-1
            prev_link=redirect_url_base+"&page_no="+str(prev_page)

        return template('search', name=words, freq=count, query=query ,logged_in = logged_in , user= user_email , description=description ,
        website_name= link_name ,link = links,link_num=link_num, total_page= total_page, current_page= integer_version , base_link=redirect_url_base , next_link=next_link , prev_link=prev_link ,root_address= ip_address ) # sending lists to template to display
        #linkname and description needs to change
    else:
        print "else isinstance"
        #needs redirecting to add new page_no parameter to the url
        redirect(str(redirect_url_base+"&page_no=1"))
    

@route('/about')
def about():
    return template("about", root_address=ip_address , logged_in=logged_in)


#USer Google Signin Procedure
@route('/signin')
def Google_signin():
	flow = flow_from_clientsecrets("client_secrets.json",scope= SCOPE, redirect_uri=REDIRECT_URI)
	uri = flow.step1_get_authorize_url()
	redirect(str(uri))


#User Sign-out section
@route('/signout')
def sign_out():
    global Client_DB
    #Transferring search history to Clinet DB
    for keyword, freq in search_history.items():
        Client_DB[current_user][keyword]=freq
    #Reseting global variables
    global logged_in
    logged_in = False
    global user_email
    user_email = ''
    global current_user
    current_user = None
    token = None
    request.session.pop('user_id', None)
    request.session.save()
    #Google Log out procedure
    redirect("https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://100.24.87.175.xip.io:80")
	

#Google redirects here after getting the request
@route('/redirect')
def redirect_page():
    #Google SIgn-in Procedure continued 
    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(client_id = CLIENT_ID, client_secret= CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']
    http = httplib2.Http()
    http = credentials.authorize(http)
	# Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    get_user_email = user_document['email']
    #CHanging Global variables after gaining user's email address
    global user_email 
    user_email=get_user_email
    if logged_in == False:
        global search_history
        search_history.clear()	
    global logged_in
    logged_in = True
    #If user logged in earlier, memory restores and goes back to main page
    memory_restore()
    redirect('/')

#Function to reach our logo
@route('/image/<picture>')
def serve_pictures(picture):
    picture_real = picture+'.png'
    exists = os.path.isfile('/websites/'+picture_real)
    if not exists:
	picture_real=picture+'.PNG'
    return static_file(picture_real, root='websites')


@route('/css/<filename>')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/img/<filename>')
def showcaseimage(filename):
    return static_file(filename, root='img')

@error(404)
def error404(error):
    return template('error', root_address=ip_address )


########################################################################
##################### Local functions ##################################
########################################################################s 
#Session Management module
def session_management():   
    if check_key(request.session, 'user_id'):
        if check_exist(request.session['user_id']):
            if check_exist(client_list[request.session['user_id']]):
                #A previous user
                global current_user
                current_user=request.session['user_id']
            else:
                pass
    else:

        #new or first user
        if len(client_list)>0:
            found = False
            #Removing Google redirect affect
            for user_id in range(len(client_list)):
                if client_list[user_id] == user_email:
                    #Google's sign in procedure return caused this
                    global current_user
                    current_user = user_id
                    found = True
                    request.session['user_id'] = user_id
            #new user        
            if found == False:
                client_list.append(user_email)
                new_id = (len(client_list)-1)
                request.session['user_id'] = new_id
                global current_user
                current_user= new_id 
        else:
            #first user
            global current_user
            current_user = 0
            request.session['user_id'] = 0
            client_list.append(user_email)
    #saving the session
    request.session.save() 
    
#THis function restores the search history if the user used our website before in signed in mode
def memory_restore():
    for user_id in range(len(client_list)):
        if client_list[user_id] == user_email:
            global search_history
            search_history = Counter(Client_DB[user_id])



#Checks if the key exist in the dictionary
def check_key( dic, searched_key):
    if searched_key in dic:
        return True
    else:
        return False

#Checks if the variable given to function exist
def check_exist(value):
    exist= True
    try:
        value
    except NameError:
        exist=False
    return exist        


#Function to increment search history and count occurance of the keywords
def word_count(str):
    counts = dict()
    words = str.split()
    for word in words:
        search_history[word] += 1
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

#Making a list of keywords from the most common 20 keywords in search_history variable
def history_word_parse():
    words = []
    i=0
    for word, count in search_history.most_common(20):
        words.append(word)
        i+=1
    return words

#Making a list of number of occurances corresponding to most common 20 keywords from search_history variable
def history_count_parse():
    freq = []
    i = 0
    for word, count in search_history.most_common(20):
        freq.append(count)
        i += 1
    return freq

#Making a list of keywords from the search query
def search_word_parse(results):
    words = []
    i=0
    for word, count in results.items():
        words.append(word)
        i+=1
    return words

#Making a list of occurances from the search query
def search_count_parse(results):
    freq = []
    i = 0
    for word in results:
        freq.append(results[word])
        i += 1
    return freq



########################################################################
################### Running the website ################################
########################################################################

app = SessionMiddleware(bottle.app(), session_opts)
bottle.run(host='0.0.0.0',port=80,app=app)

