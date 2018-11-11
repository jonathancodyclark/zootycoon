import pymysql
from flask import Flask, render_template, url_for
app = Flask(__name__)

db = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306,
                         user='cs4400_group14', passwd='AMEb4bEi', db='cs4400_group14',
                         cursorclass=pymysql.cursors.DictCursor)

cursor = db.cursor()
cursor.execute("select * from exhibits")
zoo_exhibits = cursor.fetchall()



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/exhibits")
def exhibits():
    return render_template('exhibits.html', zoo_exhibits=zoo_exhibits)



'''
cursor.execute("insert into exhibits values ('polar', TRUE, '5')")
cursor.execute("select * from exhibits")
tables = cursor.fetchall()
print (tables)
db.close()
'''