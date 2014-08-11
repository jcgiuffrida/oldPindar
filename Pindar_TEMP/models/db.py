# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['mysql', 'postgres'])
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

from datetime import datetime


## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

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

###---------------------- LANGUAGE

db.define_table('LANGUAGE',
         Field('LanguageCode', 'string', length=3, label='Two-letter code'),
         Field('EnglishName', 'string', length=64, label='English name'),
         Field('NativeName', 'string', length=64, required=True, label='Native name'))

db.LANGUAGE.LanguageCode.requires = IS_LENGTH(minsize=2, maxsize=3)
db.LANGUAGE.EnglishName.requires = IS_LENGTH(minsize=2, maxsize=64)
db.LANGUAGE.NativeName.requires = [IS_NOT_EMPTY(), IS_LENGTH(minsize=2, maxsize=64)]


###---------------------- QUOTE

db.define_table('QUOTE',
            Field('Text', 'text', required=True),
            Field('created_by', 'reference auth_user', default=auth.user_id,
                    label= 'submitter'),
            Field('SubmissionDate', 'datetime', default=datetime.now(), writable=False,
            		label='Date submitted'),
            Field('QuoteLanguageID', 'reference LANGUAGE', required=True, 
            		default=1, label='Language'), # temporary default for testing purposes
            Field('IsOriginalLanguage', 'boolean', label='Quote is in original language'),
            Field('IsDeleted', 'boolean', default=False, readable=False, writable=False),
            Field('Note', 'text', label='Context or additional information'))

db.QUOTE.Text.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.QUOTE.Text)]
db.QUOTE.SubmissionDate.requires = IS_DATETIME()
db.QUOTE.QuoteLanguageID.requires = IS_IN_DB(db, db.LANGUAGE.id, '%(NativeName)s')
db.QUOTE.Note.requires = IS_LENGTH(maxsize=4096)

###---------------------- WORK

### note: it should not be possible to enter a WORK without joining it to a WORK_TR. same with authors

db.define_table('WORK',
            Field('YearPublished', 'integer', label='Year published'),
            Field('YearWritten', 'integer', label='Year written (if different)'),
            Field('IsHidden', 'boolean', default=False, readable=False, writable=False))

db.WORK.YearPublished.requires = IS_INT_IN_RANGE(-5000,2050)
db.WORK.YearWritten.requires = IS_INT_IN_RANGE(-5000,2050)

###---------------------- WORK_TR

db.define_table('WORK_TR',
			Field('WorkID', 'reference WORK', required=True),
			Field('LanguageID', 'reference LANGUAGE', required=True, 
					label='Language of this work or translation'),
			Field('WorkName', 'string', length=1024, required=True,
					label='Name of work'),
			Field('WorkSubtitle', 'string', length=1024, 
					label='Subtitle'),
			Field('WorkDescription', 'text',
					label='Description of work'),
			Field('WikipediaLink', 'string', length=256,
					label='Link to Wikipedia page'),
			Field('WorkNote', 'text',
					label='Context or additional information'),
            Field('created_by', 'reference auth_user', default=auth.user_id,
                    label= 'User'),
			Field('SubmissionDate', 'datetime', default=datetime.now(), writable=False,
					label='Date submitted'))


auth.settings.extra_fields['auth_user']= [
    Field('QUOTE_ADDED', 'reference QUOTE'),
    Field('WORK_ADDED', 'reference WORK'),
    Field('AUTHOR_ADDED', 'reference AUTHOR')]

db.WORK_TR.WorkID.requires = IS_IN_DB(db, db.WORK.id, '%(id)s (%(YearPublished)s)')
db.WORK_TR.LanguageID.requires = IS_IN_DB(db, db.LANGUAGE.id, '%(NativeName)s')
db.WORK_TR.WorkName.requires = [IS_NOT_EMPTY(), IS_LENGTH(maxsize=1024)]
db.WORK_TR.WorkSubtitle.requires = IS_LENGTH(maxsize=1024)
db.WORK_TR.WorkDescription.requires = IS_LENGTH(maxsize=4096)
db.WORK_TR.WikipediaLink.requires = \
		[IS_MATCH('^(https://|http://)?[a-z]{2}\.wikipedia\.org/wiki/.{1,}'), 
		 IS_LENGTH(maxsize=256)]
