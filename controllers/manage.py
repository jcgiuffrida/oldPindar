# -*- coding: utf-8 -*-


def add_quote():
	"""
	*** for testing purposes only ***
	*** does not require user authorization ***
	"""
	form_quote = SQLFORM.factory(
		Field('Text', 'text', requires = [IS_NOT_EMPTY(), 
				IS_NOT_IN_DB(db, db.QUOTE.Text)], label=''),
        Field('QuoteLanguageID', 'reference LANGUAGE', 
            	default=1, label='', 
            	requires = IS_IN_DB(db, db.LANGUAGE.id, '%(LanguageCode)s', 
            	orderby=db.LANGUAGE.id)), 
        Field('IsOriginalLanguage', 'boolean', label='Quote is in original language'),
        Field('DisplayName', 'string', label=''), 
		Field('FirstName', 'string', label=''), 
		Field('MiddleName', 'string', label=''),
		Field('LastName', 'string', label=''),
		Field('AKA', 'list:string', label=''),
		Field('Biography', 'text', label=''), 
		Field('AuthorWikipediaLink', 'string', label=''),# requires = 
		Field('YearBorn', 'integer', label=''), 
		Field('YearDied', 'integer', label=''),
		Field('WorkName', 'string', label=''),
		Field('WorkSubtitle', 'string', label=''),
		Field('WorkDescription', 'text', label=''),
		Field('WorkWikipediaLink', 'string', label=''),
		Field('WorkNote', 'text', label=''),
		Field('YearPublished', 'integer', label=''),
        Field('YearWritten', 'integer', label=''),
		Field('Note', 'string', label=''),
		Field('AuthorTrID', 'integer'),
		Field('WorkTrID', 'integer'),
		col3={'AuthorWikipediaLink': \
			A(INPUT(_type="button",value="?"), _href='', 
				_id='authorWikiLink', _target='blank'),
			  'WorkWikipediaLink': \
			A(INPUT(_type="button",value="?"), _href='', 
				_id='workWikiLink', _target='blank'),
			  'YearBorn': 'Year born',
			  'YearDied': 'Year died',
			  'YearPublished': 'Publication year',
			  'YearWritten': 'Year written (if different)'},
		submit_button='Add quote!', table_name='QUOTE')
	
	author_lookup = TR(LABEL(''),
					INPUT(_name="author_lookup", _type="text", 
					_id='QUOTE_Author_Lookup', _placeholder='Author'), _id='QUOTE_Author_Lookup__row')
	form_quote[0].insert(6, author_lookup)
	
	work_lookup = TR(LABEL(''),
					INPUT(_name="work_lookup", _type="text", 
					_id='QUOTE_Work_Lookup', _placeholder='Source'), _id='QUOTE_Work_Lookup__row')
	form_quote[0].insert(16, work_lookup)
	
	author_submit = TR(LABEL(''),TD(INPUT(_name='Author_Submit', _value='Add author', 
			_id='QUOTE_Author_Submit', _type='submit'), 
			INPUT(_name='Author_Cancel', _value='Cancel', 
			_id='QUOTE_Author_Cancel', _type='button')), _id='QUOTE_Author_Submit__row'),
	form_quote[0].insert(16, author_submit)
	
	work_submit = TR(LABEL(''),TD(INPUT(_name='Work_Submit', _value='Add work', 
			_id='QUOTE_Work_Submit', _type='submit'), 
			INPUT(_name='Work_Cancel', _value='Cancel', 
			_id='QUOTE_Work_Cancel', _type='button')), _id='QUOTE_Work_Submit__row')
	form_quote[0].insert(25, work_submit)
	
	quote_submit = TR(LABEL(''),INPUT(_name='Quote_Submit', _value='Add quote!', 
			_id='QUOTE_Quote_Submit', _type='submit'), _id='QUOTE_Quote_Submit__row')
	form_quote[0].insert(26, quote_submit)
	
	# intentionally no way to submit the data here
	
	debug=''
		
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
		request.vars.author_lookup + '</td><td><em>Create new ' \
			'author</em></td></tr>'
	response += '</tbody></table>'
	return response


