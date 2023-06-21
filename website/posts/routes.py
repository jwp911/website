from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from website import db
from website.posts.forms import PostForm
from website.models import test_post

posts = Blueprint('users', __name__)

@posts.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = test_post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main_bp.home'))
    return render_template('posts/create_post.html',
                           title = 'New Post',
                           form = form,
                           legend = 'New Post')

@posts.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def post(post_id):
    post = test_post.query.get_or_404(post_id)
    return render_template('posts/post.html',
                           title = post.title,
                           post = post)

@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = test_post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Your post has been updated', 'success')
            return(redirect(url_for('post_bp.post', post_id = post.id)))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('posts/create_post.html',
                                title = 'Update Post',
                                form = form,
                                legend = 'Update Post')

@posts.route('/post/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    post = test_post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main_bp.home'))