db.WORK_TR.WorkNote.requires = IS_LENGTH(maxsize=4096)
db.WORK_TR.SubmissionDate.requires = IS_DATETIME()

###---------------------- AUTHOR

db.define_table('AUTHOR',
			Field('YearBorn', 'integer'),
			Field('YearDied', 'integer'),
			Field('IsHidden', 'boolean', default=False, readable=False, writable=False))

db.AUTHOR.YearBorn.requires = IS_INT_IN_RANGE(-5000,2050)
db.AUTHOR.YearDied.requires = IS_INT_IN_RANGE(-5000,2050)

###---------------------- AUTHOR_TR

db.define_table('AUTHOR_TR',
			Field('AuthorID', 'reference AUTHOR', required=True),
			Field('LanguageID', 'reference LANGUAGE', required=True,
					label='Your language'),
			Field('FirstName', 'string', length=128,
					label='First name'),
			Field('MiddleName', 'string', length=128,
					label='Middle name'),
			Field('LastName', 'string', length=128,
					label='Last name'),
			Field('AKA', 'list:string',
					label='Other names'),
			Field('DisplayName', 'string', length=512, required=True, 
					label='Default name'),
			Field('Biography', 'text'),
			Field('WikipediaLink', 'string', length=256, 
					label='Link to Wikipedia page'),
			Field('created_by', 'reference auth_user', default=auth.user_id,
                    label= 'User'),
			Field('SubmissionDate', 'datetime', default=datetime.now(), writable=False,
					label='Date submitted'))

db.AUTHOR_TR.AuthorID.requires = IS_IN_DB(
						db, db.AUTHOR.id, '%(id)s (%(YearBorn)s-%(YearDied)s)')
db.AUTHOR_TR.LanguageID.requires = IS_IN_DB(db, db.LANGUAGE.id, '%(NativeName)s')
db.AUTHOR_TR.FirstName.requires = IS_LENGTH(maxsize=128)
db.AUTHOR_TR.MiddleName.requires = IS_LENGTH(maxsize=128)
db.AUTHOR_TR.LastName.requires = IS_LENGTH(maxsize=128)
db.AUTHOR_TR.AKA.requires = IS_LIST_OF(IS_LENGTH(maxsize=256))
db.AUTHOR_TR.DisplayName.requires = [IS_NOT_EMPTY(), IS_LENGTH(maxsize=512)]
db.AUTHOR_TR.Biography.requires = IS_LENGTH(maxsize=8192)
db.AUTHOR_TR.WikipediaLink.requires = \
		[IS_MATCH('^(https://|http://)?[a-z]{2}\.wikipedia\.org/wiki/.{1,}'), 
		 IS_LENGTH(maxsize=256)]
db.AUTHOR_TR.SubmissionDate.requires = IS_DATETIME()

###---------------------- QUOTE_WORK

db.define_table('QUOTE_WORK',
			Field('QuoteID', 'reference QUOTE', required=True),
			Field('WorkID', 'reference WORK', required=True),
            Field('created_by', 'reference auth_user', default=auth.user_id))

db.QUOTE_WORK.QuoteID.requires = IS_IN_DB(db, db.QUOTE.id, '%(Text)s')
db.QUOTE_WORK.WorkID.requires = IS_IN_DB(db, db.WORK.id, '%(id)s (%(YearPublished)s)')


###---------------------- WORK_AUTHOR

db.define_table('WORK_AUTHOR',
			Field('WorkID', 'reference WORK', required=True),
			Field('AuthorID', 'reference AUTHOR', required=True))

db.WORK_AUTHOR.AuthorID.requires = IS_IN_DB(db, db.AUTHOR.id, 
									'%(id)s (%(YearBorn)s-%(YearDied)s)')
db.WORK_AUTHOR.WorkID.requires = IS_IN_DB(db, db.WORK.id, '%(id)s (%(YearPublished)s)')

###---------------------- TRANSLATION (fill out later)

db.define_table('TRANSLATION',
			Field('OriginalQuoteID', 'reference QUOTE'),
			Field('TranslatedQuoteID', 'reference QUOTE'),
			Field('TranslatorID', 'reference AUTHOR'))

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
