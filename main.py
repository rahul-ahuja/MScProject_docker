# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
import os
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from tempfile import mkdtemp
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from restuarant import findARestaurant

# create the application object
app = Flask(__name__)

# config
#app.secret_key = 'my precious'
app.config.from_object('config.DevelopmentConfig')

csrf = CSRFProtect(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

try:
    conn = psycopg2.connect('host=localhost user=postgres password=mypassword')
except:
    conn = psycopg2.connect('host=db user=postgres password=mypassword')
cur = conn.cursor()
conn.set_session(autocommit=True)

times = [str(t)+':00' for t in range(25)] #this needs to be global list variable

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("user"):
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/requests', methods=["GET", "POST"])
@login_required
def requests():

    name = session["user"]
    if request.method == 'POST':
        request_id = request.form['id']
        request_id = int(list(request_id)[1])

        cur.execute('''SELECT * FROM cs_requests WHERE id = (%s)''', (request_id, ))
        row = cur.fetchone()
        print(row)
        cur.execute('''INSERT INTO cs_proposals (request_id, user_to, user_from)
            VALUES (%s, %s, %s)''', (request_id, row[1], name))

        return redirect(url_for('welcome'))



    cur.execute('''SELECT * FROM cs_requests''')
    req_id = cur.fetchall()
    #print(req_id)
    #API integration
    #req_id is a list, turn it into list of dictionary or sth and make external api call
    #on relevant dict fields or sth before passing to the djinja template

    #req_id = Request.query.all()#db.session.query(Request).all()
    #return render_template('requests.html', meal_type=meal_type, location=location, time=time)
    return render_template('requests.html', req_id=req_id)


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        cur.execute('''SELECT * FROM cs_users WHERE username = (%s)''', (name, ))
        row = cur.fetchall()
        print(row)
        if len(row) != 1 or not check_password_hash(row[0][1], password):
            error = 'Invalid Credentials. Please try again.'
        else:
            session["user"] = row[0][0]
            flash('You were logged in.')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)

@app.route('/', methods=["GET", "POST"])
@csrf.exempt
@login_required
def welcome():
    name = session["user"]
    #return "<h1>{{ session['user'] }}</h1>"
    if request.method == 'POST':
        location = request.form["location"]
        meal_type = request.form["meal_type"]
        time = request.form["time"]
        name = session["user"]
        restuarant = findARestaurant(meal_type, location)
        #print(restuarant)
        if restuarant:
            location = restuarant + ', ' + location

        cur.execute('''INSERT INTO cs_requests (username, meal_type, location, meal_time) 
            VALUES (%s, %s, %s, %s)''', (name, meal_type, location, time))

    return render_template('welcome.html', name=name, times=times)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    error = None
    if request.method == "POST":
        # Query database for username
        name = request.form['username']
        password = request.form['password']
        cur.execute('''SELECT username FROM cs_users WHERE username = (%s)''', (name, ))
        row = cur.fetchall()
        if len(name) == 0 or len(row) > 0:
            error = "the user’s input is blank or the username already exists"
        else:
            cur.execute("INSERT INTO cs_users (username, hash) VALUES (%s, %s)", (name, generate_password_hash(password)))
    return render_template("register.html", error=error)


@app.route("/proposals", methods=["GET", "POST"])
@login_required
def proposals():
    name = session["user"]
    cur.execute('''SELECT p.user_from, r.location, r.meal_type, r.meal_time, p.request_id FROM cs_proposals p
    JOIN cs_requests r ON p.request_id = r.id WHERE user_to = (%s)''', (name, ) )
    prop_row = cur.fetchall()

    if request.method == 'POST':
        proposal_list = list(request.form['prop_id'].split(" "))
        #decide = proposal_list[0]
        req_id = proposal_list[-1][:-1]
        cur.execute("DELETE FROM cs_proposals WHERE request_id = (%s)", (req_id, ) )
        return redirect(url_for('welcome'))

    return render_template('proposals.html', prop_row = prop_row)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You were logged out.')
    return redirect(url_for('welcome'))

@app.route('/test')
def test_web():
    return "<h1> testing again 2 </h1>"


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
