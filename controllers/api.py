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
import re
from gluon.tools import prettydate


def check_response(request_vars, check={}, user=False):
    # validation
    # is_integer: ensures it's a nonnegative integer
    # length_xxx: max length of xxx
    # length_xxx_yyy: min length of xxx, max length of yyy
    # not_%: query is not just the % symbol (for SQL LIKE queries)
    # required: parameter must be given

    response = {'msg': '',
                'status': 200,
                'request': request_vars}
    if user:
        if not auth.user:
            response['msg'] += 'no user logged in; '
            response['status'] = 401
    for object in check.keys():
        try:
            if type(check[object]).__name__ == 'str':
                check[object] = [check[object]]
            for req in check[object]:
                if req == 'required' and not request_vars[object]:
                    response['msg'] += 'query parameter ' + object + ' missing; '
                    break;
                elif request_vars[object]:
                    if req == 'is_integer' \
                        and not re.search('^[0-9]*$', request_vars[object]):
                        response['msg'] += object + \
                            ' must be a positive integer; '
                    elif req[0:6] == 'length':
                        if not (req.find('_', 8) == -1):
                            minimum = int(req[7:req.find('_', 8)])
                            maximum = int(req[req.find('_', 8)+1:])
                            if len(request_vars[object]) < minimum:
                                response['msg'] += object + \
                                    ' has a min length of ' + str(minimum) + '; '
                            elif len(request_vars[object]) > maximum:
                                response['msg'] += object + \
                                    ' has a max length of ' + str(maximum) + '; '
                        else:
                            # if only one argument, it's the minimum
                            minimum = int(req[7:])
                            if len(request_vars[object]) < minimum:
                                response['msg'] += object + \
                                    ' has a min length of ' + str(minimum) + '; '
                    elif req == 'not_%':
                        valid = False
                        for i in request_vars[object]:
                            if i is not '%':
                                valid = True
                                break
                        if not valid:
                            response['msg'] += object + \
                                ' must be an actual query; '
        except:
            response['msg'] += 'query parameter ' + object + ' is incorrect; '
    if not response['msg']: 
        response['msg'] = 'yey'
    else:
        if response['status'] is not 401:
            response['status'] = 400
    return response


