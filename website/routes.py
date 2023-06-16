from website import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm
from website.models import test_post, test_user


#Defines what url ending will take you to the following route
@app.route('/')
@app.route('/home')
#Defines what the home route should do, when using url_for() always put the
    #route name instead of the url ending (ex. url_for(home) will redirect to home)
def home():
    #Defining posts and users from test_post and test_user to import into home screen
    posts = test_post.query.all()
    users = test_user.query.all()
    #Uses the home.html template that draws from layout.html to make a full webpage
    return render_template('home.html',
                           posts = posts,
                           users = users)


@app.route('/about')
def about():
    return render_template('about.html',
                           title = 'About')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))
    
    #Imports form from forms to register new user with MySQL database
    form = RegistrationForm()
    #Success message
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = test_user(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you may now log in.', 'success')  
        return(redirect(url_for('login')))
    
    #Despite this being after the import and if logic, this is what renders the webpage
    return render_template('register.html',
                           title = 'Register',
                           form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))
    
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
                return(redirect(url_for('home')))
        
        flash('Login unsuccessful. Please check email and password.', 'danger')
    
    #Once again, this renders the page after the logic is defined
    return render_template('login.html',
                           title = 'Log-in',
                           form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'info')
    return(redirect(url_for('home')))


@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename = f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title = 'Account', image_file = image_file)

