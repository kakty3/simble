#!/usr/bin/python 

import web, os, users, messages, admin
from urlparse import urlparse

itemsOnPage = 10
dbName = 'blog'

#web.config.debug = False

class login:
	'''
	def GET(self):
		if not session.loggedin:
			return render.login()
		else:
			return 'allready logged in'
	'''
	def POST(self):
		#print '<<LOGIN>>', web.input()
		resp = users.login(web.input())
		return resp

class logout:
	def GET(self):
		users.logout()
		return web.seeother('/')

class registration:
	def GET(self):
		if not session.loggedin:
			return render.registration()
		else:
			return render.message("Warning", "Please, log out to register")#, 'try to login again', '/login')

	def POST(self):
		i = web.input()
		#print i
		resp = users.addUser(i.username, i.password)
		if resp == 0:
			return web.seeother('/')
		else:
			return 'error'

class post:
	def GET(self):
		raise web.notfound()

	def POST(self):
		i = web.input()
		print '<<POST>>', i
		resp = messages.new(i)
		if resp == 0:
			return web.seeother('/home')
		else:
			return web.seeother('/home')


class delete:
	'''
	def GET(self,):
		resp = messages.delete(id)
		if resp == 0:
			return 0
			#return web.seeother('/')
		else:
			return 'something went wrong'
	'''

	def POST(self):
		id = web.input().id
		message = messages.search(id=id)
		if message and message[0].author == session.user_id:
			resp = messages.delete(id)
			if resp == 0:
				return 0
				#return web.seeother('/')
			else:
				return 1
		else:
			return 'you can\'t delete this post'


class home:
	def GET(self):
		if session.loggedin:
			messages = list(db.select('messages', where="author=$id", vars={'id' : session.user_id}, order="created DESC"))
			return render.home(messages)
		else:
			return web.seeother('/')

class main:
	def GET(self, page = 1):
		print 'Request from ip %s page %s' % (web.ctx.ip, page)
		'''
		if session.loggedin:
			return web.seeother('/home')
		else:
		'''
		######
		#path = web.ctx.path
		#print path.split('/')[1]
		#if path and path.split('/')[1] == 'all':
		#	gallery = list(db.select('images', order="created DESC"))
		#else:
		#x = list(db.select('images', order="created DESC", where="public=$true", vars={'true' : 1}))
		#pages = len(gallery) / ImagesOnPage
		#page = int(page)
		#if len(gallery) % ImagesOnPage:
		#	pages += 1
		messages = list(db.select('messages', order="created DESC"))
		return render.main(messages)

class userPage:
	def GET(self, userName):
		resp = users.getUser(name = userName)
		#print '<<RESP>>', resp
		if resp == -1:
			return 'no user with this name'
		else:
			userId = resp.id
			if userId == -1:
				return 'No user with this name'
			else:
				messages = list(db.select('messages', where="author=$id", vars={'id' : userId}, order="created DESC"))
				#print messages
				return render.user(messages, userName)

class showPost:
	def GET(self, id):
		message = messages.search(id = id)
		if message:
			return render.post(message[0])
		else:
			return 'no post with this id'

#===================VARIABLES==========================================
urls = (
	'/', 'main',
	'/reg', 'registration',
	'/login', 'login',
	'/logout', 'logout',
	'/post', 'post',
	'/post/(\d+)', 'showPost',
	'/delete', 'delete',
	'/home', 'home',
	'/admin', admin.app,
	'/([a-z0-9]+)', 'userPage',
	#'/admin', admin.app,
)

app = web.application(urls, globals())

if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'), initializer = {'username': None, 'loggedin': False, 'user_id': -1, 'permission': 0})
	web.config._session = session
else:
	session = web.config._session

def session_hook():
	web.ctx.session = session
	web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))

global_vars = {'session': session, 'getName': users.getName, }
render = web.template.render('templates/', globals = global_vars)
global_vars['render'] = render
#render = web.template.render('templates/',  globals={'session': session, 'getName': users.getName, 'render' : render, 'home' : web.ctx.home})
web.ctx.render = render
db = web.database(dbn='mysql', user='webpy', pw='webpy', db=dbName)

#=======================================================================

if __name__ == "__main__":
	#web.sendmail('kakty3.mail@gmail.com', 'kakty3nsk@yandex.ru', 'webpy mail test', '<html><span style="backgroud:#8997D9; color: #FFFFFF; font-weight: bold">Hello, world!</span></html>')
	app.run()

