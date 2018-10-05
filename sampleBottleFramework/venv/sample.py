from bottle import route, run, static_file, request, template
from collections import Counter

search_history = Counter()


@route('/hello')
def hello():
    return "<h1>Hello world!</h1>"

#this is a website that displays an htm file
@route('/')
def fromFile():
    #to eliminate the need for users to type in the file type
    fileName='home'

    return template(fileName)

@route('/image/<picture>')
def serve_pictures(picture):
    picture = picture+'.png'
    return static_file(picture, root='websites')

#this is the result of login page
@route('/login')
def login():
    return static_file('login.htm', root= 'websites')

@route('/search', method='POST')
def parse():
    query = request.forms.get('search')
    words_in_quesry=query.split(" ")
    my_url = "query="
    for word in words_in_quesry:
        my_url += word + "+"
    parsed_dict = word_count(query)
    #redirect("/search/<my_url>")
    return parsed_dict

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
run(port=8090)

#Template for table results page#
#Request used for getting quesries in the Url and can be used
#in the def of the route and param1=request.quesry.param1
