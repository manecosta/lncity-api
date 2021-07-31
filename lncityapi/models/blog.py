from lncityapi import db
from lncityapi.models import BaseModel, User


class Blog(BaseModel):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    title = db.Column('title', db.String(128), nullable=False)
    created_time = db.Column('created_time', db.Float, nullable=False)

    user = db.relationship('User', foreign_keys='Blog.user_id', lazy='select')

    _fields = {
        'user': {
            'type': 'model',
            'show': True
        },
        'title': {
            'type': 'base',
            'show': True
        },
        'created_time': {
            'type': 'base',
            'show': True
        }
    }


class Blogpost(BaseModel):
    __tablename__ = 'blogpost'

    id = db.Column('id', db.Integer, primary_key=True)
    blog_id = db.Column('blog_id', db.ForeignKey(Blog.id), nullable=False)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    title = db.Column('title', db.String(128), nullable=False)
    body = db.Column('body', db.Text, nullable=False)
    created_time = db.Column('created_time', db.Float, nullable=False)
    updated_time = db.Column('updated_time', db.Float, nullable=False)
    donation_count = db.Column('donation_count', db.Float, nullable=False, default=0)
    donation_amount = db.Column('donation_amount', db.Float, nullable=False, default=0)

    blog = db.relationship('Blog', foreign_keys='Blogpost.blog_id', lazy='select')
    user = db.relationship('User', foreign_keys='Blogpost.user_id', lazy='select')

    _fields = {
        'id': {
            'type': 'base',
            'show': True
        },
        'user': {
            'type': 'model',
            'show': True
        },
        'blog': {
            'type': 'model',
            'show': False
        },
        'tags': {
            'type': 'model',
            'show': True
        },
        'title': {
            'type': 'base',
            'show': True
        },
        'body': {
            'type': 'base',
            'show': True
        },
        'created_time': {
            'type': 'base',
            'show': True
        },
        'updated_time': {
            'type': 'base',
            'show': True
        },
        'donation_count': {
            'type': 'base',
            'show': True
        },
        'donation_amount': {
            'type': 'base',
            'show': True
        },
        'comments_count': {
            'type': 'base',
            'show': True
        }
    }


class Blogposttag(BaseModel):
    __tablename__ = 'blogposttag'

    id = db.Column('id', db.Integer, primary_key=True)
    blogpost_id = db.Column('blogpost_id', db.ForeignKey(Blogpost.id), nullable=False)
    tag_id = db.Column('tag_id', db.ForeignKey('tag.id'), nullable=False)

    blogpost = db.relationship('Blogpost', foreign_keys='Blogposttag.blogpost_id', lazy='select')
    tag = db.relationship('Tag', foreign_keys='Blogposttag.tag_id', lazy='select')

    _fields = {
        'id': {
            'type': 'base',
            'show': True
        },
        'blogpost': {
            'type': 'model',
            'show': True
        },
        'tag': {
            'type': 'model',
            'show': False
        }
    }


class Blogpostdonation(BaseModel):
    __tablename__ = 'blogpostdonation'

    id = db.Column('id', db.Integer, primary_key=True)
    blogpost_id = db.Column('blogpost_id', db.ForeignKey(Blogpost.id), nullable=False)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    amount = db.Column('amount', db.Float, nullable=False)
    time = db.Column('time', db.Float, nullable=False)

    blogpost = db.relationship('Blogpost', foreign_keys='Blogpostdonation.blogpost_id', lazy='select')
    user = db.relationship('User', foreign_keys='Blogpostdonation.user_id', lazy='select')

    _fields = {
        'user': {
            'type': 'model',
            'show': True
        },
        'blogpost': {
            'type': 'model',
            'show': False
        },
        'amount': {
            'type': 'base',
            'show': True
        },
        'time': {
            'type': 'base',
            'show': True
        }
    }
        

class Blogpostcomment(BaseModel):
    __tablename__ = 'blogpostcomment'

    id = db.Column('id', db.Integer, primary_key=True)
    blogpost_id = db.Column('blogpost_id', db.ForeignKey(Blogpost.id), nullable=False)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    body = db.Column('body', db.Text, nullable=False)
    created_time = db.Column('created_time', db.Float, nullable=False)
    donation_count = db.Column('donation_count', db.Float, nullable=False, default=0)
    donation_amount = db.Column('donation_amount', db.Float, nullable=False, default=0)

    blogpost = db.relationship('Blogpost', foreign_keys='Blogpostcomment.blogpost_id', lazy='select')
    user = db.relationship('User', foreign_keys='Blogpostcomment.user_id', lazy='select')

    _fields = {
        'id': {
            'type': 'base',
            'show': True
        },
        'user': {
            'type': 'model',
            'show': True
        },
        'blogpost': {
            'type': 'model',
            'show': False
        },
        'body': {
            'type': 'base',
            'show': True
        },
        'created_time': {
            'type': 'base',
            'show': True
        },
        'donation_count': {
            'type': 'base',
            'show': True
        },
        'donation_amount': {
            'type': 'base',
            'show': True
        }
    }


class Blogpostcommentdonation(BaseModel):
    __tablename__ = 'blogpostcommentdonation'

    id = db.Column('id', db.Integer, primary_key=True)
    blogpostcomment_id = db.Column('blogpostcomment_id', db.ForeignKey(Blogpostcomment.id), nullable=False)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    amount = db.Column('amount', db.Float, nullable=False)
    time = db.Column('time', db.Float, nullable=False)

    user = db.relationship('User', foreign_keys='Blogpostcommentdonation.user_id', lazy='select')
    blogpostcomment = db.relationship('Blogpostcomment', foreign_keys='Blogpostcommentdonation.blogpostcomment_id', lazy='select')

    _fields = {
        'user': {
            'type': 'model',
            'show': True
        },
        'blogpostcomment': {
            'type': 'model',
            'show': False
        },
        'amount': {
            'type': 'base',
            'show': True
        },
        'time': {
            'type': 'base',
            'show': True
        }
    }
