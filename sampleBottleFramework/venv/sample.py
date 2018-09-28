from bottle import route, run, static_file, request

@route('/hello')
def hello():
    return "<h1>Hello world!</h1>"

#this is a website that displays an htm file
@route('/fromFile/<fileName>')
def fromFile(fileName):
    #to eliminate the need for users to type in the file type
    fileName=fileName+'.htm'
    return static_file(fileName, root= 'websites')

@route('/image/<picture>')
def serve_pictures(picture):
    picture=picture+'.png'
    return static_file(picture, root='websites')

#this is the result of login page
@route('/login')
def login():
    return static_file('login.htm', root= 'websites')
run(port=8090)