from flask import Flask,redirect, escape,request,url_for
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config

import json,shlex,subprocess
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse
from datetime import datetime



app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import User,UserQueries,UserLogs
from forms import RegisterForm,LoginForm,SpellCheckerForm,AdminHistoryForm,UserLogsForm
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

        user_id = current_user.get_id()
        user_queries = UserQueries(sentence=sentence,misspelled_words=misspelled.decode('utf-8'),user_id=user_id)
        db.session.add(user_queries)
        db.session.commit()



    return render_template('home.html',form=form,length=len(misspelledarr),misspelled=misspelledarr,suppliedText=sentence)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()

    if form.validate_on_submit():
        if (User.query.filter_by(username=escape(form.username.data)).first() is not None):
            error = True
            return render_template('register.html',form=form,error=error)
        elif (User.query.filter_by(username=escape(form.username.data)).first() is not None) and (User.query.filter_by(twoFactAuth=escape(form.twoFactAuth.data)).first() is not None):
            error = True
            return render_template('register.html',form=form,error=error)
        user = User(username=escape(form.username.data),password_hash=bcrypt.generate_password_hash(escape(form.password.data)).decode('utf-8'),twoFactAuth=escape(form.twoFactAuth.data))

        db.session.add(user)
        db.session.commit()
        error = False
        return render_template('register.html',form=form,error=error)
        # return redirect(url_for('login'))
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



        user_logs = UserLogs(login_time=datetime.utcnow(),user_id=user.id)
        db.session.add(user_logs)
        db.session.commit()
        login_user(user,remember=True)
        status = 0
        return render_template('login.html',form=form,status=status)

        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('home')
        # return redirect(next_page)
    status = None
    return render_template('login.html',form=form,status=status)

    # if 'username' in session:rue : User can't view queries
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
    recentLog = db.session.query(UserLogs).order_by(UserLogs.id.desc()).first()
    if (recentLog is not None):
        recentLog.logout_time = datetime.utcnow()
        db.session.commit()
    logout_user()
    return redirect(url_for('home'))

@app.route('/history',methods=['GET','POST'])
@login_required
def history():
    num_of_queries = 0
    userQueries = None
    if current_user.username == 'admin':
        form = AdminHistoryForm()
        if form.validate_on_submit():
            username = escape(form.username.data)
            user = User.query.filter_by(username=username).first()
            if user is not None:
                userid = User.query.filter_by(username=username).first().id
                userQueries = UserQueries.query.filter_by(user_id=userid).all()
                num_of_queries = len(userQueries)


        return render_template('admin_history.html',form=form,num_of_queries=num_of_queries,userQueries=userQueries)


    user_id = current_user.get_id()

    userQueries = UserQueries.query.filter_by(user_id=user_id).all()
    num_of_queries = len(userQueries)
    return render_template("history.html",num_of_queries = num_of_queries,userQueries = userQueries)


@app.route('/history/query<query_id>')
@login_required
def query_review(query_id):


    query = UserQueries.query.filter_by(id = query_id).first()
    userId = query.user_id;

    current_user_id = current_user.get_id()
    if current_user.username != 'admin':
        if int(current_user_id) != int(userId):
            return render_template("error.html"),401

    username = current_user.username

    queryText = query.sentence
    queryResult = query.misspelled_words.strip().split("\n")

    return render_template('query_review.html',query_id=query_id,username=username,queryText=queryText,queryResult=queryResult)


@app.route('/login_history',methods=["GET","POST"])
@login_required
def login_history():
    num_of_logs = 0
    userlogs = None
    if current_user.username != "admin":
        return render_template('error.html')

    form = UserLogsForm()
    if form.validate_on_submit():
        userid = escape(form.userid.data)
        userlogs = UserLogs.query.filter_by(user_id = userid).all()
        num_of_logs = len(userlogs)

        # return render_template('login_history.html',form=form,num_of_logs=num_of_logs,userlogs=userlogs)

    return render_template('login_history.html',form=form,num_of_logs=num_of_logs,userlogs=userlogs)



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'UserQueries':UserQueries,'UserLogs':UserLogs}


if __name__ == '__main__':
    app.run()
