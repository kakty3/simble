#!/usr/bin/python 

import web, users
from urlparse import urlparse

itemsOnPage = 10
dbName = 'blog'

#web.config.debug = False

class main:
	def GET(self, page = 1):
		return 'admin page is under construct'
#===================VARIABLES==========================================
urls = (
	'(\/?)', 'main',
)

app = web.application(urls, globals())

render = web.template.render('templates/',)
web.ctx.render = render
db = web.database(dbn='mysql', user='webpy', pw='webpy', db=dbName)

#=======================================================================

if __name__ == "__main__":
	app.run()
