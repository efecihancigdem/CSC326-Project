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
from bottle import route, run, static_file, request, template , redirect , hook , get
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
import sys
sys.path.insert(0, 'Backend/')
import crawler
import pageRank



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
REDIRECT_URI = "http://localhost:8080/redirect"

#Global variables for Keeping thrack of the session
logged_in = False
user_email = ""

#Gloabl variables that keeps track of the client search history regarding the user's id and email address 
search_history = Counter()
Client_DB = defaultdict(dict)
client_list= []


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
        return template(fileName,name=words,freq=count,logged_in = logged_in , user= user_email)
    # Parsing the search dividing the word and the frequency into 2 lists as words and count
    parsed_dict = word_count(query)
    words = search_word_parse(parsed_dict)
    

    #new part for lab3
    page_num = request.query.page_no
    print "page value = " , page_num
    first_word = query.split()
    crawler.simulate_a_search(first_word[0], bot, result_page_rank)


    ###########################################################################################################
    ######passing first_word[0] to search algo of the backend
    ######Putting them into a global variable
    ######if total pages > 5 starts paginate
    ###### MAKE SURE HAVE GLOBAL FOR CURRENT PAGE AND CURRENT_QUERY TO CHECK THE STATE and not to do the research again
    ###########################################################################################################
    count = search_count_parse(parsed_dict)

    #if results_num >5:
    
    redirect_url_base = "/?keywords="+urllib.quote_plus(query)
    print REDIRECT_URI
        #if current page != page_num:
            #redirect(/redirect_url_base+"&page_no="+str(current_page) )
        #ELSE
            #if current_page=1
                #current_page++
                #next_url = redirect_url_base+"&page_no="+str(current_page)
                #current_url = redirect_url_base+"&page_no="+str(current_page-1)
                #return template('search', name=words, freq=count, query=query ,logged_in = logged_in , user= user_email, current_url= ,  next_url= ,previous_url = "none" ) # sending lists to template to display

            #RETRUN BELWO
    return template('search', name=words, freq=count, query=query ,logged_in = logged_in , user= user_email ) # sending lists to template to display


@route('/about')
def about():
    return static_file("about.html", root = ".")


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
    redirect("https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8080/")
	

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

#craw the web first
bot = crawler.crawler(None, "Backend/urls.txt")
bot.crawl(depth=1)
result_page_rank=pageRank.page_rank(bot._url_link)

app = SessionMiddleware(bottle.app(), session_opts)
bottle.run(host='localhost',port=8080,app=app)

