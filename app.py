from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'YouRMySeCReTKeY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Jeremiah@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    post = db.relationship('Post', backref='poster')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, poster):
        self.title = title
        self.body = body
        self.poster = poster


@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Blogz Home'
    return render_template('index.html', title=title)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title = 'Blogz SignUp'

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash('Your password do not match, please try again', 'error')

        else:
            # new_user = User(username, password)
            # db.session.add(new_user)
            # db.session.commit()
            flash('You are now Sign Up!', 'success')
            return redirect(url_for('home'))

    return render_template('signup.html', title=title)


if __name__ == '__main__':
    app.run()