def author_submit():
	request.vars.WikipediaLink = request.vars.AuthorWikipediaLink
	request.vars.LanguageID = 1
	request.vars.AuthorID = int(db.AUTHOR.insert(**db.AUTHOR._filter_fields(request.vars)))
	AuthorTrID = db.AUTHOR_TR.insert(**db.AUTHOR_TR._filter_fields(request.vars))
	response.flash='Added author: ' + request.vars.DisplayName
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
		request.vars.work_lookup + '</td><td><em>Create new work</em></td></tr>'
	response += '</tbody></table>'
	return response


def work_submit():
	request.vars.WikipediaLink = request.vars.WorkWikipediaLink
	request.vars.LanguageID = 1
	request.vars.WorkID = int(db.WORK.insert(**db.WORK._filter_fields(request.vars)))
	WorkTrID = db.WORK_TR.insert(**db.WORK_TR._filter_fields(request.vars))
	tmp = db((db.AUTHOR_TR.id==request.vars.AuthorTrID) & 
			 (db.AUTHOR.id==db.AUTHOR_TR.AuthorID)).select(db.AUTHOR.id)
	for row in tmp:
		request.vars.AuthorID = row.id
	Work_Author_ID = db.WORK_AUTHOR.insert(**db.WORK_AUTHOR._filter_fields(request.vars))
	response.flash='Added work: ' + request.vars.WorkName
	return 'jQuery("#QUOTE_WorkTrID").val("' + str(WorkTrID) + '");'


def quote_submit():
	request.vars.QuoteID = \
		db.QUOTE.insert(**db.QUOTE._filter_fields(request.vars))
	tmp = db((db.WORK_TR.id==request.vars.WorkTrID) & 
			 (db.WORK.id==db.WORK_TR.WorkID)).select(db.WORK.id)
	for row in tmp:
		request.vars.WorkID = row.id
	Quote_Work_ID = \
		db.QUOTE_WORK.insert(**db.QUOTE_WORK._filter_fields(request.vars))
	response.flash='Added quote!'
	return ''


def quotes():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.QUOTE, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('QUOTE', ids))])
	return locals()


def works():
	"""
	*** for testing purposes only***
	"""
	grid1 = SQLFORM.grid(db.WORK, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('WORK', ids))])
	grid2 = SQLFORM.grid(db.WORK_TR, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('WORK_TR', ids))])
	return locals()



def authors():
	"""
	*** for testing purposes only***
	"""
	grid1 = SQLFORM.grid(db.AUTHOR, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('AUTHOR', ids))])
	grid2 = SQLFORM.grid(db.AUTHOR_TR, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('AUTHOR_TR', ids))])
	return locals()


def connections():
	"""
	*** for testing purposes only***
	"""
	grid1 = SQLFORM.grid(db.QUOTE_WORK, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('QUOTE_WORK', ids))])
	grid2 = SQLFORM.grid(db.WORK_AUTHOR, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('WORK_AUTHOR', ids))])
	return locals()


def languages():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.LANGUAGE, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('LANGUAGE', ids))])
	return locals()
	

#@auth.requires_login()
def users():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.auth_user, user_signature=False)
	return locals()


def flags():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.FLAG, user_signature=False,
		selectable=[('Delete', lambda ids: delete_multiple('FLAG', ids))])
	return locals()


def delete_multiple(table, ids):
	if table == 'QUOTE':
		to_delete = db(db.QUOTE.id.belongs(ids))
		to_delete.delete()
	elif table == 'WORK':
		to_delete = db(db.WORK.id.belongs(ids))
		to_delete.delete()
	elif table == 'WORK_TR':
		to_delete = db(db.WORK_TR.id.belongs(ids))
		to_delete.delete()
	elif table == 'AUTHOR':
		to_delete = db(db.AUTHOR.id.belongs(ids))
		to_delete.delete()
	elif table == 'AUTHOR_TR':
		to_delete = db(db.AUTHOR_TR.id.belongs(ids))
		to_delete.delete()
	elif table == 'WORK_AUTHOR':
		to_delete = db(db.WORK_AUTHOR.id.belongs(ids))
		to_delete.delete()
	elif table == 'QUOTE_WORK':
		to_delete = db(db.QUOTE_WORK.id.belongs(ids))
		to_delete.delete()
	elif table == 'LANGUAGE':
		to_delete = db(db.LANGUAGE.id.belongs(ids))
		to_delete.delete()
	elif table == 'FLAG':
		to_delete = db(db.FLAG.id.belongs(ids))
		to_delete.delete()

