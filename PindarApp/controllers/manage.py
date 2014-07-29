# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def quotes():
	"""
	*** for testing purposes only***
	"""
	grid = SQLFORM.grid(db.QUOTE, user_signature=False)
	return locals()


def add_quote():
	"""
	*** for testing purposes only***
	*** does not require user authorization ***
	"""
	form = SQLFORM(db.QUOTE, user_signature=False,
		fields=['Text', 'SubmitterID', 'QuoteLanguageID', 'IsOriginalLanguage', 'Note'],
		labels={'Text': 'Quote', 'SubmitterID': 'User', 'QuoteLanguageID': 'Language of quote', 'IsOriginalLanguage': 'Check if this is the quote\'s original language', 'Note': 'Add a note'},
		submit_button='Add quote!')
	if form.process().accepted:
		response.flash = 'form accepted'
	elif form.errors:
		response.flash = 'form has errors'
	return dict(form=form)


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

