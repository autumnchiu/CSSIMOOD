from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
import datetime
# from datetime import datetime
#from html import HTML

JINJA_ENV = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape =True
)

DESCRIPTION = {
'I laughed': {'feeling': 'joyful',
              'color': '#EA76FF',
			  'index': '1'},
'I feel energetic': {'feeling':'joyful',
                     'color': '#FF43CA',
					 'index': '1'},
'I smiled': {'feeling': 'joyful',
             'color':'#FF184D',
			 'index': '1'},
'I feel confident': {'feeling': 'powerful',
                     'color': '#FFCB33'},
'I feel appreciated': {'feeling': 'powerful',
                        'color':'#DA841D'},
'I feel valuable': {'feeling': 'powerful',
                        'color':'#FF4D09'},
'I am thankful': {'feeling': 'peaceful',
                  'color': '#ACFF3A'},
'I am content': {'feeling':'peaceful',
                 'color':'#8BDA33'},
'I feel relaxed': {'feeling': 'peaceful',
                   'color':'#62C74A'},
'I feel burnt out': {'feeling':'sad',
                     'color':'#91F6FF'},
'I am homesick': {'feeling':'sad',
                    'color':'#38FFAF'},
'I feel like an imposter': {'feeling':'sad',
                            'color':'#61FAFF'},
'I am annoyed': {'feeling':'mad',
                 'color':'#9890FF'},
'I am cranky': {'feeling':'mad',
                'color': '#817BD9'},
'I feel betrayed': {'feeling': 'mad',
                    'color':'#966FC4'},
'I am embarassed': {'feeling':'scared',
                    'color':'#96485C'},
'I feel vulnerable': {'feeling':'scared',
                      'color':'#BF4C47'},
'I feel helpless': {'feeling': 'scared',
                    'color':'#BF4047'},
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
        # [START user_details]
        user = users.get_current_user()
        if user:
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome! (<a href="{}">sign out</a>)'.format(
                 logout_url)
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
		logout_url = users.create_logout_url('/')
		signout = 'Sign Out'
		link = logout_url

        # description = {
        # 'I laughed': {'feeling': 'joyful',
        #               'color': '#EA76FF'},
        # 'I feel energetic': {'feeling':'joyful',
        #                      'color': '#FF43CA'},
        # 'I smiled': {'feeling': 'joyful',
        #              'color':'#FF184D'},
        # 'I feel confident': {'feeling': 'powerful',
        #                      'color': '#FFCB33'},
        # 'I feel appreciated': {'feeling': 'powerful',
        #                         'color':'#DA841D'},
        # 'I feel valuable': {'feeling': 'powerful',
        #                         'color':'#FF4D09'},
        # 'I am thankful': {'feeling': 'peaceful',
        #                   'color': '#ACFF3A'},
        # 'I am content': {'feeling':'peaceful',
        #                  'color':'#8BDA33'},
        # 'I feel relaxed': {'feeling': 'peaceful',
        #                    'color':'#62C74A'},
        # 'I feel burnt out': {'feeling':'sad',
        #                      'color':'#91F6FF'},
        # 'I am homesick': {'feeling':'sad',
        #                     'color':'#38FFAF'},
        # 'I feel like an imposter': {'feeling':'sad',
        #                             'color':'#61FAFF'},
        # 'I am annoyed': {'feeling':'mad',
        #                  'color':'#9890FF'},
        # 'I am cranky': {'feeling':'mad',
        #                 'color': '#817BD9'},
        # 'I feel betrayed': {'feeling': 'mad',
        #                     'color':'#966FC4'},
        # 'I am embarassed': {'feeling':'scared',
        #                     'color':'#96485C'},
        # 'I feel vulnerable': {'feeling':'scared',
        #                       'color':'#BF4C47'},
        # 'I feel helpless': {'feeling': 'scared',
        #                     'color':'#BF4047'},


        # }
        # params['emotions'] = [
        #     'I laughed',
        #     'I feel confident',
        #     'I feel energetic',
        #     'I smiled',
        #     'I am thankful',
        #     'I am annoyed',
        #     'I feel like an imposter',
        #     'I want to sleep',
        #     'I am cranky',
        #     'I am homesick',
        #     'I feel vulnerable',
        #     'I feel burnt out',
        #     'I am jealous',
        #     'I feel betrayed',
        #     'I feel weak',
        # ]

        self.response.write(content.render(emotions=DESCRIPTION, signout=signout, link=link))


