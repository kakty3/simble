#!/usr/bin/python 

import web, os, users, messages
from urlparse import urlparse

ItemsOnPage = 10
DatabaseName = 'blog'

#web.config.debug = False

def ret(a, b, c):
	if a:
		return b
	else:
		return c

def validUrl(url):
	parsed = urlparse(url)
	if (parsed.scheme == 'http') and (parsed.path):
		ext = parsed.path.split('/')[-1].split('.')[-1]
		try:
			['jpg', 'jpeg', 'gif', 'png'].index(ext.lower())
		except ValueError:
			return 0
		else:
			return 1
	else:
		return 0

class add:
	def GET(self):
		if session.loggedin:
			i = web.input()
			print i
			if not i:
				return render.add()
			try:
				name = i.t
				url = i.u
			except AttributeError:
				return 'Bad request'
			else:
				#return 'name=%s url=%s' % (name, url)
				if validUrl(url):
					print '=' * 30
					print 'name \"%s\"' % name
					if name:
						n = db.insert('images', url=url, name=name, public=1, user_id=session.user_id)
						return 'name: %s\nurl: %s\nstatus: %s' % (name, url, 'posted')
					else:
						return render.message("Error", "Trying to add picture without name", "try again", "/add")
				else:
					return render.message("Error", "Url is not valid", "try again", "/add")
		else:
			print 'not logged in'
			return render.index()
			#return "Please, login to add pictures"

	def POST(self):
		i = web.input()
		#print i
		try:
			i.public
		except:
			public = 0
		else:
			public = 1
		url = i.url
		name  = i.name
		print 'name \'%s\'' % name
		if validUrl(url):
			if name:
				n = db.insert('images', url=i.url, name=i.name, public=public, user_id=session.user_id)
				return render.message("Well done", "Picture was succesfully added")
			else:
				return render.message("Error", "Trying to add picture without name", "try again", "/add")
		else:
			return render.message("Error", "Url is not valid", "try again", "/add")

class login:
	def GET(self):
		if not session.loggedin:
			return render.login()
		else:
			return 'allready logge in'
	def POST(self):
		resp = users.login(web.input())
		if resp == 0:
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

class ajax:
	def GET(self):
		return render.ajax()
	def POST(self):
		i = web.input()
		print i
		com = i.text
		if com == 'ping':
			return 'pong'
		else:
			return 'unknown command'

class post:
	def GET(self):
		return render.post(session)

	def POST(self):
		i = web.input()
		resp = messages.new(i)
		if resp == 0:
			return web.seeother('/')


def delete(id):
	if db.delete('images', where="id=$id", vars={'id' : id}):
		return "image id=%d deleted" % id
	else:
		return "no images with that id"

class logout:
	def GET(self):
		users.logout()
		return web.seeother('/')

class main:
	#@staticmethod
	def GET(self, page = 1):
		print 'Request from ip %s page %s' % (web.ctx.ip, page)
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
		return render.main(session)

#===================VARIABLES==========================================
urls = (
	'/', 'main',
	'/reg', 'registration',
	'/login', 'login',
	'/logout', 'logout',
	'/post', 'post'
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
db = web.database(dbn='mysql', user='webpy', pw='webpy', db='gallery')

#=======================================================================

if __name__ == "__main__":
	app.run()
