import psycopg2
from main import db
from flask_sqlalchemy import SQLAlchemy


'''
class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(32), primary_key=True)
    hash = db.Column(db.String(256))


class Request(db.Model):

    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)
    meal_type = db.Column(db.String, nullable=False)
    location  = db.Column(db.String, nullable=False)
    meal_time = db.Column(db.Time(timezone=False), nullable=False)


class Proposal(db.Model):

    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"), nullable=False)
    user_to = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)
    user_from  = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)
    

db.create_all()
'''


###below is deprecated



#making connection to the postgres database
try:
    conn = psycopg2.connect('host=localhost user=postgres password=mypassword')
except:
    conn = psycopg2.connect('host=db user=postgres password=mypassword')

cur = conn.cursor()
conn.set_session(autocommit=True)

making user the table with same does not exists

cur.execute('''DROP TABLE IF EXISTS proposals''')
cur.execute('''DROP TABLE IF EXISTS requests''')
cur.execute('''DROP TABLE IF EXISTS users''')

#creating users tables in the schema
cur.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL PRIMARY KEY,
    hash TEXT NOT NULL)''')

#creating request tables in the schema
cur.execute('''CREATE TABLE IF NOT EXISTS requests (id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        location TEXT NOT NULL,
        meal_time time without time zone)''')


#creating proposals tables in the schema
cur.execute('''CREATE TABLE IF NOT EXISTS proposals (id SERIAL PRIMARY KEY,
        request_id INTEGER NOT NULL,
        user_to TEXT NOT NULL,
        user_from TEXT NOT NULL)''')



cur.execute('''ALTER TABLE requests ADD CONSTRAINT fk_requests 
        FOREIGN KEY (username) REFERENCES users(username)''')

cur.execute('''ALTER TABLE proposals ADD CONSTRAINT fk_proposals 
        FOREIGN KEY (request_id) REFERENCES requests(id)''')

cur.execute('''ALTER TABLE proposals ADD CONSTRAINT fk_proposals_userto 
        FOREIGN KEY (user_to) REFERENCES users(username)''')

cur.execute('''ALTER TABLE proposals ADD CONSTRAINT fk_proposals_userfrom 
        FOREIGN KEY (user_from) REFERENCES users(username)''')

conn.close() #closing the database connection