class EmotionHandler(webapp2.RequestHandler):
    def dispatch(self):
        my_emotion = self.request.get('emotion')
        #self.response.out.write('The emotion entered was: ' + my_emotion)
        emotionpage = JINJA_ENV.get_template('templates/emotionpage.html')
        self.response.write(emotionpage.render(emotion=my_emotion, color = DESCRIPTION[my_emotion]['color']))

# class CalendarHandler(webapp2.RequestHandler):
# 	def get(self):
# 		calendar_template = JINJA_ENV.get_template('templates/dailylog.html')
# 		var = {
# 		'month': 'July',
# 		'year': '2018',
# 		'weeks_in_month': [
# 		[1,2,3,4,5,6,7],
# 		[8,9,10,11,12,13,14],
# 		[15,16,17,18,19,20,21],
# 		[22,23,24,25,26,27,28],
# 		[29,30,31]
# 		]
# 		}
# 		self.response.write(calendar_template.render(var))

class aboutpageHandler(webapp2.RequestHandler):
	def get(self):
		about_template = JINJA_ENV.get_template('templates/about.html')
		self.response.write(about_template.render())

class dailyLog(webapp2.RequestHandler):
    def post(self):
		answer = self.request.get('answer')
		intensityAnswer = int(self.request.get('intensityAnswer'))
		my_emotion = self.request.get('my_emotion')
		time = datetime.datetime.now()
        #time = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        #self.response.write(answer)
		EmotionData = Feelings(chosen_reason =answer,chosen_intensity =intensityAnswer, chosen_emotion=my_emotion, chosen_time=time, user = users.get_current_user().user_id())
		#e = Feelings(chosen_emotion = "sad", chosen_intensity = 3)
		#e.put()
		EmotionData.put()
		self.redirect('/dailylog')

    def get(self):

		table_template = JINJA_ENV.get_template('templates/table/index.html')
		today = datetime.datetime.today()
		date = datetime.datetime(today.year,today.month,today.day)
		print date

		tableData = Feelings.query(

    		ndb.AND(Feelings.chosen_time >= date,
            Feelings.chosen_time < date + datetime.timedelta(days=1), Feelings.user == users.get_current_user().user_id())).order(Feelings.chosen_time)
		#tableData = Feelings.query(Feelings.chosen_time.date() == datetime.today().date()).order(Feelings.chosen_time)
		#htmlcode = HTML.table(tableData)

		#tableData.chosen_emotion = chosen_emotion
		#self.response.write(tableData)
		#for feeling in tableData
		self.response.write(table_template.render(tableData = tableData))

class StyleHandler(webapp2.RequestHandler):
    def get(self):
        with open('templates/logs.css', 'r') as f:
            self.response.write(f.read())

class dailyGraphHandler(webapp2.RequestHandler):
    def get(self):
        xAxis= []
        allTimes = Feelings.query()
        for time in sorted(allTimes, key = lambda t: t.chosen_time):
            print(time.chosen_time)
            print(datetime.datetime.strfttime(time.chosen_time, '%H:%M'))
            xAxis.append(datetime.datetime.strfttime(time.chosen_time, '%H:%M'))
        data = [-1,3,-15,2,7,26,82,172,312,433]
        dailygraph = JINJA_ENV.get_template('templates/dailygraph.html')
        self.response.write(dailygraph.render(xAxis = ','.join(['"%s"'% x for x in xAxis]), data = data))

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
