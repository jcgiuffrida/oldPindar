# -*- coding: utf-8 -*-

# controller for API

# exposes endpoints:
# author_query(): GET authors based on a search query
# author_submit(): POST a new author
# work_query(): GET works based on a search query
# work_submit(): POST a new work
# quote_submit(): POST a new quote
# flag(): POST a new flag
# rate(): POST a new rating
# get_comments(): GET comments
# comment(): POST a new comment


import json


def check_response(request_vars, check={}, user=False):
    response = {'msg': '',
                'status': 200,
                'request': request_vars}
    if user:
        if not auth.user:
            response['msg'] += 'no user logged in'
            response['status'] = 501
    for object in check.keys():
        if not request_vars[object]:
            if response['msg']: response['msg'] += '; '
            response['msg'] += 'no ' + check[object] + ' specified'
            response['status'] = 501
    if not response['msg']: response['msg'] = 'yey'
    return response



def author_query():
    # should add a line here disqualifying query if it's just the '%' character
    query = '%' + request.vars.author_lookup + '%'
    if len(query) < 4:
        return ''
    lang = 1
    display_authors = db((db.AUTHOR_TR.LanguageID==lang) &
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
            response += '<tr class="author_query_result" id="' + \
                str(row.AUTHOR_TR.id) + '"><td>' + \
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
    request.vars.AuthorID = int(db.AUTHOR.insert(
        **db.AUTHOR._filter_fields(request.vars)))
    AuthorTrID = db.AUTHOR_TR.insert(
        **db.AUTHOR_TR._filter_fields(request.vars))
    response.flash='Added author: ' + request.vars.DisplayName
    return 'jQuery("#QUOTE_AuthorTrID").val("' + str(AuthorTrID) + '");'

    
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
            db.WORK.YearWritten, db.WORK_TR.WorkSubtitle, 
            orderby=db.WORK_TR.WorkName)
    response = '<table><thead>'
    response += '<tr><td><h4>Search results</h4></td></tr></thead>'
    if len(display_works)>0:
        response += '<tbody>'
        for row in display_works:
            response += '<tr class="work_query_result" id="' + \
                str(row.WORK_TR.id) + '"><td>' + \
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
    request.vars.WorkID = int(db.WORK.insert(
        **db.WORK._filter_fields(request.vars)))
    WorkTrID = db.WORK_TR.insert(**db.WORK_TR._filter_fields(request.vars))
    tmp = db((db.AUTHOR_TR.id==request.vars.AuthorTrID) & 
             (db.AUTHOR.id==db.AUTHOR_TR.AuthorID)).select(db.AUTHOR.id)
    for row in tmp:
        request.vars.AuthorID = row.id
    Work_Author_ID = db.WORK_AUTHOR.insert(
        **db.WORK_AUTHOR._filter_fields(request.vars))
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


# flag quote
def flag():
    response = check_response(request.vars, 
        {'Type': 'flag type', 'QuoteID': 'quote'})
    if not response['status'] == 501:
        flagID = db.FLAG.insert(**db.FLAG._filter_fields(request.vars))
        if flagID:
            response.update({'msg': 'yey', 'id': flagID})
        else:
            response.update({'msg': 'oops', 'status': 501})
    return json.dumps(response)


# rate quote
@auth.requires_login()
def rate():
    response = check_response(request.vars, 
        {'Rating': 'rating', 'QuoteID': 'quote'}, 
        user=True)
    if not response['status'] == 501:
        ratingID = db.RATING.insert(**db.RATING._filter_fields(request.vars))
        if ratingID:
            response['id'] = ratingID
        else:
            response.update({'msg': 'oops', 'status': 501})
    return json.dumps(response)


# get comments
def get_comments():
    response = check_response(request.vars,
        {'QuoteID': 'quote'})
    if not response['status'] == 501:
        quoteid = request.vars.QuoteID
        comments = db((db.COMMENT.QuoteID==quoteid) & 
            (db.auth_user._id==db.COMMENT.created_by)).select(
            orderby=~db.COMMENT.created_on, limitby=(0,10))
        commentslist = []
        for q in comments:
            commentslist.append({
                'text': q.COMMENT.Text, 
                'user': q.auth_user.username, 
                'timestamp': str(prettydate(q.COMMENT.created_on,T)) })
        response['comments'] = commentslist
    return json.dumps(response)


# add comment
@auth.requires_login()
def comment():
    response = check_response(request.vars,
        {'Text': 'text', 'QuoteID': 'quote'},
        user=True)
    if not response['status'] == 501:
        commentID = db.COMMENT.insert(**db.COMMENT._filter_fields(request.vars))
        if commentID:
            response['mycomment'] = {
            'text': request.vars.Text,
            'user': auth.user.username,
            'timestamp': 'Just now'}
        else:
            response.update({'msg': "oops", 'status': 501})
    return json.dumps(response)