def quote_query():
    response = check_response(request.vars,
        {'lookup': 'length_2_128', 'quote': 'is_integer'})
    if response['status'] == 200:
        #try:
            # should disqualify query if it's just the '%' character
            # initial query: lookup
            # filter by: author, work, min/max rating, language, dates
            # finally: sort by rating, date, date submitted, magic
            # and then limit/offset

            # base query
            r = db.RATING.Rating.avg()
            s = db.RATING.Rating.count()
            query = (db.QUOTE._id==db.QUOTE_WORK.QuoteID) & \
                (db.QUOTE_WORK.WorkID==db.WORK._id) & \
                (db.WORK._id==db.WORK_TR.WorkID) & \
                (db.WORK_AUTHOR.WorkID==db.WORK._id) & \
                (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & \
                (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)
            if request.vars.lookup:
                lookup = request.vars.lookup
                lookup = lookup.split(' ')
                for word in lookup:
                    query &= db.QUOTE.Text.like('%' + word + '%')
            init_query = db(query).select(
                db.QUOTE.Text, db.QUOTE.QuoteLanguageID, db.QUOTE._id, 
                db.QUOTE.IsOriginalLanguage, db.QUOTE.created_on, 
                db.AUTHOR_TR.DisplayName, db.AUTHOR_TR._id, 
                db.AUTHOR.YearBorn, db.AUTHOR.YearDied,
                db.WORK_TR.WorkName, db.WORK_TR._id,
                db.WORK.YearPublished, db.WORK.YearWritten,
                r, s, 
                left=db.RATING.on(db.RATING.QuoteID==db.QUOTE._id),
                groupby=db.QUOTE._id)
            for h in init_query:
                    h.QUOTE.created_on = str(h.QUOTE.created_on)

            # filters
            if request.vars.quote:
                init_query = init_query.find(lambda row: 
                    row.QUOTE.id==int(request.vars.quote))
            if request.vars.author:
                author_list = (request.vars.author).split(',')
                if isinstance(author_list, str):
                    author_list = [author_list]
                author_list = map(int, author_list)
                init_query = init_query.find(lambda row: 
                    row.AUTHOR_TR.id in author_list)
            if request.vars.work:
                work_list = (request.vars.work).split(',')
                if isinstance(work_list, str):
                    work_list = [work_list]
                work_list = map(int, work_list)
                init_query = init_query.find(lambda row: 
                    row.WORK_TR.id in work_list)
            if request.vars.language:
                language_list = (request.vars.language).split(',')
                if isinstance(language_list, str):
                    language_list = [language_list]
                language_list = map(int, language_list)
                init_query = init_query.find(lambda row: 
                    row.QUOTE.QuoteLanguageID in language_list)
            if request.vars.minRating:
                init_query = init_query.find(lambda row: 
                    row._extra['AVG(RATING.Rating)'] >= \
                    float(request.vars.minRating))
            if request.vars.maxRating:
                init_query = init_query.find(lambda row: 
                    row._extra['AVG(RATING.Rating)'] <= \
                    float(request.vars.maxRating))
            if request.vars.minDate or request.vars.maxDate:
                if request.vars.minDate:
                    if request.vars.maxDate:
                        init_query = init_query.find(lambda row:
                            __check_dates(row, min=request.vars.minDate, 
                                max=request.vars.maxDate))
                    else:
                        init_query = init_query.find(lambda row:
                            __check_dates(row, min=request.vars.minDate))
                else:
                    init_query = init_query.find(lambda row:
                            __check_dates(row, max=request.vars.maxDate))

            # sorting: note ~ means ascending
            if request.vars.sort:
                sort = request.vars.sort
            else:
                sort = 'rating'
            if sort == 'rating':
                init_query = init_query.sort(lambda row: 
                    row._extra['AVG(RATING.Rating)'], reverse=True)
            elif sort == '~rating':
                init_query = init_query.sort(lambda row: 
                    row._extra['AVG(RATING.Rating)'])
            elif sort == 'dateSubmitted':
                init_query = init_query.sort(lambda row: 
                    row.QUOTE.created_on, reverse=True)
            elif sort == '~dateSubmitted':
                init_query = init_query.sort(lambda row: 
                    row.QUOTE.created_on)
            else:
                response.update({'msg': 'invalid sort parameter'})

            # offset
            if request.vars.offset:
                offset = int(request.vars.offset)
            else:
                offset = 0
            init_query = init_query.find(lambda row: True, 
                limitby=(offset, 10 + offset))

            display_quotes = init_query.as_list()

            response.update({'quotes': sanitize_JSON(display_quotes)})
        #except:
         #   response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


def __check_dates(row, min=-10000, max=10000):
    min = int(min)
    max = int(max)
    # min date: if earlier than work or author born, know it's false
    if row.WORK.YearPublished is not None or row.WORK.YearWritten is not None:
        # can use work dates
        if row.WORK.YearPublished is not None:
            if row.WORK.YearPublished < min:
                return False
        if row.WORK.YearWritten is not None:
            if row.WORK.YearWritten < min:
                return False
    else:
        if row.AUTHOR.YearDied is not None:
            if row.AUTHOR.YearDied < min:
                return False
    if row.WORK.YearPublished is not None or row.WORK.YearWritten is not None:
        # can use work dates
        if row.WORK.YearPublished is not None:
            if row.WORK.YearPublished > max:
                return False
        if row.WORK.YearWritten is not None:
            if row.WORK.YearWritten > max:
                return False
    else:
        if row.AUTHOR.YearBorn is not None:
            if row.AUTHOR.YearBorn > max:
                return False
    return True


def author_query():
    response = check_response(request.vars, 
        {'lookup': 'length_2_128'})
    if response['status'] == 200:
        try:
            # should disqualify query if it's just the '%' character
            lang = 1
            workcount = db.WORK_AUTHOR.WorkID.count()
            query = (db.AUTHOR_TR.LanguageID==lang) & \
                (db.AUTHOR_TR.AuthorID==db.AUTHOR.id)
            if request.vars.lookup:
                lookup = request.vars.lookup
                lookup = lookup.split(' ')
                for word in lookup:
                    word = '%' + word + '%'
                    query &= ((db.AUTHOR_TR.DisplayName.like(word)) | \
                        (db.AUTHOR_TR.FirstName.like(word)) | \
                        (db.AUTHOR_TR.MiddleName.like(word)) | \
                        (db.AUTHOR_TR.LastName.like(word)) | \
                        (db.AUTHOR_TR.AKA.like(word)))
            init_query = db(query).select(
                db.AUTHOR_TR.DisplayName, db.AUTHOR_TR.id,
                db.AUTHOR.YearBorn, db.AUTHOR.YearDied, db.AUTHOR.id, 
                workcount, 
                left=db.WORK_AUTHOR.on(db.AUTHOR.id==db.WORK_AUTHOR.AuthorID),
                groupby=db.AUTHOR.id,
                orderby=~workcount)

            if request.vars.offset:
                offset = int(request.vars.offset)
            else:
                offset = 0
            init_query = init_query.find(lambda row: True, 
                limitby=(offset, 6 + offset))
            display_authors = init_query.as_list()

            response.update({'authors': sanitize_JSON(display_authors)})
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
        {'DisplayName': 'length_2_512'},
        user=True)
    if response['status'] == 200:
        try:
            request.vars.AuthorID = int(db.AUTHOR.insert(
                **db.AUTHOR._filter_fields(request.vars)))
            AuthorTrID = db.AUTHOR_TR.insert(
                **db.AUTHOR_TR._filter_fields(request.vars))
            response.update({'AuthorID': request.vars.AuthorID,
                             'AuthorTrID': AuthorTrID})
            attributedWorkID = db.WORK.insert()
            attributedWorkTrID = db.WORK_TR.insert(WorkName='Attributed',
                LanguageID=1, WorkID=attributedWorkID,
                WorkSubtitle='', WorkDescription='', WikipediaLink='',
                WorkNote='')
            db.WORK_AUTHOR.insert(WorkID=attributedWorkID,
                AuthorID=request.vars.AuthorID)

        except:
            response.update({'msg': 'no author by that id', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


    
def work_query():
    response = check_response(request.vars, 
        {'lookup': 'length_2_128'}) # add 'not_%'
    if response['status'] == 200:
        try:
            # should disqualify query if it's just the '%' character
            lang = 1
            quotecount = db.QUOTE_WORK.QuoteID.count()
            query = (db.WORK_AUTHOR.AuthorID==db.AUTHOR._id) & \
                    (db.WORK_AUTHOR.WorkID==db.WORK._id) & \
                    (db.WORK._id==db.WORK_TR.WorkID) & \
                    (db.WORK_TR.LanguageID==lang) & \
                    (db.AUTHOR._id==db.AUTHOR_TR.AuthorID)
            if request.vars.lookup:
                lookup = request.vars.lookup
                lookup = lookup.split(' ')
                for word in lookup:
                    word = '%' + word + '%'
                    query &= ((db.WORK_TR.WorkName.like(word)) | \
                        (db.WORK_TR.WorkSubtitle.like(word)))
            if request.vars.author:
                query &= db.AUTHOR._id==request.vars.author
            init_query = db(query).select(
                    db.WORK_TR.WorkName, db.WORK_TR.id, 
                    db.WORK_TR.WorkSubtitle, db.WORK.YearPublished,
                    db.WORK.id, db.AUTHOR_TR.DisplayName, quotecount, 
                    left=db.QUOTE_WORK.on(db.WORK.id==db.QUOTE_WORK.WorkID),
                    groupby=db.WORK.id,
                    orderby=~quotecount)

            if request.vars.offset:
                offset = int(request.vars.offset)
            else:
                offset = 0
            init_query = init_query.find(lambda row: True, 
                limitby=(offset, 6 + offset))
            display_works = init_query.as_list()

            response.update({'works': sanitize_JSON(display_works)})
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
        {'WorkName': 'length_2_1024', 'AuthorID': 'is_integer'},
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
        {'QuoteLanguageID': 'is_integer', 'Text': 'length_3',
        'WorkID': 'is_integer'},
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


def language_query():
    response = check_response(request.vars, 
        {})
    counts = db.QUOTE.QuoteLanguageID.count()
    languages = db(db.LANGUAGE._id > 0).select(
        db.LANGUAGE.id, db.LANGUAGE.EnglishName, db.LANGUAGE.NativeName,
        counts,
        left=db.QUOTE.on(db.LANGUAGE.id==db.QUOTE.QuoteLanguageID),
        groupby=db.LANGUAGE.id, orderby=~counts).as_list()
    response.update({'languages': sanitize_JSON(languages)})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


# flag quote
def flag():
    response = check_response(request.vars, 
        {'Type': 'is_integer'})
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
        {'Rating': 'is_integer', 'QuoteID': 'is_integer'}, 
        user=True)
    if response['status'] == 200:
        previous = db((db.RATING.QuoteID==request.vars.QuoteID) & 
            (db.RATING.created_by==auth.user)).select(db.RATING.Rating.avg()).\
            first()['AVG(RATING.Rating)']
        if previous is None:
            ratingID = db.RATING.insert(
                **db.RATING._filter_fields(request.vars))
        else: # user has already rated this quote
            previous = str(previous)
            ratingID = db((db.RATING.QuoteID==request.vars.QuoteID) & 
                (db.RATING.created_by==auth.user)).update(
                **db.RATING._filter_fields(request.vars))
        if ratingID:
            response.update({'id': ratingID, 'update': previous})
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
        {'QuoteID': 'is_integer'})
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
        response['comments'] = sanitize_JSON(commentslist)
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
        {'Text': 'length_1_512', 'QuoteID': 'is_integer'},
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


