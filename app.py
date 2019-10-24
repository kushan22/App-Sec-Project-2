from flask import Flask,redirect, escape,session
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config
from forms import RegisterForm,LoginForm,SpellCheckerForm
import json,shlex,subprocess
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)

# data = []

@app.route('/',methods=['GET','POST'])
def home():
    if 'username' not in session:
        return redirect('/login')

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
    form = RegisterForm()

    userDetails = {}
    if form.validate_on_submit():
        with open("database/users.json","r") as fp:
            users = json.loads(fp.read())
        for d in users:
            if d['username'] == form.username.data:
                error = True
                return render_template('register.html',form=form,error=error)
        userDetails['username'] = escape(form.username.data)
        print(bcrypt.generate_password_hash(escape(form.password.data)))
        userDetails['password'] = bcrypt.generate_password_hash(escape(form.password.data)).decode('utf-8')
        userDetails['twoFactAuth'] = escape(form.twoFactAuth.data)

        users.append(userDetails)
        with open('database/users.json','w') as f:
            json.dump(users,f)
        error = False
        return render_template('register.html',form=form,error=error)
    error = None
    # print(form.errors)
    return render_template('register.html',form=form,error = error)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    userName = escape(form.username.data)
    password = escape(form.password.data)
    twoFactAuth = escape(form.twoFactAuth.data)
    if form.validate_on_submit():

        with open("database/users.json","r") as f:
            users = json.loads(f.read())
        for d in users:
            if d['username'] == userName and bcrypt.check_password_hash(d['password'],password) and d['twoFactAuth'] == twoFactAuth:
                status = 0
                session['username'] = userName
                return render_template('login.html',form=form,status=status)
            elif d['username'] == userName and bcrypt.check_password_hash(d['password'],password) and d['twoFactAuth'] != twoFactAuth:
                status = 1
                return render_template('login.html',form=form,status=status)
        status = 2
        return render_template('login.html',form=form,status=status)
    status = None
    return render_template('login.html',form=form,status=status)

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return home()


if __name__ == '__main__':
    app.run()
