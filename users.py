import web
from hashlib import md5

db = web.database(dbn='mysql', user='webpy', pw='webpy', db='blog')

def addUser(name, password):
	'''
	Statuses:
		1: user exists
		2: password is to weak
		3: username contains invalid symbols
	'''
	if len(password) < 6:
		return 2
	if not db.select('users', where="name=$name", vars={'name' : name}):
		password = md5(password).hexdigest()
		n = db.insert('users', name=name, password=password)
		return 0
	else:
		return 1

def getName(id):
	check = db.select('users', where="id=$id", vars={'id' : id})
	if check:
		return check[0].name
	else:
		return 'No user with id=%d' % id

def login(i):
	print "trying to login"
	session = web.ctx.session
	pswd = md5(i.password).hexdigest()
	check = db.select('users', where="name=$n AND password=$pswd", vars={'n' : i.username, 'pswd' : pswd})
	if check:
		user = check[0]
		session.loggedin = True
		session.username = user.name
		session.user_id = user.id
		return 0
	else:
		return "Password or username is incorrect"

def logout():
	session = web.ctx.session
	session.kill()
	return 0
if __name__ ==  '__main__':
	#print getName(2)
	pass
