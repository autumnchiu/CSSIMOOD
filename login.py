from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from datetime import datetime, timedelta
# from datetime import datetime
#from html import HTML

JINJA_ENV = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape =True
)

DESCRIPTION = {
'I laughed': {'feeling': 'joyful',
              'color': '#02BCB8',
			  'index': 1},
'I feel energetic': {'feeling':'joyful',
                     'color': '#05ABC0',
					 'index': 1},
'I smiled': {'feeling': 'joyful',
             'color':'#025D9C',
			 'index': 1},
'I feel confident': {'feeling': 'powerful',
                     'color': '#97D4D1',
					 'index': 1},
'I feel appreciated': {'feeling': 'powerful',
                        'color':'#6BB9C6',
						'index': 1},
'I feel valuable': {'feeling': 'powerful',
                        'color':'#5D4E4F',
						'index': 1},
'I am thankful': {'feeling': 'peaceful',
                  'color': '#3C9BD1',
				  'index': 1},
'I am content': {'feeling':'peaceful',
                 'color':'#486476',
				 'index': 1},
'I feel relaxed': {'feeling': 'peaceful',
                   'color':'#B4A893',
				   'index': 1},
'I feel burnt out': {'feeling':'sad',
                     'color':'#F1C131',
					 'index': -1},
'I am homesick': {'feeling':'sad',
                    'color':'#F1DD48',
					'index': -1},
'I feel like an imposter': {'feeling':'sad',
                            'color':'#F1AD48',
							'index': -1},
'I am annoyed': {'feeling':'mad',
                 'color':'#F1AD7C',
				 'index': -1},
'I am cranky': {'feeling':'mad',
                'color': '#F1ADA1',
				'index': -1},
'I feel betrayed': {'feeling': 'mad',
                    'color':'#EDADC3',
					'index': -1},
'I am embarassed': {'feeling':'scared',
                    'color':'#FBDDCE',
					'index': -1},
'I feel vulnerable': {'feeling':'scared',
                      'color':'#AED8BD',
					  'index': -1},
'I feel helpless': {'feeling': 'scared',
                    'color':'#BED85E',
					'index': -1},
}

class Feelings(ndb.Model):
    chosen_emotion = ndb.StringProperty();
    chosen_intensity = ndb.IntegerProperty();
    chosen_reason = ndb.StringProperty();
    chosen_time = ndb.DateTimeProperty();
    user = ndb.StringProperty();
#p = Feelings(chosen_emotion = "angry", chosen_intensity = 7, chosen_reason="I hate my life", chosen_time="September 7")
#p.put();

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome! (<a href="{}">sign out</a>)'.format(
                logout_url)
            self.redirect('/homepage')
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
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
        logout_url = users.create_logout_url('/')
        signout = 'Sign Out'
        link = logout_url
        self.response.write(content.render(emotions=DESCRIPTION, signout=signout, link=link))


class EmotionHandler(webapp2.RequestHandler):
    def dispatch(self):
        my_emotion = self.request.get('emotion')
        #self.response.out.write('The emotion entered was: ' + my_emotion)
        emotionpage = JINJA_ENV.get_template('templates/emotionpage.html')
        self.response.write(emotionpage.render(emotion=my_emotion, color = DESCRIPTION[my_emotion]['color']))

class aboutpageHandler(webapp2.RequestHandler):
    def get(self):
        about_template = JINJA_ENV.get_template('templates/about.html')
        self.response.write(about_template.render())


class dailyLog(webapp2.RequestHandler):
    def post(self):
        answer = self.request.get('answer')
        intensityAnswer = int(self.request.get('intensityAnswer'))
        my_emotion = self.request.get('my_emotion')
        time = datetime.now()
        #time = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        #self.response.write(answer)
        EmotionData = Feelings(chosen_reason =answer,chosen_intensity =intensityAnswer, chosen_emotion=my_emotion, chosen_time=time, user = users.get_current_user().user_id())
		#e = Feelings(chosen_emotion = "sad", chosen_intensity = 3)
		#e.put()
        EmotionData.put()
        self.redirect('/dailylog')

    def get(self):
        table_template = JINJA_ENV.get_template('templates/table/index.html')
        today = datetime.today()
        date = datetime(today.year,today.month,today.day)
        print date

        tableData = Feelings.query(
    		ndb.AND(Feelings.chosen_time >= date,
            Feelings.chosen_time < date + timedelta(days=1), Feelings.user == users.get_current_user().user_id())).order(Feelings.chosen_time)
        self.response.write(table_template.render(tableData = tableData))

class StyleHandler(webapp2.RequestHandler):
    def get(self):
        with open('templates/logs.css', 'r') as f:
            self.response.write(f.read())

class dailyGraphHandler(webapp2.RequestHandler):
    def get(self):
        xAxis = []
        yAxis = []
        user = users.get_current_user()
        current_date = datetime.now().replace(hour=0, minute=0, second=0)
        my_todays_entries = (Feelings.query()
                .filter(ndb.AND(
                                Feelings.user == user.user_id(),
                                Feelings.chosen_time >= current_date,
                                ))
                .order(Feelings.chosen_time)
                .fetch())
        #allTimes = Feelings.query().filter(Feelings.user == user.user_id())
        #index = DESCRIPTION[my_emotion]['index']
        for entry in my_todays_entries:
            #print(time.chosen_time)
            print(datetime.strftime(entry.chosen_time, '%H:%M'))
            #print(chosen_intensity)
            index = DESCRIPTION[entry.chosen_emotion]['index']
            xAxis.append(datetime.strftime(entry.chosen_time, '%H:%M'))
            yAxis.append(index*entry.chosen_intensity)
        #data = [-1,3,-15,2,7,26,82,172,312,433]
        dailygraph = JINJA_ENV.get_template('templates/dailygraph.html')
        self.response.write(
                dailygraph.render(
                        xAxis = xAxis,
                        yAxis=yAxis))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/homepage', homePage),
    ('/admin', AdminPage),
    ('/emotion', EmotionHandler),
	# ('/calendar', CalendarHandler),
	('/about', aboutpageHandler),
    ('/logs.css', StyleHandler),
    ('/dailylog', dailyLog),
    ('/dailygraph', dailyGraphHandler)
], debug=True)
