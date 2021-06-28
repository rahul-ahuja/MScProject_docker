import psycopg2

#making connection to the postgres database
try:
    conn = psycopg2.connect('host=localhost user=postgres password=mypassword')
except:
    conn = psycopg2.connect('host=db user=postgres password=mypassword')

cur = conn.cursor()
conn.set_session(autocommit=True)

#making user the table with same does not exists

#cur.execute('''DROP TABLE IF EXISTS cs_proposals''')
#cur.execute('''DROP TABLE IF EXISTS cs_requests''')
#cur.execute('''DROP TABLE IF EXISTS cs_users''')

#creating users tables in the schema
cur.execute('''CREATE TABLE IF NOT EXISTS cs_users (username TEXT NOT NULL PRIMARY KEY,
    hash TEXT NOT NULL)''')

#creating request tables in the schema
cur.execute('''CREATE TABLE IF NOT EXISTS cs_requests (id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        location TEXT NOT NULL,
        meal_time time without time zone)''')


#creating proposals tables in the schema
cur.execute('''CREATE TABLE IF NOT EXISTS cs_proposals (id SERIAL PRIMARY KEY,
        request_id INTEGER NOT NULL,
        user_to TEXT NOT NULL,
        user_from TEXT NOT NULL)''')



cur.execute('''ALTER TABLE cs_requests ADD CONSTRAINT fk_requests 
        FOREIGN KEY (username) REFERENCES cs_users(username)''')

cur.execute('''ALTER TABLE cs_proposals ADD CONSTRAINT fk_proposals 
        FOREIGN KEY (request_id) REFERENCES cs_requests(id)''')

cur.execute('''ALTER TABLE cs_proposals ADD CONSTRAINT fk_proposals_userto 
        FOREIGN KEY (user_to) REFERENCES cs_users(username)''')

cur.execute('''ALTER TABLE cs_proposals ADD CONSTRAINT fk_proposals_userfrom 
        FOREIGN KEY (user_from) REFERENCES cs_users(username)''')

conn.close() #closing the database connection
