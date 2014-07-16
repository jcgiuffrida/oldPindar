# coding: utf8
#basic outline for DAL text quote interface
db.define_table('QUOTE',
    Field('ORIGIN'),
    Field('TEXT'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id)
    )

#basic outline for DAL author interface
db.define_table('AUTHOR',
    Field('FNAME'),
    Field('LNAME'),
    Field('AKA'),
    Field('B_YEAR'),
    Field('D_YEAR'),
    Field('M_YEAR')
    )

#basic outline for DAL work interface
db.define_table('WORK',
    Field('TITLE'),
    Field('YEAR'),
    Field('LANGUAGE')
    )

#basic outline for DAL chapter interface
db.define_table('CHAPTER',
    Field('TITLE'),
    Field('NATIVE_TITLE')
    )
