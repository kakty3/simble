import web

db = web.database(dbn='mysql', user='webpy', pw='webpy', db='blog')

dbName = 'messages'

def new(message):
	n = db.insert(dbName, topic=message['topic'], body=message['body'], author=web.ctx.session.user_id)
	return 0

def delete(id):
	pass


