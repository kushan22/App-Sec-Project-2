from app import app,db

from app.models import User,UserQueries,UserLogs

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'UserQueries':UserQueries,'UserLogs':UserLogs}


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')