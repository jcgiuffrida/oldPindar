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
        #Field('Note', 'text', label='Context or additional information',
        #		requires = IS_LENGTH(maxsize=4096)),
		submit_button='Add quote!', table_name='QUOTE')
	
	add_author_tr = SQLFORM.factory(
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
					[IS_EMPTY_OR(IS_MATCH('(https://|http://)?[a-z]{2}'\
					'\.wikipedia\.org/wiki/.{1,}')), 
					IS_LENGTH(maxsize=256)]),
			Field('YearBorn', 'integer', label='Year born', 
					requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
			Field('YearDied', 'integer', label='Year died',
					requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
			submit_button='Add author', table_name='AUTHOR_TR')
	
	add_work_tr = SQLFORM.factory(
			Field('WorkName', 'string', label='Name of work',
					requires = [IS_NOT_EMPTY(), IS_LENGTH(maxsize=1024)]),
			Field('WorkSubtitle', 'string', label='Subtitle',
					requires = IS_LENGTH(maxsize=1024)),
			Field('WorkDescription', 'text', label='Description of work',
					requires = IS_LENGTH(maxsize=4096)),
			Field('WikipediaLink', 'string', label='Link to Wikipedia page',
					requires = [IS_EMPTY_OR(IS_MATCH('(https://|http://)?[a-z]{2}'\
					'\.wikipedia\.org/wiki/.{1,}')), IS_LENGTH(maxsize=256)]),
			Field('WorkNote', 'text', label='Context or additional information',
					requires = IS_LENGTH(maxsize=4096)),
			Field('YearPublished', 'integer', label='Year published',
				requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
            Field('YearWritten', 'integer', label='Year written (if different)',
				requires = IS_EMPTY_OR(IS_INT_IN_RANGE(-5000,2050))),
			Field('Author_Tr_ID', 'integer'), 
			submit_button='Add work', table_name='WORK_TR')
	
	author_js = SCRIPT('jQuery("#form_author_tr").hide();$("#work_tr").hide();', _type="text/javascript")
	work_js = SCRIPT('jQuery("#form_work_tr").hide();', _type="text/javascript")
	if form_quote.validate():
		display_authors = db((db.AUTHOR_TR.LanguageID==request.vars.QuoteLanguageID)).\
				select(db.AUTHOR_TR.DisplayName, db.AUTHOR_TR.id)
		response.flash = 'quote accepted'
	elif form_quote.errors:
		response.flash = 'form has errors'
	debug = ''
	
	if add_author_tr.validate():
		# add AUTHOR
		author_id = db.AUTHOR.insert(**db.AUTHOR._filter_fields(add_author_tr.vars))
		add_author_tr.vars.AuthorID = author_id
		# add AUTHOR_TR
		add_author_tr.vars.LanguageID = 1  # later, get user's language
		add_author_tr.vars.SubmitterID = 1  # later, grab user from form_quote
		author_tr_id = db.AUTHOR_TR.insert(**db.AUTHOR_TR._filter_fields(\
			add_author_tr.vars))
		
		author_js = SCRIPT('jQuery("#form_author_tr").fadeOut("fast");' \
			'$("#work_tr").fadeIn("fast");' \
			'$("#author_target").html("<input style=\'display:none\'' \
			'name=\'author_selection\'></input>");$("#author_target input").val(' + \
			str(author_id) + ');$("#author_tr>input").val("' + \
			add_author_tr.vars.DisplayName + '");$("#work_tr").fadeIn("fast");', 
			_type="text/javascript")
		response.flash = 'author added'
	elif add_author_tr.errors:
		author_js = SCRIPT('jQuery("#form_author_tr").show();', _type="text/javascript")
		response.flash = 'form has errors'
	
	if add_work_tr.validate():
		# add WORK
		work_id = db.WORK.insert(**db.WORK._filter_fields(add_work_tr.vars))
		add_work_tr.vars.WorkID = work_id
		# add WORK_TR
		add_work_tr.vars.LanguageID = 1  # later, get user's language
		add_work_tr.vars.SubmitterID = 1  # later, grab user from form_quote
		work_tr_id = db.WORK_TR.insert(**db.WORK_TR._filter_fields(\
			add_work_tr.vars))
		
		work_js = SCRIPT('jQuery("#form_work_tr").fadeOut("fast");' \
			'$("#work_target").html(<input style=\'display:none\'' \
			'name=\'work_selection\'></input>");$("#work_target input").val(' + \
			str(work_id) + ');$("#work_tr>input").val("' + \
			add_work_tr.vars.WorkName + '");$("#submit_button").fadeIn("fast");',
			_type="text/javascript")
		response.flash = 'work added'
	elif add_work_tr.errors:
		author_display_row = db(db.AUTHOR_TR.id==add_work_tr.vars.Author_Tr_ID).\
			select(db.AUTHOR_TR.DisplayName)
		for row in author_display_row:
			author_display = row.DisplayName
		work_js = SCRIPT('$("#work_tr").show();jQuery("#form_work_tr").show();' \
			'$("#author_target").html("<input style=\'display:none\' ' \
			'name=\'author_selection\'></input>");' \
			'$("#author_target input").val("' + str(add_work_tr.vars.Author_Tr_ID) +
			'");$("#author_tr>input").val("' + author_display + '");', 
			_type="text/javascript")
		response.flash = 'form has errors' + str(add_work_tr.vars.Author_Tr_ID)
	
	return dict(form_quote=form_quote, add_author_tr=add_author_tr, author_js=author_js,
		add_work_tr=add_work_tr, work_js=work_js, debug=debug)


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


def languages():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.LANGUAGE, user_signature=False)
	return locals()
