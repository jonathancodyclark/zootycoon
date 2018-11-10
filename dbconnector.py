import pymysql
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# Open database connection
'''
db = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306,
                     user='cs4400_group14', passwd='AMEb4bEi', db='cs4400_group14')

cursor = db.cursor()
cursor.execute("insert into exhibits values ('polar', TRUE, '5')")
cursor.execute("select * from exhibits")
tables = cursor.fetchall()
print (tables)
db.close()
'''