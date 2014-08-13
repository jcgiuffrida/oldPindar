# -*- coding: utf-8 -*-


def show(): 
   """
   test SQL query and display
   """
   query1 = db((db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
   	(db.QUOTE_WORK.WorkID==db.WORK._id) & 
   	(db.WORK._id==db.WORK_TR.WorkID) & 
   	(db.QUOTE.QuoteLanguageID==db.LANGUAGE._id) & 
   	(db.WORK_AUTHOR.WorkID==db.WORK._id) & 
   	(db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
   	(db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.QUOTE.Text,
   		db.LANGUAGE.EnglishName, db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName,
   		db.AUTHOR.YearBorn, db.AUTHOR.YearDied, db.WORK.YearPublished,
   		db.QUOTE.IsOriginalLanguage)
   langs = db(db.LANGUAGE).select(db.LANGUAGE._id, db.LANGUAGE.NativeName)
   return dict(results1=query1, langs=langs) 


def text_query():
	lang = 1 if request.vars.lang=='' else int(request.vars.lang)
	if len(request.vars.query) < 2:
		return ''
	query = '%' + request.vars.query + '%'
	if lang == 0:
		results = db((db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
		(db.QUOTE_WORK.WorkID==db.WORK._id) & 
		(db.WORK._id==db.WORK_TR.WorkID) & 
		(db.WORK._id==db.WORK_AUTHOR.WorkID) & 
		(db.WORK_AUTHOR.AuthorID==db.AUTHOR_TR.AuthorID) & 
		(db.QUOTE.Text.like(query))).select(db.QUOTE.Text, 
											db.AUTHOR_TR.DisplayName, 
											db.WORK_TR.WorkName, 
											db.WORK_TR.id, 
											groupby=db.QUOTE.Text)
	else:
		results = db((db.QUOTE.QuoteLanguageID==lang) & 
		(db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
		(db.QUOTE_WORK.WorkID==db.WORK._id) & 
		(db.WORK._id==db.WORK_TR.WorkID) & 
		(db.WORK._id==db.WORK_AUTHOR.WorkID) & 
		(db.WORK_AUTHOR.AuthorID==db.AUTHOR_TR.AuthorID) & 
		(db.QUOTE.Text.like(query))).select(db.QUOTE.Text, 
											db.AUTHOR_TR.DisplayName, 
											db.WORK_TR.WorkName, 
											db.WORK_TR.id, 
											groupby=db.QUOTE.Text)
   	
   	response = '<h3>Example query (text search)</h3>'
   	if len(results) == 0:
   		response += '<em>No results found.</em>'
   	for row in results:
		response += row.QUOTE.Text + '<br/>&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#888;">'
		response += row.AUTHOR_TR.DisplayName + ', <a href="data/read/WORK_TR/' + str(row.WORK_TR.id) + '"><em>'
		response += row.WORK_TR.WorkName + '</em></a></span><br/><br/>'
   	
   	return response



def index():
    """
    ***for testing purposes only***
    
    function to list data on the main page
   
    """
    return dict(quotes=SQLFORM.grid(db.QUOTE), authors=SQLFORM.grid(db.AUTHOR),
    	authors_tr=SQLFORM.grid(db.AUTHOR_TR), works=SQLFORM.grid(db.WORK),
    	works_tr=SQLFORM.grid(db.WORK_TR), users=SQLFORM.grid(db.auth_user), 
    	languages=SQLFORM.grid(db.LANGUAGE), translations=SQLFORM.grid(db.TRANSLATION))



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """	    
    # the below is from https://groups.google.com/forum/#!topic/web2py/okakKiDajNw
    if request.args[0]=='profile':
    	response.view='default/profile.html'
    	quotes_added = db((db.QUOTE.created_by==auth.user_id) & 
        	(db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
   			(db.QUOTE_WORK.WorkID==db.WORK._id) & 
   			(db.WORK._id==db.WORK_TR.WorkID) & 
   			(db.WORK_AUTHOR.WorkID==db.WORK._id) & 
   			(db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
   			(db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.QUOTE.Text,
   			db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName, db.QUOTE.created_on)
        authors_added = db((db.AUTHOR_TR.created_by==auth.user_id) & 
        	(db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.AUTHOR_TR.DisplayName,
   			db.AUTHOR_TR.created_on, db.AUTHOR.YearBorn, db.AUTHOR.YearDied)
        works_added = db((db.WORK_TR.created_by==auth.user_id) & 
        	(db.WORK._id==db.WORK_TR.WorkID) & 
   			(db.WORK_AUTHOR.WorkID==db.WORK._id) & 
   			(db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
   			(db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.WORK_TR.WorkName,
   			db.WORK.YearPublished, db.AUTHOR_TR.DisplayName, db.WORK_TR.created_on)
        quotes_edited = db((db.QUOTE.modified_by==auth.user_id) & 
        	(db.QUOTE.modified_on!=db.QUOTE.created_on) & # not the first edit
   			(db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
   			(db.QUOTE_WORK.WorkID==db.WORK._id) & 
   			(db.WORK._id==db.WORK_TR.WorkID) & 
   			(db.WORK_AUTHOR.WorkID==db.WORK._id) & 
   			(db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
   			(db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.QUOTE.Text,
   			db.QUOTE.modified_on, db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName)
    	return dict(form=auth(), quotes_added=quotes_added, authors_added=authors_added,
        	works_added=works_added, quotes_edited=quotes_edited)
    return dict(form=auth())  



@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


#@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
