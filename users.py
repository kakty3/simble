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

def getUser(**request):
	x = request.keys()[0]
	w = ('%s=$%s') % (x, x)
	v = {x : request[x]}
	for k in request.keys()[1:]:
		w = ('%s AND %s=$%s') % (w, k, k)
		v[k] = request[k]
	print w
	print v
	users = db.select('users', where=w, vars=v)
	print len(users)
	if len(users):
		return users[0]
	else:
		return -1

def getName(id):
	#check = db.select('users', where="id=$id", vars={'id' : id})
	user = getUser(id = id)
	print user
	return user.name
'''
def getId(name):
	check = db.select('users', where="name=$name", vars={'name' : name})
	if check:
		return check[0].id
	else:
		return -1
'''


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
		return 1

def logout():
	session = web.ctx.session
	session.kill()
	return 0

if __name__ ==  '__main__':
	#print getName(2)
	pass
	search(id = 3, name = 'sergey')
