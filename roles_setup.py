import psycopg2

#making connection to the postgres database called meetneat as an owner- Database Admin
try:
    conn = psycopg2.connect('host=localhost user=postgres password=mypassword')
except:
    conn = psycopg2.connect('host=db user=postgres password=mypassword')

cur = conn.cursor()
conn.set_session(autocommit=True)

#creating a role for role-based policy
try:
        cur.execute('''CREATE ROLE readwrite''')
except:
        print('Role already created')



cur.execute('''GRANT CONNECT ON DATABASE postgres TO readwrite''')
cur.execute('''GRANT SELECT, INSERT, UPDATE ON TABLE users TO readwrite''')
cur.execute('''GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE requests TO readwrite''')
cur.execute('''GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE proposals TO readwrite''')
cur.execute('''GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO readwrite''')
cur.execute('''GRANT USAGE ON SCHEMA public TO readwrite''')

#assigning the role to the user called developer4 who will work on the main application
try:
        cur.execute("CREATE USER developer WITH PASSWORD 'dev_pswd'")
except:
        print('User already created')

cur.execute('''GRANT readwrite TO developer''')
conn.close() #closing the database connection

