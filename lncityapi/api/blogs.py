
import json

from flask import abort, request
from flask_login import login_required, current_user

from lncityapi import app
from lncityapi.other.util import route_prefix_v1

from lncityapi.controllers.blogscontroller import blog_exists, get_blog_post_count, get_blog_posts, blog_post_exists, \
    get_blog_post_comment_count, get_blog_post_comments, add_blog_post_comment, get_blog_post


@app.route(route_prefix_v1 + '/blogs/<int:blog_id>/posts/<int:page>/<int:count>', methods=['GET'])
@app.route(route_prefix_v1 + '/blogs/<int:blog_id>/posts/<int:page>/<int:count>/tags/<string:tag>', methods=['GET'])
def get_blog_posts_request(blog_id, page, count, tag=None):

    if not blog_exists(blog_id):
        abort(404, 'Blog not found')

    return json.dumps({
        'page': page,
        'count': count,
        'total': get_blog_post_count(blog_id, tag=tag),
        'posts': [bp.serializable() for bp in get_blog_posts(blog_id, page, count, tag=tag)]
    })


@app.route(route_prefix_v1 + '/blogs/<int:blog_id>/posts/<int:post_id>', methods=['GET'])
def get_blog_post_request(blog_id, post_id):

    if not blog_exists(blog_id):
        abort(404, 'Blog not found')

    blogpost = get_blog_post(post_id)

    if blogpost is None:
        abort(404, 'Blog post not found')

    return json.dumps(blogpost.serializable())


@app.route(route_prefix_v1 + '/blogs/<int:blog_id>/posts/<int:blogpost_id>/comments/<int:page>/<int:count>', methods=['GET'])
def get_blog_post_comments_request(blog_id, blogpost_id, page, count):

    if not blog_exists(blog_id):
        abort(404, 'Blog not found')

    if not blog_post_exists(blog_id, blogpost_id):
        abort(404, 'Blogpost not found')

    return json.dumps({
        'page': page,
        'count': count,
        'total': get_blog_post_comment_count(blogpost_id),
        'comments': [bpc.serializable() for bpc in get_blog_post_comments(blogpost_id, page, count)]
    })


@app.route(route_prefix_v1 + '/blogs/<int:blog_id>/posts/<int:blogpost_id>/comments', methods=['POST'])
@login_required
def add_blog_post_comment_request(blog_id, blogpost_id):

    if not blog_exists(blog_id):
        abort(404, 'Blog not found')

    if not blog_post_exists(blog_id, blogpost_id):
        abort(404, 'Blogpost not found')

    payload = request.get_json()
    body = payload.get('body')

    if not body:
        abort(400, 'Please provide a non empty body.')

    if len(body) > 500:
        abort(400, 'Comment too big. Keep it up to 500 characters.')

    comment = add_blog_post_comment(blogpost_id, current_user.id, body)

    return json.dumps(comment.serializable())
