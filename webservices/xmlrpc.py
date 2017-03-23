import functools
import xmlrpclib


HOST = 'localhost'
PORT = 8069
DB = 'testopenacademy'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print "Logged in as %s (uid:%d)" % (USER,uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)


# 2. Read the sessions
sessions = call('openacademy.session','search_read', [], ['name','seats'])
for session in sessions:
    print "Session %s (%s seats)" % (session['name'], session['seats'])

# 3.create a new session for the "Functional" course
course_id = call('openacademy.course', 'search', [('name','ilike','Functional')])[0]
instructor_id = call('res.partner', 'search', [('name', 'like', 'Edward Foster')])
attendee_ids = call('res.partner', 'search', ['&',('is_company', '=', 0),'!',('instructor', '=', True)])
session_id = call('openacademy.session', 'create', {
    'name' : 'My session',
    'course_id' : course_id,
    'instructor_id' : instructor_id[0],
    'duration' : 10,
    'seats' : 100,
    #'attendee_ids' : [(6, 0, [1,2])],
    'attendee_ids' : [(6, 0, attendee_ids)],
})