@auth.requires_login()
def edit_quote():
    response = check_response(request.vars, 
        {'QuoteLanguageID': 'is_integer', 'Text': 'length_3',
        'QuoteID': 'is_integer'},
        user=True)
    if response['status'] == 200:
        try:
            quote = db(db.QUOTE._id==request.vars.QuoteID).\
                    update(**db.QUOTE._filter_fields(request.vars))
            quote = db(db.QUOTE._id==request.vars.QuoteID).select(
                db.QUOTE.id, db.QUOTE.Text, db.QUOTE.QuoteLanguageID, 
                db.QUOTE.IsOriginalLanguage, db.QUOTE.Note).as_list()
            response.update({'msg': 'Quote successfully updated',
                'Quote': quote})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


@auth.requires_login()
def edit_author():
    request.vars.LanguageID = 1
    response = check_response(request.vars, 
        {'DisplayName': 'length_2_512'},
        user=True)
    if response['status'] == 200:
        try:
            author = db(db.AUTHOR._id==request.vars.AuthorId).\
                    update(**db.AUTHOR._filter_fields(request.vars))
            author = db(db.AUTHOR._id==request.vars.AuthorId).\
                select(db.AUTHOR.id).as_list()
            author_tr = db(db.AUTHOR_TR._id==request.vars.AuthorTrId).\
                    update(**db.AUTHOR_TR._filter_fields(request.vars))
            author_tr = db(db.AUTHOR_TR._id==request.vars.AuthorTrId).\
                    select(db.AUTHOR_TR.id, db.AUTHOR_TR.DisplayName).as_list()
            response.update({'msg': 'Author successfully updated',
                'Author': author, 'AuthorTr': author_tr})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


