import mongoengine as me
from flask_mongoengine import MongoEngine
from flask import Flask, request, session, render_template, redirect, url_for
from os import getenv
import datetime as dt
from models import User, Wellness, Note, Concern
from functions import format_current_datetime

def create_app():
    APP = Flask(__name__)
    DB_URI = getenv('MONGODB_URI')
    APP.config['MONGODB_SETTINGS'] = {
            'host': DB_URI,
            'authentication_source': 'admin'
        }
    APP.config['SECRET_KEY'] = getenv('SECRET_KEY')
    DB = MongoEngine(APP)

    @APP.before_first_request
    def make_session_permanent():
        session.permanent = True
        APP.permanent_session_lifetime = dt.timedelta(minutes = 30)


    @APP.route('/', methods = ['POST', 'GET'])
    def root():
        if session.get('username', None) != None:
            session['username'] = ''
            session['password'] = ''
        if request.method == 'POST':
            return redirect(url_for('page_two'))
        return render_template('page_one.html')


    @APP.route('/page_two', methods = ['POST', 'GET'])
    def page_two():
        if session.get('username', None) != None:
            session['username'] = ''
            session['password'] = ''
        if request.method == 'POST':
            if 'continue' in request.form:
                return redirect(url_for('page_three'))
            if 'back' in request.form:
                return redirect('/')
        return render_template('page_two.html')


    @APP.route('/page_three', methods = ['POST', 'GET'])
    def page_three():
        if session.get('username', None) != None:
            session['username'] = ''
            session['password'] = ''
        if request.method == 'POST':
            if 'dashboard' in request.form:
                return redirect(url_for('dashboard'))
            if 'back' in request.form:
                return redirect(url_for('page_two'))
        return render_template('page_three.html')


    @APP.route('/dashboard', methods = ['POST', 'GET'])
    def dashboard():
        if session.get('username', None) != None:
            session['username'] = ''
            session['password'] = ''
        if request.method == 'POST':
            if 'data' in request.form:
                return redirect(url_for('page_three'))
            if 'tracker' in request.form:
                return redirect(url_for('tracker'))
            if 'workouts' in request.form:
                return redirect(url_for('workouts'))
        return render_template('dashboard.html',
            today_date = format_current_datetime())
                                                                                        

    @APP.route('/tracker', methods = ['POST', 'GET'])
    def tracker():
        if session.get('username', None) != None:
            session['username'] = ''
            session['password'] = ''
        if request.method == 'POST':
            if 'create' in request.form:
                return redirect(url_for('signup'))
            if 'login' in request.form:
                return redirect(url_for('login'))
            if 'dashboard' in request.form:
                return redirect(url_for('dashboard'))
        return render_template('tracker.html', status = request.args.get('status') or '')


    @APP.route('/signup', methods = ['POST', 'GET'])
    def signup():
        if session.get('username', None) != None:
            session['username'] = ''
            session['password'] = ''
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            password_conf = request.form.get('password_conf')
            try:
                user = User.objects(username = username)[0]
            except IndexError:
                if (7 < len(username) < 33) and (7 < len(password) < 17):
                    if password == password_conf:
                        new_user = User(username = username, password = password)
                        new_user.save()
                        return redirect(url_for('tracker', status = 'Successfully Created Account'))
                    return render_template('signup.html', error = 'Passwords must match')
                return render_template('signup.html', error = 'Invalid username or password')               
            return render_template('signup.html', error = 'Username already exists')
        return render_template('signup.html')


    @APP.route('/login', methods = ['POST', 'GET'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            try:
                user = User.objects(username = username)[0]
            except IndexError:
                return render_template('login.html', error = 'Error: Could not find username')
            if user.password == password:
                session['username'] = username
                session['password'] = password
                return redirect(url_for('tracker_dash'))
            return render_template('login.html', error = 'Error: Incorrect password')
        return render_template('login.html')


    @APP.route('/tracker_dash', methods = ['POST', 'GET'])
    def tracker_dash():
        if not session.get('username', None):
            return redirect(url_for('tracker'))
        today_date = dt.datetime.today().strftime('%A %B %d, %Y')
        user = User.objects(username = session['username'])[0]
        if request.method == 'POST':
            if 'view' in request.form:
                return redirect(url_for('tracker_view'))
            if 'update' in request.form:
                return redirect(url_for('tracker_update'))
            if 'signout' in request.form:
                session['username'] = ''
                session['password'] = ''
                return redirect(url_for('dashboard'))
        first_log = user.date_created
        return render_template('tracker_dash.html',
            start_date = first_log.date().strftime('%A %B %d, %Y'),
            today_date = today_date)


    @APP.route('/tracker_update', methods = ['POST', 'GET'])
    def tracker_update():
        try:
            user = User.objects(username = session['username'])[0]
        except IndexError:
            return redirect(url_for('tracker'))
        if request.method == 'POST':
            wellness = request.form.get('wellness')
            notes = request.form.get('notes')
            concerns = request.form.get('concerns')
            if wellness.isdigit() and 0 < int(wellness) < 11:
                wellness = Wellness(rating = int(wellness))
                date = wellness.date_entered.date()
                last_20 = [w.date_entered.date() for w in user.wellness[-20:]]
                if last_20.count(date) >= 20:
                    return render_template('tracker_update.html',
                        error = 'Maximum Daily Entries Exceeded')
                notes = Note(text = notes)
                concerns = Concern(text = concerns)
                user.update_wellness(wellness = wellness)
                user.update_notes(notes = notes)
                user.update_concerns(concerns = concerns)
                user.save()
                return redirect(url_for('tracker_dash'))
            return render_template('tracker_update.html', error = 'Error: Invalid rating')
        return render_template('tracker_update.html')


    @APP.route('/tracker_view', methods = ['POST', 'GET'])
    def tracker_view():
        tracker_empty = False
        if request.method == 'POST':
            return redirect(url_for('tracker_dash'))
        try:
            user = User.objects(username = session['username'])[0]
        except IndexError:
            return redirect(url_for('tracker'))
        l = lambda x: [o.text for o in x]
        ratings = [o.rating for o in user.wellness]
        wellness = ratings
        dates = [o.date_entered for o in user.wellness]
        notes, concerns = [l(o) for o in [user.notes, user.concerns]]
        if len(wellness):
            wellness = zip(wellness, notes, concerns, dates)
        else:
            tracker_empty = True
        return render_template('tracker_view.html',
            wellness_ratings = ratings,
            wellness = wellness,
            dates = dates,
            tracker_empty = 'Your tracker is currently empty' if tracker_empty else '')


    @APP.route('/workouts', methods = ['POST', 'GET'])
    def workouts():
        return render_template('workouts.html')

    DB.disconnect(alias = DB_URI)
    return APP
 
    
# if __name__ == '__main__':
#     APP.run(debug = True)



