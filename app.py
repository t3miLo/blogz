from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user, login_url
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'YouRMySeCReTKeY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Jeremiah@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    if request.method == 'GET':
        flash('Please log in to access this page', 'error')
        return redirect(login_url(url_for('login')))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    posts = db.relationship('Post', backref='poster')

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
    users = User.query.all()
    return render_template('index.html', title=title, users=users)


@app.route('/allPosts', methods=['GET', 'POST'])
def allPosts():
    title = 'All Posts Blogz'
    posts = Post.query.all()
    posts.reverse()
    return render_template('allPosts.html', title=title, posts=posts)


@app.route('/newPost', methods=['GET', 'POST'])
@login_required
def newPost():
    title = 'New Post Blogz'
    print(current_user)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Post(title=title, body=body, poster=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('You have just added a post', 'success')
        return redirect(url_for('allPosts'))
    return render_template('newPost.html', title=title)


@app.route('/singleuser/<int:user_id>')
def singleuser(user_id):
    user = User.query.filter_by(id=user_id).first()
    posts = Post.query.filter_by(poster_id=user_id).all()
    posts.reverse()

    return render_template('singleuser.html', posts=posts, user=user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title = 'Blogz SignUp'

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        exist = User.query.filter_by(username=username).first()

        if password != confirm_password:
            flash('Your password do not match, please try again', 'error')

        else:
            if exist:
                flash(
                    'That username is already being used. Please Login or use a different one.', 'error')
            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                flash('You are now registered!', 'success')
                return redirect(url_for('home'))

    return render_template('signup.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login to Blogz'

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                flash('You have successfully login!', 'success')
                return redirect(url_for('newPost'))
            else:
                flash('Please check you username / password and try again', 'error')
        else:
            print('User Does not exist')
            flash(
                'Sorry check the username or go to register to be able to login', 'error')

    return render_template('login.html', title=title)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user = current_user
    user.authenticated = False
    # db.session.add(user)
    # db.session.commit()
    logout_user()
    flash('You have logout successfully!', 'sucess')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
