# -*- coding: utf-8 -*-
import json
from gluon.tools import prettydate
import gluon.http
import random


def show(): 
   # for ratings: 
   # r = db.RATING.Rating.avg()
   # and in the query:     & 
   #    (db.RATING.QuoteID==db.QUOTE._id)).select(db.QUOTE.Text,
   #        db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName,
     #    db.QUOTE._id, db.AUTHOR_TR._id, db.WORK_TR._id, r, 
     #    groupby=db.QUOTE._id, orderby=~r)

   # this is the standard quotes query, ordered by rating
    r = db.RATING.Rating.avg()
    s = db.RATING.Rating.count()
    quotes = db((db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
            (db.QUOTE_WORK.WorkID==db.WORK._id) & 
            (db.WORK._id==db.WORK_TR.WorkID) & 
            (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
            (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
            (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(
            db.QUOTE.Text, db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName,
            db.QUOTE._id, db.AUTHOR_TR._id, db.WORK_TR._id, r, s, 
            left=db.RATING.on(db.RATING.QuoteID==db.QUOTE._id),
            groupby=db.QUOTE._id, orderby=~r|~s, limitby=(0,10))
    workcount = db.WORK_AUTHOR.AuthorID.count()
    authors = db((db.AUTHOR_TR.AuthorID==db.AUTHOR._id)).select(
            db.AUTHOR_TR.DisplayName, db.AUTHOR.YearBorn, 
            db.AUTHOR.YearDied, db.AUTHOR_TR._id, workcount, 
            left=db.WORK_AUTHOR.on(db.WORK_AUTHOR.AuthorID==db.AUTHOR._id),
            orderby=~workcount|db.AUTHOR_TR.LastName, limitby=(0,5), 
            groupby=db.AUTHOR.id)
    quotecount = db.QUOTE_WORK.QuoteID.count()
    works = db((db.WORK_TR.WorkID==db.WORK._id) & 
            (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
            (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
            (db.AUTHOR_TR.AuthorID==db.AUTHOR._id)).select(
            db.AUTHOR_TR.DisplayName, db.WORK.YearPublished, 
            db.WORK_TR.WorkName, db.WORK_TR._id, quotecount, 
            left=db.QUOTE_WORK.on(db.QUOTE_WORK.WorkID==db.WORK._id),
            orderby=~quotecount|db.WORK_TR.WorkName, limitby=(0,5), 
            groupby=db.WORK._id)
    return locals()



def index():
    # for now, just redirect to /show
    response.view=redirect(URL('default', 'show'))
    return locals()



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


# show user profile page
@auth.requires_login()
def users():
    user = db.auth_user(username=request.args(0)) or redirect(URL('error'))
    userid = user.id
    quotes_added = db((db.QUOTE.created_by==userid) & 
      (db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
        (db.QUOTE_WORK.WorkID==db.WORK._id) & 
        (db.WORK._id==db.WORK_TR.WorkID) & 
        (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
        (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
        (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.QUOTE.Text,
        db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName, db.QUOTE.created_on)
    authors_added = db((db.AUTHOR_TR.created_by==userid) & 
        (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.AUTHOR_TR.DisplayName,
        db.AUTHOR_TR.created_on, db.AUTHOR.YearBorn, db.AUTHOR.YearDied)
    
    works_added = db((db.WORK_TR.created_by==userid) & 
        (db.WORK._id==db.WORK_TR.WorkID) & 
        (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
        (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
        (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.WORK_TR.WorkName,
        db.WORK.YearPublished, db.AUTHOR_TR.DisplayName, db.WORK_TR.created_on)
    
    quotes_edited = db((db.QUOTE.modified_by==userid) & 
        (db.QUOTE.modified_on!=db.QUOTE.created_on) & # not the first edit
        (db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
        (db.QUOTE_WORK.WorkID==db.WORK._id) & 
        (db.WORK._id==db.WORK_TR.WorkID) & 
        (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
        (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
        (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(db.QUOTE.Text,
        db.QUOTE.modified_on, db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName)
    return dict(user=user, quotes_added=quotes_added, authors_added=authors_added,
            works_added=works_added, quotes_edited=quotes_edited)


# show the page for a quote
def quotes():
    # figure out what quote to display
    q = db.QUOTE(request.args(0))
    # if quote is invalid, return to home
    if not q:
        redirect(URL('default', 'show'))
    if auth.user:
        lang = auth.user.PrimaryLanguageID
    else:
        lang = 1  # default is english
    comment_count = db((db.COMMENT.QuoteID==request.args(0))).count()
    quote = db((db.QUOTE._id==request.args(0)) & 
            (db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
            (db.QUOTE_WORK.WorkID==db.WORK._id) & 
            (db.WORK._id==db.WORK_TR.WorkID) & 
            (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
            (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
            (db.AUTHOR_TR.AuthorID==db.AUTHOR._id) & 
            (db.AUTHOR_TR.LanguageID==lang) & 
            (db.WORK_TR.LanguageID==lang)).select(
            db.QUOTE.Text, db.QUOTE._id, db.WORK_TR.WorkName, 
            db.AUTHOR_TR.DisplayName, db.WORK_TR._id, db.AUTHOR_TR._id)
    return locals()


# unique page for each author
def authors():
    if auth.user:
        lang = auth.user.PrimaryLanguageID
    else:
        lang = 1  # default is english
    # what author?
    if request.args(0)=='all':
        workcount = db.WORK_AUTHOR.AuthorID.count()
        authors = db((db.AUTHOR_TR.AuthorID==db.AUTHOR._id) & 
                    (db.AUTHOR_TR.LanguageID==lang)).select(
                    db.AUTHOR_TR.DisplayName, db.AUTHOR_TR._id, 
                    db.AUTHOR.YearBorn, db.AUTHOR.YearDied, workcount, 
                    left=db.WORK_AUTHOR.on(db.AUTHOR.id==db.WORK_AUTHOR.AuthorID),
                    groupby=db.AUTHOR.id,
                    orderby=~workcount|db.AUTHOR_TR.LastName, limitby=(0,10))
        if request.vars['e']:
            response.flash='Author ' + request.vars['e'] + ' was not found'
        return locals()
    a = db.AUTHOR_TR(request.args(0))
    # if author is invalid, show all authors and an error message
    if not a:
        if not request.args(0):
            redirect(URL('Pindar/default', 'authors', 'all'))
        else:
            redirect(URL('Pindar/default', 'authors', 'all?e='+request.args(0)))
    try:
        author = db((db.AUTHOR_TR._id==request.args(0)) & 
            (db.AUTHOR_TR.AuthorID==db.AUTHOR._id)).select()
        author_id = author[0]['AUTHOR']['id']
    except KeyError:
        redirect(URL('Pindar/default', 'authors', 'all?e='+request.args(0)))
    quotecount = db.QUOTE_WORK.QuoteID.count()
    works = db((db.WORK_AUTHOR.AuthorID==author_id) & 
            (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
            (db.WORK._id==db.WORK_TR.WorkID) & 
            (db.WORK_TR.LanguageID==lang)).select(
            db.WORK.YearPublished, db.WORK.YearWritten, db.WORK.id,
            db.WORK_TR.id, db.WORK_TR.WorkName, db.WORK_TR.WorkSubtitle, 
            quotecount, 
            left=db.QUOTE_WORK.on(db.WORK.id==db.QUOTE_WORK.WorkID),
            groupby=db.WORK.id, orderby=~quotecount|db.WORK_TR.WorkName, 
            limitby=(0,10))
    quotes = db((db.WORK_AUTHOR.AuthorID==author_id) & 
            (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
            (db.WORK_TR.WorkID==db.WORK._id) & 
            (db.QUOTE_WORK.WorkID==db.WORK._id) & 
            (db.QUOTE_WORK.QuoteID==db.QUOTE._id) & 
            (db.QUOTE.QuoteLanguageID==lang)).select(
            orderby=~db.QUOTE.created_on, limitby=(0,10))
    return locals()


# unique page for each work
def works():
    if auth.user:
        lang = auth.user.PrimaryLanguageID
    else:
        lang = 1  # default is english# what work?
    quotecount = db.QUOTE_WORK.QuoteID.count()
    works = db((db.WORK_TR.WorkID==db.WORK._id) & 
                (db.WORK_TR.LanguageID==lang) & 
                (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
                (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
                (db.AUTHOR_TR.AuthorID==db.AUTHOR._id) & 
                (db.AUTHOR_TR.LanguageID==lang)).select(
                db.AUTHOR_TR.DisplayName, db.WORK.YearPublished, 
                db.WORK_TR.WorkName, db.WORK_TR._id, quotecount, 
                left=db.QUOTE_WORK.on(db.WORK.id==db.QUOTE_WORK.WorkID),
                groupby=db.WORK.id, orderby=~quotecount, limitby=(0,10))
    if request.args(0)=='all':
        if request.vars['e']:
            response.flash='Work ' + request.vars['e'] + ' was not found'
        return locals()
    w = db.WORK_TR(request.args(0))
    # if work is invalid, show all works and an error message
    if not w:
        if not request.args(0):
            redirect(URL('Pindar/default', 'works', 'all'))
        else:
            redirect(URL('Pindar/default', 'works', 'all?e='+request.args(0)))
    try:
        work = db((db.WORK_TR._id==request.args(0)) & 
            (db.WORK_TR.WorkID==db.WORK._id) & 
            (db.WORK_TR.LanguageID==lang)).select(
            db.WORK.ALL, db.WORK_TR.ALL, groupby=db.WORK._id)
        work_id = work[0]['WORK_TR']['id']
    except KeyError:
        redirect(URL('Pindar/default', 'works', 'all?e='+request.args(0)))
    authors = db((db.WORK_AUTHOR.WorkID==work_id) & 
            (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
            (db.AUTHOR._id==db.AUTHOR_TR.AuthorID) & 
            (db.AUTHOR_TR.LanguageID==lang)).select(
            orderby=db.AUTHOR_TR.DisplayName, limitby=(0,10))
    quotes = db((db.WORK_TR._id==work_id) & 
            (db.WORK_TR.WorkID==db.WORK._id) & 
            (db.QUOTE_WORK.WorkID==db.WORK._id) & 
            (db.QUOTE_WORK.QuoteID==db.QUOTE._id)).select(
            orderby=~db.QUOTE.created_on, limitby=(0,10))
    return locals()


@auth.requires_login()
def add():
    langs = db((db.LANGUAGE._id > 0)).select(
        db.LANGUAGE.NativeName, db.LANGUAGE._id,
        orderby=db.LANGUAGE._id).as_list()
    if request.vars.author:
        init_author = request.vars.author
        init_author_name = db((db.AUTHOR.id==init_author) & 
            (db.AUTHOR_TR.AuthorID==db.AUTHOR.id)).select(
            db.AUTHOR_TR.DisplayName, limitby=(0,1))[0].DisplayName
    if request.vars.work:
        init_work = request.vars.work
        init_work_name = db((db.WORK.id==init_work) & 
            (db.WORK_TR.WorkID==db.WORK.id)).select(
            db.WORK_TR.WorkName, limitby=(0,1))[0].WorkName
        if not request.vars.author:
            search = db((db.WORK_AUTHOR.WorkID==init_work) & 
                (db.AUTHOR.id==db.WORK_AUTHOR.AuthorID) & 
                (db.AUTHOR_TR.AuthorID==db.AUTHOR.id)).select(
                db.AUTHOR_TR.DisplayName, db.AUTHOR.id, 
                limitby=(0,1))[0]
            init_author = search.AUTHOR.id
            init_author_name = search.AUTHOR_TR.DisplayName
    return locals()












