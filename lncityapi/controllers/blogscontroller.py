import arrow

from peewee import fn, JOIN, prefetch

from lncityapi.models import Blog, Blogpost, Blogpostcomment, User, Blogposttag, Tag


def blog_exists(blog_id):
    for _ in Blog.select().where(Blog.id == blog_id):
        return True
    return False


def blog_post_exists(blog_id, blogpost_id):
    for _ in Blogpost.select().where(Blogpost.blog == blog_id, Blogpost.id == blogpost_id):
        return True
    return False


def get_blog_post_count(blog_id, tag=None):
    if tag is None:
        return Blogpost.select().where(Blogpost.blog == blog_id).count()
    else:
        return Blogposttag.select(Blogposttag, Tag).join(Tag).where(Tag.name == tag, Tag.blog == blog_id).count()


def get_blog_post(blogpost_id):
    blogpost_query = (
        Blogpost.select(Blogpost, User, fn.COUNT(Blogpostcomment.id).alias('comments_count'))
            .join(User)
            .switch(Blogpost)
            .join(Blogpostcomment, JOIN.LEFT_OUTER)
            .where(Blogpost.id == blogpost_id)
            .group_by(Blogpost.id)
    )

    for bp in blogpost_query:
        return bp

    return None


def get_blog_posts(blog_id, page, count, tag=None):

    if tag is None:
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
    else:
        blogpost_ids = [bpt.blogpost_id for bpt in Blogposttag.select(Blogposttag, Tag).join(Tag).where(Tag.name == tag, Tag.blog == blog_id)]

        blogposts_query = (
            Blogpost.select(Blogpost, User, fn.COUNT(Blogpostcomment.id).alias('comments_count'))
                .join(User)
                .switch(Blogpost)
                .join(Blogpostcomment, JOIN.LEFT_OUTER)
                .where(Blogpost.blog == blog_id, Blogpost.id.in_(blogpost_ids))
                .order_by(Blogpost.created_time.desc())
                .group_by(Blogpost.id)
                .paginate(page, count)
        )

    blogposts = []
    blogposts_by_id = {}
    for bp in blogposts_query:
        setattr(bp, 'tags', [])
        blogposts.append(bp)
        blogposts_by_id[str(bp.id)] = bp

    blogposttags_query = (
        Blogposttag.select(Blogposttag, Tag)
            .join(Tag)
            .where(Blogposttag.blogpost << [int(k) for k in blogposts_by_id.keys()])
    )

    for bpt in blogposttags_query:
        bp = blogposts_by_id.get(str(bpt.blogpost_id))
        bp.tags.append(bpt.tag)

    return blogposts


def get_blog_post_comment_count(blogpost_id):
    return Blogpostcomment.select().where(Blogpostcomment.blogpost == blogpost_id).count()


def get_blog_post_comment(blogpostcomment_id):

    blogpostcomments_query = (
        Blogpostcomment.select(Blogpostcomment, User)
            .join(User)
            .switch(Blogpostcomment)
            .where(Blogpostcomment.id == blogpostcomment_id)
    )

    for bpc in blogpostcomments_query:
        return bpc

    return None


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
