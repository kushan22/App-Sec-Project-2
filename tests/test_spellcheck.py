import unittest
from app import app,db
from models import User,UserQueries



class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        db.session.close()
        db.drop_all()
        db.create_all()

    def tearDown(self) -> None:
        pass


    def register(self,username,password,twoFactAuth):
        return self.app.post(
            '/register',
            data=dict(username=username,password=password,twoFactAuth=twoFactAuth),
            follow_redirects=True
        )



    def login(self,username,password,twoFactAuth):
        return self.app.post(
            '/login',
            data=dict(username=username,password=password,twoFactAuth=twoFactAuth),
            follow_redirects=True
        )

    def spellCheck(self,sentence):
        return self.app.post(
            '/spell_check',
            data=dict(sentence=sentence),
            follow_redirects=True
        )


    def history(self,username):
        return self.app.get(
            '/history',
            query_string=dict(username=username),
            follow_redirects=True
        )





    #
    # def spellcheck(self):
    #     passhttps://github.com/kushan22/App-Sec-Project-2

#Database Models Test

    def test_user_database(self):
        user = User(username="testuser",password_hash="$2b$12$B8UKLo0ORCQOU9c0Sp7lmO5x7ddi43YJeQgnvriVeDOxI2WA6ERh2",twoFactAuth="123456789")
        db.session.add(user)
        db.session.commit()

        users = User.query.all()
        assert user in users


    def test_user_queries(self):

        userquery = UserQueries(sentence="Hey Everything is amazing, What abt you",misspelled_words="abt",user_id=1)
        db.session.add(userquery)
        db.session.commit()

        queries = UserQueries.query.all()
        assert userquery in queries



    def test_valid_user_registration(self):
        response = self.register('rahul','1234','2345')
        self.assertEqual(response.status_code, 200)


    def test_valid_login(self):
        response = self.login("kushan22","1234","9293326764")
        self.assertEqual(response.status_code,200)

    def test_spell_check(self):
        response = self.spellCheck("Wasssup Homie al gd")
        self.assertEqual(response.status_code,200)

    def test_history(self):
        response = self.history("testuser")
        self.assertEqual(response.status_code,200)


















if __name__ == '__main__':
    unittest.main()