@auth.requires_login()
def edit_work():
    request.vars.LanguageID = 1
    response = check_response(request.vars, 
        {'WorkName': 'length_2_1024'},
        user=True)
    if response['status'] == 200:
        try:
            work = db(db.WORK._id==request.vars.WorkId).\
                    update(**db.WORK._filter_fields(request.vars))
            work = db(db.WORK._id==request.vars.WorkId).\
                select(db.WORK.id).as_list()
            work_tr = db(db.WORK_TR._id==request.vars.WorkTrId).\
                    update(**db.WORK_TR._filter_fields(request.vars))
            work_tr = db(db.WORK_TR._id==request.vars.WorkTrId).\
                    select(db.WORK_TR.id, db.WORK_TR.WorkName).as_list()
            response.update({'msg': 'Work successfully updated',
                'Work': work, 'WorkTr': work_tr})
        except TypeError as e:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


@auth.requires_login()
def get_edit_history():
    response = check_response(request.vars, user=True)
    if response['status'] == 200:
        try:
            if request.vars.QuoteID:
                past = db((db.QUOTE_archive.current_record==\
                    request.vars.QuoteID) & 
                    (db.QUOTE_archive.modified_by==db.auth_user.id)).select(
                    db.QUOTE_archive.Text, db.QUOTE_archive.QuoteLanguageID,
                    db.QUOTE_archive.Note, db.QUOTE_archive.IsOriginalLanguage, 
                    db.QUOTE_archive.modified_on, db.auth_user.username,
                    orderby=~db.QUOTE_archive.modified_on)
                current = db((db.QUOTE._id==request.vars.QuoteID) & 
                    (db.QUOTE.modified_by==db.auth_user.id)).select(
                    db.QUOTE.Text, db.QUOTE.QuoteLanguageID,
                    db.QUOTE.Note, db.QUOTE.IsOriginalLanguage, 
                    db.QUOTE.modified_on, db.auth_user.username)
                for h in past:
                    h.QUOTE_archive.modified_on = \
                        str(h.QUOTE_archive.modified_on)
                for h in current:
                    h.QUOTE.modified_on = \
                        str(h.QUOTE.modified_on)
            elif request.vars.AuthorID:
                past = db((db.AUTHOR_TR_archive.current_record==\
                    request.vars.AuthorID) & 
                    (db.AUTHOR_TR_archive.modified_by==db.auth_user.id)).select(
                    db.AUTHOR_TR_archive.DisplayName, 
                    db.AUTHOR_TR_archive.FirstName, 
                    db.AUTHOR_TR_archive.MiddleName,
                    db.AUTHOR_TR_archive.LastName,
                    db.AUTHOR_TR_archive.modified_on,
                    db.auth_user.username,
                    orderby=~db.AUTHOR_TR_archive.modified_on)
                current = db((db.AUTHOR_TR._id==\
                    request.vars.AuthorID) & 
                    (db.AUTHOR_TR.modified_by==db.auth_user.id)).select(
                    db.AUTHOR_TR.DisplayName, 
                    db.AUTHOR_TR.FirstName, 
                    db.AUTHOR_TR.MiddleName,
                    db.AUTHOR_TR.LastName,
                    db.AUTHOR_TR.modified_on,
                    db.auth_user.username,
                    orderby=~db.AUTHOR_TR.modified_on)
                for h in past:
                    h.AUTHOR_TR_archive.modified_on = \
                        str(h.AUTHOR_TR_archive.modified_on)
                for h in current:
                    h.AUTHOR_TR.modified_on = \
                        str(h.AUTHOR_TR.modified_on)
            elif request.vars.WorkID:
                past = db((db.WORK_TR_archive.current_record==\
                    request.vars.WorkID) & 
                    (db.WORK_TR_archive.modified_by==db.auth_user.id)).select(
                    db.WORK_TR_archive.WorkName,
                    db.WORK_TR_archive.WorkSubtitle,
                    db.WORK_TR_archive.modified_on, db.auth_user.username,
                    orderby=~db.WORK_TR_archive.modified_on)
                current = db((db.WORK_TR._id==\
                    request.vars.WorkID) & 
                    (db.WORK_TR.modified_by==db.auth_user.id)).select(
                    db.WORK_TR.WorkName,
                    db.WORK_TR.WorkSubtitle,
                    db.WORK_TR.modified_on, db.auth_user.username,
                    orderby=~db.WORK_TR.modified_on)
                for h in past:
                    h.WORK_TR_archive.modified_on = \
                        str(h.WORK_TR_archive.modified_on)
                for h in current:
                    h.WORK_TR.modified_on = \
                        str(h.WORK_TR.modified_on)
            else:
                raise Exception('No ID supplied')
            response.update({'msg': 'yey',
                'past': sanitize_JSON(past.as_list()), 
                'current': sanitize_JSON(current.as_list())})
        except:
            response.update({'msg': 'oops', 'status': 503})
    status = response['status']
    response.pop('status', None)
    if not status == 200:
        raise HTTP(status, json.dumps(response))
    return json.dumps(response)


def sanitize_JSON(q):
    try:
        if isinstance(q, dict):
            for i in q.keys():
                q[i] = sanitize_JSON(q[i])
        elif isinstance(q, list):
            for i in range(0, len(q)):
                q[i] = sanitize_JSON(q[i])
        elif isinstance(q, str):  # actual value
            q = str(sanitize(q))
    except:
        pass
    return q



