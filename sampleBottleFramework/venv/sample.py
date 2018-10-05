from bottle import route, run, static_file, request, template
from collections import Counter

search_history = Counter()
listed= ['brandon','efe']
freq = [2,1]

@route('/hello')
def hello():
    return "<h1>Hello world!</h1>"

#this is a website that displays an htm file
@route('/')
def fromFile():
    #to eliminate the need for users to type in the file type
    fileName='home'
    words = history_word_parse()
    count =history_count_parse()
    return template(fileName,name=words,freq=count)

@route('/image/<picture>')
def serve_pictures(picture):
    picture = picture+'.png'
    return static_file(picture, root='websites')

#this is the result of login page
@route('/login')
def login():
    return static_file('login.htm', root= 'websites')

@route('/', method='POST')
def parse():
    query = request.forms.get('search')
    words_in_quesry=query.split(" ")
    my_url = "query="
    for word in words_in_quesry:
        my_url += word + "+"
    parsed_dict = word_count(query)
    words = search_word_parse(parsed_dict)
    count = search_count_parse(parsed_dict)
    #redirect("/search/<my_url>")
    return template('search', name = words,freq = count,query = query)

#For users with the link
@route('/search/query=<query>')
def user_with_link(query):
    return '<p>You are looking for a search result: '+query +'.</p>'

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

def history_word_parse():
    words = []
    i=0
    for word, count in search_history.most_common(20):
        words.append(word)
        i+=1
    return words

def history_count_parse():
    freq = []
    i = 0
    for word, count in search_history.most_common(20):
        freq.append(count)
        i += 1
    return freq
def search_word_parse(results):
    words = []
    i=0
    for word, count in results.items():
        words.append(word)
        i+=1
    return words

def search_count_parse(results):
    freq = []
    i = 0
    for word in results:
        freq.append(results[word])
        i += 1
    return freq
run(port=8080)

#Template for table results page#
#Request used for getting quesries in the Url and can be used
#in the def of the route and param1=request.quesry.param1
