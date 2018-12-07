import bottle
from beaker.middleware import SessionMiddleware
from bottle import request, route, hook


session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

client_list= []

@hook('before_request')

# Get the session object from the environ
def setup_request():
	request.session = request.environ['beaker.session']
	print '***************************************session = ' 
	print request.session 
	

@bottle.route('/')
def simple_app():	
	#session['accessed'] = session.get('accessed',0) + 1
	print '***************************************in the simple app'
	if check_key(request.session, 'user_id'):
		print '***************************************not first user'
		if check_exist(request.session['user_id']):
			if check_exist(client_list[request.session['user_id']]):
				#visited
				global current_user
				current_user=request.session['user_id']
				print '***************************************visited current user = ', current_user
			else:
				print "******************request.session != in+session[user_id] exist"
			
	else:
		print '***************************************first/new user'
		#new/first user
		if len(client_list)>0:
			#new user
			client_list.append('new_user@gmail.com')
			new_id = (len(client_list)-1)
			request.session['user_id'] = new_id
			global current_user
			current_user= new_id 
			print '***************************************new current user = ', current_user
		else:
			#first user
			global current_user
			current_user = 0
			request.session['user_id'] = 0
			client_list.append('first_user@gmail.com')
	
	request.session.save() #problem hereee dont carry the dict in the session
	print '***************************************Session is saved'
	print client_list
	print 'current user is ' , current_user
	print '----------------------------------------------------------------------------------------'
	print '----------------------------------------------------------------------------------------'
	return client_list


def check_key( dic, searched_key):
	if searched_key in dic:
		return True
	else:
		return False


def check_exist(value):
	exist= True
	try:
		value
	except NameError:
		exist=False
	return exist
		


app = SessionMiddleware(bottle.app(), session_opts)

bottle.run( app=app)
#host='0.0.0.0',port=80,




