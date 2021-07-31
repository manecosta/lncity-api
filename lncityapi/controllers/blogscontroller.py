import arrow

from lncityapi.models import Blog, Blogpost, Blogpostcomment, User, Blogposttag, Tag

from lncityapi import db

def blog_exists(blog_id):
    for _ in Blog.query.filter_by(id=blog_id):
        return True
    return False


def blog_post_exists(blog_id, blogpost_id):
    for _ in Blogpost.query.filter_by(blog_id=blog_id, id=blogpost_id):
        return True
    return False


def get_blog_post_count(blog_id, tag=None):
    if tag is None:
        return Blogpost.query.filter_by(blog_id=blog_id).count()
    else:
        return Blogposttag.query.join(Tag, Blogposttag.tag_id == Tag.id)\
                .filter(Tag.name == tag, Tag.blog == blog_id).count()


def get_blog_post(blogpost_id):
    # TODO: LATER

    # blogpost_query = (
    #     Blogpost.select(Blogpost, User, fn.COUNT(Blogpostcomment.id).alias('comments_count'))
    #         .join(User)
    #         .switch(Blogpost)
    #         .join(Blogpostcomment, JOIN.LEFT_OUTER)
    #         .where(Blogpost.id == blogpost_id)
    #         .group_by(Blogpost.id)
    # )

    # for bp in blogpost_query:
    #     setattr(bp, 'tags', [])
    #     for bpt in Blogposttag.query.join(Tag, Blogposttag.tag_id == Tag.id).filter(Blogposttag.blogpost == bp.id):
    #         bp.tags.append(bpt.tag)
    #     return bp

    return None


def get_blog_posts(blog_id, page, count, tag=None):
    # TODO: LATER
    return []

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
    return Blogpostcomment.query.filter_by(blogpost_id=blogpost_id).count()


def get_blog_post_comment(blogpostcomment_id):

    # TODO: LATER

    # blogpostcomments_query = (
    #     Blogpostcomment.select(Blogpostcomment, User)
    #         .join(User)
    #         .switch(Blogpostcomment)
    #         .where(Blogpostcomment.id == blogpostcomment_id)
    # )

    # for bpc in blogpostcomments_query:
    #     return bpc

    return None


def get_blog_post_comments(blogpost_id, page, count):
    # TODO: LATER
    return []

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

    comment = Blogpostcomment(
        blogpost_id=blogpost_id,
        user_id=user_id,
        body=body,
        created_time=arrow.get().timestamp()
    )

    db.session.add(comment)
    db.session.commit()
    db.session.refresh(comment)

    return comment
