from flask import Blueprint, render_template, request
from website.models import test_post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = test_post.query.order_by(test_post.date_posted.desc()).\
        paginate(page = page, per_page = 6)
    return render_template('main/home.html',
                           posts = posts)

@main.route('/about')
def about():
    return render_template('main/about.html',
                           title = 'About')

