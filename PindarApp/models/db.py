# -*- coding: utf-8 -*-
from datetime import datetime

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db = DAL('sqlite://storage.sqlite',
         check_reserved=['mysql'])

from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)




db.define_table('LANGUAGE',
			Field('LanguageCode', 'string', length=3),
			Field('EnglishName', 'string', length=64),
			Field('NativeName', 'string', length=64))


db.define_table('USER',
			Field('UserName', 'string', length=32, required=True),
			Field('DateJoined', 'datetime', default=datetime.now()),
			Field('PrimaryLanguageID', 'integer', 'reference LANGUAGE'),
			Field('UserBiography', 'text'),
			Field('IsDeleted', 'boolean'))


db.define_table('QUOTE',
            Field('Text', 'text', required=True),
            Field('SubmitterID', 'reference USER', required=True),
            Field('SubmissionDate', 'datetime', default=datetime.now()),
            Field('QuoteLanguageID', 'reference LANGUAGE', required=True),
            Field('IsOriginalLanguage', 'boolean'),
            Field('IsDeleted', 'boolean', default=False),
            Field('Note', 'text'))


db.define_table('WORK',
            Field('YearPublished', 'integer'),
            Field('YearWritten', 'integer'),
            Field('IsHidden', 'boolean', default=False))


db.define_table('WORK_TR',
			Field('WorkID', 'reference WORK', required=True),
			Field('LanguageID', 'reference LANGUAGE', required=True),
			Field('WorkName', 'string', length=1024, required=True),
			Field('WorkSubtitle', 'string', length=1024),
			Field('WorkDescription', 'text'),
			Field('WikipediaLink', 'string', length=256),
			Field('WorkNote', 'text'),
			Field('SubmitterID', 'reference USER', required=True),
			Field('SubmissionDate', 'datetime', default=datetime.now()))


db.define_table('AUTHOR',
			Field('YearBorn', 'integer'),
			Field('YearDied', 'integer'),
			Field('IsHidden', 'boolean', default=False))
			

db.define_table('AUTHOR_TR',
			Field('AuthorID', 'reference AUTHOR', required=True),
			Field('LanguageID', 'reference LANGUAGE', required=True),
			Field('FirstName', 'string', length=128),
			Field('MiddleName', 'string', length=128),
			Field('LastName', 'string', length=128),
			Field('AKA', 'list:string'),
			Field('DisplayName', 'string', length=512),
			Field('Biography', 'text'),
			Field('WikipediaLink', 'string', length=256),
			Field('SubmitterID', 'reference USER', required=True),
			Field('SubmissionDate', 'datetime', default=datetime.now()))


db.define_table('QUOTE_WORK',
			Field('QuoteID', 'reference QUOTE', required=True),
			Field('WorkID', 'reference WORK', required=True))


db.define_table('WORK_AUTHOR',
			Field('WorkID', 'reference WORK', required=True),
			Field('AuthorID', 'reference AUTHOR', required=True))


db.define_table('TRANSLATION',
			Field('OriginalQuoteID', 'reference QUOTE'),
			Field('TranslatedQuoteID', 'reference QUOTE'),
			Field('TranslatorID', 'reference AUTHOR'))




## after defining tables, uncomment below to enable auditing and storing old copies
# auth.enable_record_versioning(db)
