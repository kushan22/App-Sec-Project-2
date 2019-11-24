from flask import Flask,redirect, escape,session,request,url_for
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config

import json,shlex,subprocess
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse



app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import User,UserQueries
from forms import RegisterForm,LoginForm,SpellCheckerForm
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)

SELF= "'self'"

content_security_policy = {
    'default-src': [SELF,'cdnjs.cloudflare.com'],
    'img-src': '*',
    'script-src': [
        SELF,
        'cdnjs.cloudflare.com',
    ],
    'style-src': [
        SELF,
        'cdnjs.cloudflare.com',
    ],
}



# data = []

@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = content_security_policy
    resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
    resp.headers['X-XSS-Protection'] = '1; mode=block'
    return resp


@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route('/spell_check',methods=['GET','POST'])
@login_required
def home():
    # if 'username' not in session:
    #     return redirect(url_for('login'))

    misspelledarr = []
    form = SpellCheckerForm()
    sentence=""
    if form.validate_on_submit():
        sentence = escape(form.wordsToCheck.data.strip())
        with open("words.txt",'w') as f:
            f.write(sentence)
        cmd = "./spell_check words.txt wordlist.txt"
        process = subprocess.Popen(shlex.split(cmd),shell=False,stdout=subprocess.PIPE)

        misspelled = process.communicate()[0]
        misspelledarr = misspelled.decode('utf-8').strip().split('\n')


    return render_template('home.html',form=form,length=len(misspelledarr),misspelled=misspelledarr,suppliedText=sentence)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()

    if form.validate_on_submit():
        if (User.query.filter_by(username=escape(form.username.data)).first()) is not None:
            error = True
            return render_template('register.html',form=form,error=error),406
        user = User(username=escape(form.username.data),password_hash=bcrypt.generate_password_hash(escape(form.password.data)).decode('utf-8'),twoFactAuth=escape(form.twoFactAuth.data))

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    error = None
    return render_template('register.html',form=form,error=error)


    # if 'username' in session:
    #     return redirect('/')
    # form = RegisterForm()
    #
    # userDetails = {}
    #
    # if request.method == 'POST' and form.validate_on_submit():
    #     with open("./database/users.json","r") as fp:
    #         users = json.loads(fp.read())
    #     for d in users:
    #         if d['username'] == form.username.data:
    #             error=True
    #             return render_template('register.html',form=form,error=error),406
    #     userDetails['username'] = escape(form.username.data)
    #     userDetails['password'] = bcrypt.generate_password_hash(escape(form.password.data)).decode('utf-8')
    #     userDetails['twoFactAuth'] = escape(form.twoFactAuth.data)
    #
    #     users.append(userDetails)
    #     with open('./database/users.json','w') as f:
    #         json.dump(users,f)
    #
    #     return redirect(url_for('login'))
    # error = None
    # # print(form.errors)
    # return render_template('register.html',form=form,error = error)

@app.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=escape(form.username.data)).first()
        if user is None or not bcrypt.check_password_hash(user.password_hash,escape(form.password.data)):
            status = 2
            return render_template('login.html',form = form,status=status)
        elif user is not None and bcrypt.check_password_hash(user.password_hash,escape(form.password.data)) and user.twoFactAuth != escape(form.twoFactAuth.data):
            status = 1
            return render_template('login.html',form=form,status=status)

        login_user(user,remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    status = None
    return render_template('login.html',form=form,status=status)

    # if 'username' in session:
    #     return redirect(url_for('home'))
    # form = LoginForm()
    # userName = escape(form.username.data)
    # password = escape(form.password.data)
    # twoFactAuth = escape(form.twoFactAuth.data)
    # if form.validate_on_submit():
    #
    #     with open("./database/users.json","r") as f:
    #         users = json.loads(f.read())
    #     for d in users:
    #         if d['username'] == userName and bcrypt.check_password_hash(d['password'],password) and d['twoFactAuth'] == twoFactAuth:
    #             session['username'] = userName
    #             return redirect(url_for('home'))
    #         elif d['username'] == userName and bcrypt.check_password_hash(d['password'],password) and d['twoFactAuth'] != twoFactAuth:
    #             status = 1
    #             return render_template('login.html',form=form,status=status)
    #     status = 2
    #     return render_template('login.html',form=form,status=status)
    # status = None


@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'UserQueries':UserQueries}


if __name__ == '__main__':
    app.run()
