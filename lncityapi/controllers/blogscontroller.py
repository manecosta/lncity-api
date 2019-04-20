import arrow

from peewee import fn, JOIN

from lncityapi.models.blog import Blog, Blogpost, Blogpostcomment
from lncityapi.models.user import User


def blog_exists(blog_id):
    for _ in Blog.select().where(Blog.id == blog_id):
        return True
    return False


def blog_post_exists(blog_id, blogpost_id):
    for _ in Blogpost.select().where(Blogpost.blog == blog_id, Blogpost.id == blogpost_id):
        return True
    return False


def get_blog_post_count(blog_id):
    return Blogpost.select().where(Blogpost.blog == blog_id).count()


def get_blog_posts(blog_id, page, count):

    blogposts_query = (
        Blogpost.select(Blogpost, User, fn.COUNT(Blogpostcomment.id).alias('comments_count'))
            .join(User)
            .switch(Blogpost)
            .join(Blogpostcomment, JOIN.LEFT_OUTER)
            .where(Blogpost.blog == blog_id)
            .order_by(Blogpost.created_time.desc())
            .group_by(Blogpost.id)
            .paginate(page, count)
    )

    blogposts = []
    for bp in blogposts_query:
        blogposts.append(bp)

    return blogposts


def get_blog_post_comment_count(blogpost_id):
    return Blogpostcomment.select().where(Blogpostcomment.blogpost == blogpost_id).count()


def get_blog_post_comments(blogpost_id, page, count):

    blogpostcomments_query = (
        Blogpostcomment.select(Blogpostcomment, User)
            .join(User)
            .switch(Blogpostcomment)
            .where(Blogpostcomment.blogpost == blogpost_id)
            .order_by(Blogpostcomment.created_time.desc())
            .paginate(page, count)
    )

    blogpostcomments = []
    for bpc in blogpostcomments_query:
        blogpostcomments.append(bpc)

    return blogpostcomments


def add_blog_post_comment(blogpost_id, user_id, body):

    comment = Blogpostcomment.create(
        blogpost=blogpost_id,
        user=user_id,
        body=body,
        created_time=arrow.get().timestamp
    )

    return comment
