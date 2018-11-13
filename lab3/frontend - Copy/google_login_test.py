from bottle import route, run, static_file, request, template, redirect
from collections import Counter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2

CLIENT_ID= "41115492198-68e4f5r58f8toqi72hmgrf8rcjp24066.apps.googleusercontent.com"
CLIENT_SECRET = "_gSgca14PJ3LKVQgyubz5Tms"
SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
REDIRECT_URI = "http://localhost:8080/redirect"

logged_in = False
user_id = ""

#The fucntion that handles main page and result page
@route('/')
def handler():
	query = request.query.keywords #getting url query
	if query == "":
		if logged_in == True:
			print "**************logged_in is True"
		else:
			print"**************logged_in is false user_id is " + user_id
		return template('test_template',logged_in = logged_in , user= user_id)
	else: 
		home()
		

def home():
    flow = flow_from_clientsecrets("client_secrets.json",scope= SCOPE, redirect_uri=REDIRECT_URI)
    uri = flow.step1_get_authorize_url()
    redirect(str(uri))

@route('/redirect')
def redirect_page():
	code = request.query.get('code', '')
	flow = OAuth2WebServerFlow(client_id = CLIENT_ID, client_secret= CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
	credentials = flow.step2_exchange(code)
	token = credentials.id_token['sub']
	http = httplib2.Http()
	http = credentials.authorize(http)
	# Get user email
	users_service = build('oauth2', 'v2', http=http)
	user_document = users_service.userinfo().get().execute()
	user_email = user_document['email']
	global user_id
	user_id=user_email
	print "**************user email value = " + user_email
	global logged_in
	logged_in = True
	print "**************logged_in value = %r" %(logged_in)
	redirect('/')

run(port=8080)


