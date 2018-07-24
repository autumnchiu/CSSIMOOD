from google.appengine.api import users
import webapp2
import jinja2
import os

JINJA_ENV = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape =True

)

class MainPage(webapp2.RequestHandler):
    def get(self):
        # [START user_details]
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
            #Redirect to Main Page
            self.redirect('/homepage')
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
        # [END user_details]
        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))

class AdminPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                self.response.write('You are an administrator.')
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')

class homePage(webapp2.RequestHandler):
    def get(self):
        content = JINJA_ENV.get_template('templates/homepage.html')
        params = {}
        params['emotions'] = [
            'Angry',
            'Sad',
            'Happy',
            'Annoyed',
            'Tired',
            'Excited',
            'Sick',
            'Ecstatic',
            'Hungry'
        ]
        self.response.write(content.render(params))

class EmotionHandler(webapp2.RequestHandler):
    def dispatch(self):
        my_emotion = self.request.get('emotion')
        #self.response.out.write('The emotion entered was: ' + my_emotion)
        emotionpage = JINJA_ENV.get_template('templates/emotionpage.html')
        self.response.write(emotionpage.render(emotion=my_emotion))

class submitReason(webapp2.RequestHandler):
    def post(self):
        the_fav_food = self.request.get('answer')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/homepage', homePage),
    ('/admin', AdminPage),
    ('/emotion', EmotionHandler),
], debug=True)
