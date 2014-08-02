# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def add_quote():
	"""
	*** for testing purposes only ***
	*** does not require user authorization ***
	"""
	langs = db(db.LANGUAGE).select(db.LANGUAGE._id, db.LANGUAGE.NativeName)
	options = []
	for row in langs:
		options.append(OPTION(row.NativeName, _value=row.id))
	form_quote = SQLFORM.factory(
		Field('Text', 'text', requires = [IS_NOT_EMPTY(), 
				IS_NOT_IN_DB(db, db.QUOTE.Text)]),
        Field('SubmitterID', 'reference USER', label='Submitter', 
            	default=1, requires = IS_IN_DB(db, db.USER.id, '%(UserName)s')),
        Field('SubmissionDate', 'datetime', default=datetime.now(), writable=False,
            	label='Date submitted', requires = IS_DATETIME()),
    	Field('QuoteLanguageID', 'reference LANGUAGE', 
            	default=1, label='Language', 
            	requires = IS_IN_DB(db, db.LANGUAGE.id, '%(NativeName)s')), 
        Field('IsOriginalLanguage', 'boolean', label='Quote is in original language'),
        Field('Note', 'text', label='Context or additional information',
        		requires = IS_LENGTH(maxsize=4096)),
		submit_button='Add quote!', table_name='QUOTE')
	
	
		

		
	if form_quote.validate():
		display_authors = db((db.AUTHOR_TR.LanguageID==request.vars.QuoteLanguageID)).\
				select(db.AUTHOR_TR.DisplayName, db.AUTHOR_TR.id)
		response.flash = 'quote accepted'
	elif form_quote.errors:
		response.flash = 'form has errors'
	return dict(form_quote=form_quote)


def author_query():
	lang = request.vars.QuoteLanguageID
	# should add a line here disqualifying query if it's just the '%' character
	query = '%' + request.vars.author_query + '%'
	if len(query) < 4:
		return ''
	display_authors = db((db.AUTHOR_TR.LanguageID==1) & # change 1 to lang, later
			(db.AUTHOR_TR.AuthorID==db.AUTHOR.id) & 
			((db.AUTHOR_TR.DisplayName.like(query)) | 
			 (db.AUTHOR_TR.FirstName.like(query)) | 
			 (db.AUTHOR_TR.MiddleName.like(query)) | 
			 (db.AUTHOR_TR.LastName.like(query)) | 
			 (db.AUTHOR_TR.AKA.like(query)))).select(
			db.AUTHOR_TR.DisplayName, db.AUTHOR.YearBorn, db.AUTHOR.YearDied,
			db.AUTHOR_TR.id, orderby=db.AUTHOR_TR.LastName)
	response = '<h4>Search results:</h4><br/>'
	response += '<table><tbody>'
	if len(display_authors)>0:
		response += '<table><tbody>'
		for row in display_authors:
			response += '<tr class="author_query_result" id="' + str(row.AUTHOR_TR.id)+\
		 		'"><td>' + \
				row.AUTHOR_TR.DisplayName + '</td><td>' + \
				str(row.AUTHOR.YearBorn) + ' - ' + str(row.AUTHOR.YearDied) + \
				'</td></tr>'
	response += '<tr class="author_query_result" id="0"><td>' + \
		request.vars.author_query + '...</td><td><em>Create new author</em></td></tr>'
	response += '<table><tbody>'
	return response


def lang_changed():
	#rows = db().select(cache=(cache.ram, 10),cacheable=True)
	return 'x'

def author_selected():
	if request.vars.authorid == "0":
		add_author_tr = SQLFORM.factory(
			Field('AuthorID', 'reference AUTHOR', requires = IS_IN_DB(
					db, db.AUTHOR.id, '%(id)s (%(YearBorn)s-%(YearDied)s)')),
			Field('LanguageID', 'reference LANGUAGE', label='Your language', 
					requires = IS_IN_DB(db, db.LANGUAGE.id, '%(NativeName)s')),
			Field('FirstName', 'string', label='First name', 
					requires = IS_LENGTH(maxsize=128)),
			Field('MiddleName', 'string', label='Middle name',
					requires = IS_LENGTH(maxsize=128)),
			Field('LastName', 'string', label='Last name',
					requires = IS_LENGTH(maxsize=128)),
			Field('AKA', 'list:string', label='Other names',
					requires=IS_LIST_OF(IS_LENGTH(maxsize=256))),
			Field('DisplayName', 'string', label='Default name', 
					requires=[IS_NOT_EMPTY(), IS_LENGTH(maxsize=512)]),
			Field('Biography', 'text', requires=IS_LENGTH(maxsize=8192)),
			Field('WikipediaLink', 'string', label='Link to Wikipedia page', requires = 
					[IS_MATCH('(https://|http://)?[a-z]{2}\.wikipedia\.org/wiki/.{1,}'), 
					IS_LENGTH(maxsize=256)]),
			Field('SubmitterID', 'reference USER', label='User', 
					requires = IS_IN_DB(db, db.USER.id, '%(UserName)s')),
			Field('SubmissionDate', 'datetime', default=datetime.now(), writable=False,
					label='Date submitted', requires = IS_DATETIME()),
			submit_button='', table_name='AUTHOR_TR')
		return add_author_tr
	else:
		return ''
	
	
