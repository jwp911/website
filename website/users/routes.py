from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from website import db, bcrypt
from website.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
    RequestResetForm, ResetPasswordForm)
from website.users.utils import save_picture, send_reset_email
from website.models import test_post, test_user


users = Blueprint('users', __name__)

@users.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main_bp.home'))
    
    #Imports form from forms to register new user with MySQL database
    form = RegistrationForm()
    #Success message
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = test_user(username = form.username.data,
                         email = form.email.data,
                         password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you may now log in.', 'success')  
        return(redirect(url_for('user_bp.login')))
    
    #Despite this being after the import and if logic, this is what renders the webpage
    return render_template('users/register.html',
                           title = 'Register',
                           form = form)

@users.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main_bp.home'))
    
    #Imports form from forms to log into an account with MySQL database
    form = LoginForm()
    if form.validate_on_submit():
        #Check if there is a user with given email, and then check that password matches
        user = test_user.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #Logs user in and redirects them to home with a success message
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful.', 'success')
            if next_page:
                return(redirect(next_page))
            else:
                return(redirect(url_for('main_bp.home')))
        
        flash('Login unsuccessful. Please check email and password.', 'danger')
    
    #Once again, this renders the page after the logic is defined
    return render_template('users/login.html',
                           title = 'Log-in',
                           form = form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'info')
    return(redirect(url_for('main_bp.home')))

@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information has been updated', 'success')
        return redirect(url_for('user_bp.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = f'profile_pics/{current_user.image_file}')
    return render_template('users/account.html',
                           title = 'Account',
                           image_file = image_file,
                           form = form)

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = test_user.query.filter_by(username = username).first_or_404()
    posts = test_post.query.filter_by(author = user)\
        .order_by(test_post.date_posted.desc())\
        .paginate(page = page, per_page = 6)
    return render_template('user_posts.html',
                           user = user,
                           posts = posts)

@users.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main_bp.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = test_user.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('user_bp.login'))
    return render_template('users/reset_request.html',
                           title = 'Reset Password',
                           form = form)

@users.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main_bp.home'))
    user = test_user.verify_reset_token(token)
    if user == False:
        flash('That token is invalid or expired. Please try again.', 'warn')
        return redirect(url_for('main_bp.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated, you may now log in.', 'success')  
        return(redirect(url_for('main_bp.login')))
    return render_template('users/reset_token.html',
                           title = 'Reset Password',
                           form = form)

