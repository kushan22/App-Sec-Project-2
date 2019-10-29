import unittest
import json
from app import app


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self) -> None:
        pass

    #Check for registration
    def register(self,username,password,twoFactAuth):
        return self.app.post(
            '/register',
            data=dict(username=username,password=password,twoFactAuth=twoFactAuth),
            follow_redirects=True
        )



    # def login(self,username,password,twoFactAuth):
    #     return self.app.post(
    #         '/login',
    #         data=dict(username=username,password=password,twoFactAuth=twoFactAuth),
    #         follow_redirects=True
    #     )

    #
    # def spellcheck(self):
    #     pass

    def test_valid_user_registration(self):
        response = self.register('rahul','1234','2345')
        self.assertEqual(response.status_code, 200)
        with open("./database/users.json","r") as fp:
            users = json.loads(fp.read())

        for user in users:
            self.assertNotIn(user['username'],'rahul')











if __name__ == '__main__':
    unittest.main()