def work_query():
	# should add a line here disqualifying query if it's just the '%' character
	query = '%' + request.vars.work_query + '%'
	if len(query) < 4:
		return ''
	selected_author = request.vars.author_selection
	display_works = db((db.AUTHOR_TR.id==selected_author) &
			(db.AUTHOR_TR.AuthorID==db.AUTHOR.id) & 
			(db.WORK_AUTHOR.AuthorID==db.AUTHOR.id) & 
			(db.WORK_AUTHOR.WorkID==db.WORK.id) & 
			(db.WORK.id==db.WORK_TR.WorkID) & 
			(db.WORK_TR.LanguageID==1) & # change to 'lang' later
			((db.WORK_TR.WorkName.like(query)) |
			 (db.WORK_TR.WorkSubtitle.like(query)))).select(
			db.WORK_TR.WorkName, db.WORK_TR.id, db.WORK.YearPublished,
			db.WORK.YearWritten, db.WORK_TR.WorkSubtitle, orderby=db.WORK_TR.WorkName)
	response = '<h4>Search results:</h4><br/>'
	response += '<table><tbody>'
	if len(display_works)>0:
		for row in display_works:
			response += '<tr class="work_query_result" id="' + str(row.WORK_TR.id)+\
		 		'"><td>' + \
				row.WORK_TR.WorkName + '</td><td>' + \
				row.WORK_TR.WorkSubtitle + '</td><td>' + \
				str(row.WORK.YearPublished) + \
				'</td></tr>'
	response += '<tr class="work_query_result" id="0"><td>' + \
		request.vars.work_query + '...</td><td><em>Create new work</em></td></tr>'
	response += '<table><tbody>'
	return response


def work_selected():
	if request.vars.workid == "0":
		add_work_tr = SQLFORM.factory(
			Field('AuthorID', 'reference AUTHOR', requires = IS_IN_DB(
					db, db.AUTHOR.id, '%(id)s (%(YearBorn)s-%(YearDied)s)')),
			Field('LanguageID', 'reference LANGUAGE', label='Your language', 
					requires = IS_IN_DB(db, db.LANGUAGE.id, '%(NativeName)s')),
			Field('FirstName', 'string', label='First name', 
					requires = IS_LENGTH(maxsize=128)),
			Field('MiddleName', 'string', label='Middle name',
					requires = IS_LENGTH(maxsize=128)),
			Field('LastName', 'string', label='Last name',
					requires = IS_LENGTH(maxsize=128)),
			Field('AKA', 'list:string', label='Other names',
					requires=IS_LIST_OF(IS_LENGTH(maxsize=256))),
			Field('DisplayName', 'string', label='Default name', 
					requires=[IS_NOT_EMPTY(), IS_LENGTH(maxsize=512)]),
			Field('Biography', 'text', requires=IS_LENGTH(maxsize=8192)),
			Field('WikipediaLink', 'string', label='Link to Wikipedia page', requires = 
					[IS_MATCH('(https://|http://)?[a-z]{2}\.wikipedia\.org/wiki/.{1,}'), 
					IS_LENGTH(maxsize=256)]),
			Field('SubmitterID', 'reference USER', label='User', 
					requires = IS_IN_DB(db, db.USER.id, '%(UserName)s')),
			Field('SubmissionDate', 'datetime', default=datetime.now(), writable=False,
					label='Date submitted', requires = IS_DATETIME()),
			submit_button='', table_name='AUTHOR_TR')
		return add_work_tr
	else:
		return ''

def quotes():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.QUOTE, user_signature=False)
	return locals()


def works():
	"""
	*** for testing purposes only***
	"""
	grid1 = SQLFORM.grid(db.WORK, user_signature=False)
	grid2 = SQLFORM.grid(db.WORK_TR, user_signature=False)
	return locals()



def authors():
	"""
	*** for testing purposes only***
	"""
	grid1 = SQLFORM.grid(db.AUTHOR, user_signature=False)
	grid2 = SQLFORM.grid(db.AUTHOR_TR, user_signature=False)
	return locals()


def connections():
	"""
	*** for testing purposes only***
	"""
	grid1 = SQLFORM.grid(db.QUOTE_WORK, user_signature=False)
	grid2 = SQLFORM.grid(db.WORK_AUTHOR, user_signature=False)
	return locals()


def users():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.USER, user_signature=False)
	return locals()
