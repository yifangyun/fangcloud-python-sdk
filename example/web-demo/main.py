import threading

import tornado.ioloop
import tornado.web
import utils

from config import Config
from fangcloud.exceptions import OAuthCodeParamError, OAuthRedirectParamError
from fangcloud.oauth import FangcloudOAuth2FlowBase
from fangcloud.yifangyun import YfyInit
from user_database import UserDatabase
from session import MemorySession


YfyInit.init_yifangyun(Config.client_id, Config.client_secret)


class SessionHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def initialize(self):
        self.session_obj = MemorySession(self)

    def get_session_obj(self, obj_key):
        return self.session_obj.__getitem__(obj_key)

    def set_session_obj(self, obj_key, obj_value):
        self.session_obj.__setitem__(obj_key, obj_value)

    def del_session_obj(self, obj_key):
        self.session_obj.__delitem__(obj_key)


class BasicHandler(SessionHandler):

    __lock__ = threading.Lock()
    __database__ = UserDatabase("user.db")
    __oauth__ = FangcloudOAuth2FlowBase()

    def get_login_user(self):
        return self.get_session_obj("login_user")

    def set_login_user(self, username):
        self.set_session_obj("login_user", username)

    def user_logout(self):
        self.del_session_obj("login_user")

    def set_state(self, value):
        self.set_session_obj("state", value)

    def get_state(self):
        return self.get_session_obj("state")


class IndexHandler(BasicHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        username = self.get_login_user()
        user = self.__database__.get_user(username)

        if user is not None:
            self.redirect("/home")
            return

        self.write(
            """
            <html>
                <head><title>Home - Web Demo</title></head>
                <body>
                    <h2>Log in</h2>
                    <form action='/login' method='POST'>
                        <p>Username: <input name='username' type='text' /> (pick whatever you want)</p>
                        <p>No password needed for this tiny example.</p>
                        <input type='submit' value='Login' />
                    </form>
                </body>
            </html>
            """
        )
        self.flush()


class LoginHandler(BasicHandler):

    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        username = self.get_argument("username", None)
        if username is None:
            self.send_error(400, reason="Missing field \"username\"")
            return

        with self.__lock__:
            user = self.__database__.get_user(username)
            if user is None:
                self.__database__.add_user(username)
                self.__database__.save_user_db()
        self.set_login_user(username)
        self.redirect("/")


class LogoutHandler(BasicHandler):

    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        self.user_logout()
        self.redirect("/")


class HomeHandler(BasicHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        username = self.get_login_user()
        user = self.__database__.get_user(username)

        if user is None:
            self.redirect("/")
            return

        self.write(
            """
            <html>
            <head><title>Home - Web demo</title></head>
            <body>
            <h2>User: %s</h2>
            """ % username
        )
        if user.access_token is not None:
            pass
        else:
            self.write(
                """
                <p><form action='/fangcloud-auth-start' method='POST'>
                <input type='submit' value='Link to your Fangcloud account' />
                </form></p>
                """
            )
        self.write(
            """
            <p><form action='/logout' method='POST'>
            <input type='submit' value='Logout' />
            </form></p>
            </body>
            </html>
            """
        )
        self.flush()


class AuthStartHandler(BasicHandler):

    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        username = self.get_login_user()
        user = self.__database__.get_user(username)

        # check user login
        if user is None:
            response_page = utils.build_page("Error", "This page requires a logged-in user.  Nobody is logged in.")
            self.write(response_page)
            return

        # create a random stats, used for CSRF or remember web service current stats
        state = utils.generate_new_state()
        # the state can be stored in session
        self.set_state(state)
        # use SDK to fetch authorized url
        authorize_url = self.__oauth__.get_authorize_url(Config.redirect_url, state)
        self.redirect(authorize_url)


class AuthFinishHandler(BasicHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        code = self.get_argument("code", None)
        state = self.get_argument("state", None)
        username = self.get_login_user()
        user = self.__database__.get_user(username)
        if user is None:
            response_page = utils.build_page("Error", "This page requires a logged-in user.  Nobody is logged in.")
            self.write(response_page)
            return

        # check state
        state_in_session = self.get_state()
        if state != state_in_session:
            # self.send_error(400, reason="On /fangcloud-auth-finish: Wrong state received")
            # return
            pass
        try:
            result = self.__oauth__.authenticate(code, Config.redirect_url)
        except OAuthCodeParamError:
            self.send_error(400, reason="On /fangcloud-auth-finish: Wrong oauth code to fetch oauth token in finish")
            return
        except OAuthRedirectParamError:
            self.send_error(400, reason="On /fangcloud-auth-finish: Wrong oauth redirect url to fetch oauth in finish")
            return

        # here, we need to store result.access_token, result.refresh_token and result.expires_in into self defined database in real application

        self.write(str(result))


def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/home", HomeHandler),
        (r"/fangcloud-auth-start", AuthStartHandler),
        (r"/fangcloud-auth-finish", AuthFinishHandler),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8088)
    tornado.ioloop.IOLoop.current().start()