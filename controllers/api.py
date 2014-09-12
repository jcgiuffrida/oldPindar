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
import gluon.http


def check_response(request_vars, check={}, user=False):
    response = {'msg': '',
                'status': 200,
                'request': request_vars}
    if user:
        if not auth.user:
            response['msg'] += 'no user logged in'
            response['status'] = 401
    for object in check.keys():
        if not request_vars[object]:
            if response['msg']: response['msg'] += '; '
            response['msg'] += 'no ' + check[object] + ' specified'
            response['status'] = 400
    if not response['msg']: response['msg'] = 'yey'
    return response


def text_query():
    response = check_response(request.vars,
        {'lookup': 'query'})
    if response['status'] == 200:
        try:
            # should disqualify query if it's just the '%' character
            query = '%' + request.vars.lookup + '%'
            if len(query) < 4:
                response.update({'msg': 'query is too short',
                    'status': 400})
            else:
                lang = 1
                r = db.RATING.Rating.avg()
                s = db.RATING.Rating.count()
                quotes_display = db((db.QUOTE.Text.like(query)) & 
                    (db.QUOTE._id==db.QUOTE_WORK.QuoteID) & 
                    (db.QUOTE_WORK.WorkID==db.WORK._id) & 
                    (db.WORK._id==db.WORK_TR.WorkID) & 
                    (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
                    (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
                    (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)).select(
                    db.QUOTE.Text, db.AUTHOR_TR.DisplayName, db.WORK_TR.WorkName,
                    db.QUOTE._id, db.AUTHOR_TR._id, db.WORK_TR._id, r, s, 
                    left=db.RATING.on(db.RATING.QuoteID==db.QUOTE._id),
                    groupby=db.QUOTE._id, orderby=~r|~s, limitby=(0,10)).as_list()
                response.update({'quotes': quotes_display})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


def author_query():
    response = check_response(request.vars, 
        {'author_lookup': 'query'})
    if response['status'] == 200:
        try:
            # should disqualify query if it's just the '%' character
            query = '%' + request.vars.author_lookup + '%'
            if len(query) < 4:
                response.update({'msg': 'query is too short',
                    'status': 400})
            else:
                lang = 1
                workcount = db.WORK_AUTHOR.WorkID.count()
                display_authors = db((db.AUTHOR_TR.LanguageID==lang) &
                    (db.AUTHOR_TR.AuthorID==db.AUTHOR.id) & 
                    ((db.AUTHOR_TR.DisplayName.like(query)) | 
                     (db.AUTHOR_TR.FirstName.like(query)) | 
                     (db.AUTHOR_TR.MiddleName.like(query)) | 
                     (db.AUTHOR_TR.LastName.like(query)) | 
                     (db.AUTHOR_TR.AKA.like(query)))).select(
                    db.AUTHOR_TR.DisplayName, db.AUTHOR_TR.id,
                    db.AUTHOR.YearBorn, db.AUTHOR.YearDied, db.AUTHOR.id, 
                    workcount, 
                    left=db.WORK_AUTHOR.on(db.AUTHOR.id==db.WORK_AUTHOR.AuthorID),
                    groupby=db.AUTHOR.id,
                    orderby=~workcount, limitby=(0,5)).as_list()
                response.update({'authors': display_authors})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


@auth.requires_login()
def author_submit():
    request.vars.LanguageID = 1
    response = check_response(request.vars, 
        {'DisplayName': 'author display name'},
        user=True)
    if response['status'] == 200:
        try:
            request.vars.AuthorID = int(db.AUTHOR.insert(
                **db.AUTHOR._filter_fields(request.vars)))
            AuthorTrID = db.AUTHOR_TR.insert(
                **db.AUTHOR_TR._filter_fields(request.vars))
            response.update({'AuthorID': request.vars.AuthorID,
                             'AuthorTrID': AuthorTrID})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


    
def work_query():
    response = check_response(request.vars, 
        {'work_lookup': 'query'})
    if response['status'] == 200:
        try:
            # should disqualify query if it's just the '%' character
            query = '%' + request.vars.work_lookup + '%'
            if len(query) < 4:
                response.update({'msg': 'query is too short',
                    'status': 400})
            else:
                lang = 1
                quotecount = db.QUOTE_WORK.QuoteID.count()
                if request.vars.author:
                    display_works = db((db.AUTHOR._id==request.vars.author) &
                        (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
                        (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
                        (db.WORK._id==db.WORK_TR.WorkID) & 
                        (db.WORK_TR.LanguageID==lang) & 
                        (db.AUTHOR._id==db.AUTHOR_TR.AuthorID) & 
                        ((db.WORK_TR.WorkName.like(query)) |
                         (db.WORK_TR.WorkSubtitle.like(query)))).select(
                        db.WORK_TR.WorkName, db.WORK_TR.id, 
                        db.WORK_TR.WorkSubtitle, db.WORK.YearPublished,
                        db.WORK.id, db.AUTHOR_TR.DisplayName, quotecount, 
                        left=db.QUOTE_WORK.on(db.WORK.id==db.QUOTE_WORK.WorkID),
                        groupby=db.WORK.id,
                        orderby=~quotecount, limitby=(0,5)).as_list()
                else:
                    display_works = db((db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & 
                        (db.WORK_AUTHOR.WorkID==db.WORK._id) & 
                        (db.WORK._id==db.WORK_TR.WorkID) & 
                        (db.WORK_TR.LanguageID==lang) & 
                        (db.AUTHOR._id==db.AUTHOR_TR.AuthorID) & 
                        ((db.WORK_TR.WorkName.like(query)) |
                         (db.WORK_TR.WorkSubtitle.like(query)))).select(
                        db.WORK_TR.WorkName, db.WORK_TR.id, 
                        db.WORK_TR.WorkSubtitle, db.WORK.YearPublished,
                        db.WORK.id, db.AUTHOR_TR.DisplayName, quotecount, 
                        left=db.QUOTE_WORK.on(db.WORK.id==db.QUOTE_WORK.WorkID),
                        groupby=db.WORK.id,
                        orderby=~quotecount, limitby=(0,5)).as_list()
                response.update({'works': display_works})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


@auth.requires_login()
def work_submit():
    request.vars.LanguageID = 1
    response = check_response(request.vars, 
        {'WorkName': 'work name', 'AuthorID': 'author'},
        user=True)
    if response['status'] == 200:
        try:
            request.vars.WorkID = int(db.WORK.insert(
                **db.WORK._filter_fields(request.vars)))
            WorkTrID = db.WORK_TR.insert(
                **db.WORK_TR._filter_fields(request.vars))
            Work_Author_ID = db.WORK_AUTHOR.insert(
                **db.WORK_AUTHOR._filter_fields(request.vars))
            response.update({'WorkID': request.vars.WorkID,
                             'WorkTrID': WorkTrID,
                             'WorkAuthorID': Work_Author_ID})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


@auth.requires_login()
def quote_submit():
    response = check_response(request.vars, 
        {'QuoteLanguageID': 'language', 'Text': 'quote',
        'WorkID': 'work'},
        user=True)
    if response['status'] == 200:
        try:
            request.vars.QuoteID = \
                db.QUOTE.insert(**db.QUOTE._filter_fields(request.vars))
            Quote_Work_ID = db.QUOTE_WORK.insert(
                **db.QUOTE_WORK._filter_fields(request.vars))
            response.update({'QuoteID': request.vars.QuoteID,
                             'QuoteWorkID': Quote_Work_ID})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


# flag quote
def flag():
    response = check_response(request.vars, 
        {'Type': 'flag type', 'QuoteID': 'quote'})
    if response['status'] == 200:
        flagID = db.FLAG.insert(**db.FLAG._filter_fields(request.vars))
        if flagID:
            response.update({'msg': 'yey', 'id': flagID})
        else:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


# rate quote
@auth.requires_login()
def rate():
    response = check_response(request.vars, 
        {'Rating': 'rating', 'QuoteID': 'quote'}, 
        user=True)
    if response['status'] == 200:
        ratingID = db.RATING.insert(**db.RATING._filter_fields(request.vars))
        if ratingID:
            response['id'] = ratingID
        else:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


# get comments
def get_comments():
    response = check_response(request.vars,
        {'QuoteID': 'quote'})
    if response['status'] == 200:
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
    else:
        status = response['status']
        response.pop('status', None)
        raise HTTP(status, json.dumps(response))
    response.pop('status', None)
    return json.dumps(response)


# add comment
@auth.requires_login()
def comment():
    response = check_response(request.vars,
        {'Text': 'text', 'QuoteID': 'quote'},
        user=True)
    if response['status'] == 200:
        commentID = db.COMMENT.insert(**db.COMMENT._filter_fields(request.vars))
        if commentID:
            response['mycomment'] = {
            'text': request.vars.Text,
            'user': auth.user.username,
            'timestamp': 'Just now'}
        else:
            response.update({'msg': "oops", 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)














