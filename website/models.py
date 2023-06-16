from website import db, login_manager
from datetime import datetime
from flask_login import UserMixin

#Defines function to find and load user from user_id
@login_manager.user_loader
def load_user(user_id):
    return test_user.query.get(int(user_id))

#Sets up object based handling for tables in MySQL db. Class names match table names in db,
    #and each column and pk/fk has to be defined here.
class test_user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    #Backref allows access to the test_user entry from a test_post entry (ex. 
        #for post in test_post:
            #print(post.author.username) will print the username of the author of the post)
    posts = db.relationship('test_post', backref = 'author', lazy = True)

    def __repr__(self):
        return f'test_user("{self.username}", "{self.email}", "{self.image_file}")'
    
class test_post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('test_user.id'), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f'test_post("{self.title}", "{self.date_posted}")'
    
