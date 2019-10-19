from flask import Flask,redirect, escape
from flask_bootstrap import Bootstrap
from flask import render_template
from config import Config
from forms import RegisterForm
import json

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)



data = []

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    error = None
    userDetails = {}
    if form.validate_on_submit():

        # if (form.username.data in data[]):
        #     error = True
        #     return render_template('register.html',form=form,error = error)
        userDetails['username'] = escape(form.username.data)
        userDetails['password'] = escape(form.password.data)
        userDetails['twoFactAuth'] = escape(form.twoFactAuth.data)

        data.append(userDetails)
        # userNames.append(escape(form.username.data))
        # passwords.append(escape(form.password.data))
        # twoFactAuths.append(escape(form.twoFactAuth.data))
        # userDetails["username"] = userNames
        # userDetails["password"] = passwords
        # userDetails["twoFactAuth"] = twoFactAuths
        with open('database/users.json','w') as f:
            json.dump(data,f)
        return redirect('/')

    # print(form.errors)
    return render_template('register.html',form=form,error = error)

@app.route('/login',methods=['GET','POST'])
def login():
    return "Login Page"

@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run()
