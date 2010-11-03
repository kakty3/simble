import web

db = web.database(dbn='mysql', user='webpy', pw='webpy', db='blog')

dbName = 'messages'

def new(message):
	if message.body.strip():
		n = db.insert(dbName, body=message['body'], author=web.ctx.session.user_id)
		return 0
	else:
		return 1 #message can't be empty

def delete(id):
	pass


