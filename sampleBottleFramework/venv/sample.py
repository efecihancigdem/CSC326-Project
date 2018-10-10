from bottle import route, run, static_file, request, template
from collections import Counter

#Global counter to keep track of search history
search_history = Counter()

#The fucntion that handles main page and result page
@route('/')
def display_search():
    query = request.query.search #getting url query
    if query == "": #Checking if it is home page request or search request
        fileName = 'home'
        words = history_word_parse()
        count = history_count_parse()
        return template(fileName,name=words,freq=count)
    # Parsing the search dividing the word and the frequency into 2 lists as words and count
    parsed_dict = word_count(query)
    words = search_word_parse(parsed_dict)
    count = search_count_parse(parsed_dict)
    return template('search', name=words, freq=count, query=query) # sending lists to template to display

#Function to reach our logo
@route('/image/<picture>')
def serve_pictures(picture):
    picture = picture+'.png'
    return static_file(picture, root='websites')

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
run(port=8080)


