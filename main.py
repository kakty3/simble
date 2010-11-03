#!/usr/bin/python 

import web, os, users, messages
from urlparse import urlparse

itemsOnPage = 10
dbName = 'blog'

#web.config.debug = False

class login:
	def GET(self):
		if not session.loggedin:
			return render.login()
		else:
			return 'allready logge in'
	def POST(self):
		resp = users.login(web.input())
		if resp == 0:
			return web.seeother('/home')

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
		print 'REG POST'
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
		resp = messages.new(i)
		if resp == 0:
			return web.seeother('/home')
		else:
			return web.seeother('/home')
'''
def delete(id):
	if db.delete('images', where="id=$id", vars={'id' : id}):
		return "image id=%d deleted" % id
	else:
		return "no images with that id"
'''

class home:
	def GET(self):
		if session.loggedin:
			messages = list(db.select('messages', where="author=$id", vars={'id' : session.user_id}, order="created DESC"))
			return render.home(session, messages)
		else:
			return web.seeother('/')

class main:
	def GET(self, page = 1):
		print 'Request from ip %s page %s' % (web.ctx.ip, page)
		if session.loggedin:
			return web.seeother('/home')
		else:
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
			return render.main(session, messages)

#===================VARIABLES==========================================
urls = (
	'/', 'main',
	'/reg', 'registration',
	'/login', 'login',
	'/logout', 'logout',
	'/post', 'post',
	'/home', 'home'
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

render = web.template.render('templates/', globals={'session': session, 'getName': users.getName})
web.ctx.render = render
db = web.database(dbn='mysql', user='webpy', pw='webpy', db=dbName)

#=======================================================================

if __name__ == "__main__":
	app.run()
