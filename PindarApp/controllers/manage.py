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
		Field('FirstName', 'string', label='First name'), 
#				requires = IS_LENGTH(maxsize=128)),
		Field('MiddleName', 'string', label='Middle name'),
#				requires = IS_LENGTH(maxsize=128)),
		Field('LastName', 'string', label='Last name'),
#				requires = IS_LENGTH(maxsize=128)),
		Field('AKA', 'list:string', label='Other names'),
#				requires=IS_LIST_OF(IS_LENGTH(maxsize=256))),
		Field('DisplayName', 'string', label='Default name'), 
#				requires=[IS_LENGTH(maxsize=512)]),
		Field('Biography', 'text'), 
#				requires=IS_LENGTH(maxsize=8192)),
		Field('AuthorWikipediaLink', 'string', label='Link to Wikipedia page'),# requires = 
#				[IS_EMPTY_OR(IS_MATCH('(https://|http://)?[a-z]{2}'\
#				'\.wikipedia\.org/wiki/.{1,}')), 
#				IS_LENGTH(maxsize=256)]),
		Field('YearBorn', 'integer', label='Year born'), 
#				requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
		Field('YearDied', 'integer', label='Year died'),
#				requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
		Field('WorkName', 'string', label='Name of work'),
#				requires = [IS_NOT_EMPTY(), IS_LENGTH(maxsize=1024)]),
		Field('WorkSubtitle', 'string', label='Subtitle'),
#				requires = IS_LENGTH(maxsize=1024)),
		Field('WorkDescription', 'text', label='Description of work'),
#				requires = IS_LENGTH(maxsize=4096)),
		Field('WorkWikipediaLink', 'string', label='Link to Wikipedia page'),
#				requires = [IS_EMPTY_OR(IS_MATCH('(https://|http://)?[a-z]{2}'\
#				'\.wikipedia\.org/wiki/.{1,}')), IS_LENGTH(maxsize=256)]),
		Field('WorkNote', 'text', label='Context or additional information'),
#				requires = IS_LENGTH(maxsize=4096)),
		Field('YearPublished', 'integer', label='Year published'),
#				requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
        Field('YearWritten', 'integer', label='Year written (if different)'),
#				requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
		Field('AuthorTrID', 'integer'),
		Field('WorkTrID', 'integer'),
		submit_button='Add quote!', table_name='QUOTE')
	
	author_lookup = TR(LABEL('Select Author'),
					INPUT(_name="author_lookup", _type="text", 
					_id='QUOTE_Author_Lookup'), _id='QUOTE_Author_Lookup__row')
	form_quote[0].insert(6, author_lookup)
	
	work_lookup = TR(LABEL('Select Work'),
					INPUT(_name="work_lookup", _type="text", 
					_id='QUOTE_Work_Lookup'), _id='QUOTE_Work_Lookup__row')
	form_quote[0].insert(16, work_lookup)
	
	author_submit = TR(INPUT(_name='Author_Submit', _value='Add author', 
			_id='QUOTE_Author_Submit', _type='submit'), _id='QUOTE_Author_Submit__row')
	form_quote[0].insert(16, author_submit)
	
	work_submit = TR(INPUT(_name='Work_Submit', _value='Add work', 
			_id='QUOTE_Work_Submit', _type='submit'), _id='QUOTE_Work_Submit__row')
	form_quote[0].insert(25, work_submit)
	
	quote_submit = TR(INPUT(_name='Quote_Submit', _value='Add quote!', 
			_id='QUOTE_Quote_Submit', _type='submit'), _id='QUOTE_Quote_Submit__row')
	form_quote[0].insert(26, quote_submit)
	
	debug=''
	
	if form_quote.validate():
		form_quote.vars.QuoteID = \
			db.QUOTE.insert(**db.QUOTE._filter_fields(form_quote.vars))
		tmp = db((db.WORK_TR.id==form_quote.vars.WorkTrID) & 
				 (db.WORK.id==db.WORK_TR.WorkID)).\
			  	 select(db.WORK.id)
		for row in tmp:
			form_quote.vars.WorkID = row.id
		
		Quote_Work_ID = \
			db.QUOTE_WORK.insert(**db.QUOTE_WORK._filter_fields(form_quote.vars))
		
		debug = Quote_Work_ID
		
		response.flash = 'quote accepted'
	elif form_quote.errors:
		debug = db.WORK_AUTHOR._filter_fields(form_quote.vars)
		
		response.flash = 'form has errors'
		
	return dict(form_quote=form_quote, debug=debug)


def author_query():
	# should add a line here disqualifying query if it's just the '%' character
	query = '%' + request.vars.author_lookup + '%'
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
	response = '<table><thead>'
	response += '<tr><td><h4>Search results</h4></td></tr></thead>'
	if len(display_authors)>0:
		response += '<tbody>'
		for row in display_authors:
			response += '<tr class="author_query_result" id="' + str(row.AUTHOR_TR.id)+\
		 		'"><td>' + \
				row.AUTHOR_TR.DisplayName + '</td><td>' + \
				str(row.AUTHOR.YearBorn) + ' - ' + str(row.AUTHOR.YearDied) + \
				'</td></tr>'
	response += '<tr class="author_query_result" id="0"><td>' + \
		request.vars.author_lookup + '...</td><td><em>Create new author</em></td></tr>'
	response += '</tbody></table>'
	return response


def author_submit():
	request.vars.WikipediaLink = request.vars.AuthorWikipediaLink
	request.vars.LanguageID = 1
	request.vars.AuthorID = int(db.AUTHOR.insert(**db.AUTHOR._filter_fields(request.vars)))
	AuthorTrID = db.AUTHOR_TR.insert(**db.AUTHOR_TR._filter_fields(request.vars))
	return 'jQuery("#QUOTE_AuthorTrID").val("' + str(AuthorTrID) + '");'

def lang_changed():
	#rows = db().select(cache=(cache.ram, 10),cacheable=True)
	return 'x'

	
def work_query():
	# should add a line here disqualifying query if it's just the '%' character
	query = '%' + request.vars.work_lookup + '%'
	if len(query) < 4:
		return ''
	selected_author = request.vars.AuthorTrID
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
	response = '<table><thead>'
	response += '<tr><td><h4>Search results</h4></td></tr></thead>'
	if len(display_works)>0:
		response += '<tbody>'
		for row in display_works:
			response += '<tr class="work_query_result" id="' + str(row.WORK_TR.id)+\
		 		'"><td>' + \
				row.WORK_TR.WorkName + '</td><td>' + \
				row.WORK_TR.WorkSubtitle + '</td><td>' + \
				str(row.WORK.YearPublished) + \
				'</td></tr>'
	response += '<tr class="work_query_result" id="0"><td>' + \
		request.vars.work_lookup + '...</td><td><em>Create new work</em></td></tr>'
	response += '</tbody></table>'
	return response


def work_submit():
	request.vars.WikipediaLink = request.vars.WorkWikipediaLink
	request.vars.LanguageID = 1
	request.vars.WorkID = int(db.WORK.insert(**db.WORK._filter_fields(request.vars)))
	WorkTrID = db.WORK_TR.insert(**db.WORK_TR._filter_fields(request.vars))
	return 'jQuery("#QUOTE_WorkTrID").val("' + str(WorkTrID) + '");'


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


def languages():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.LANGUAGE, user_signature=False)
	return locals()
