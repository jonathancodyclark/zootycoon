import pymysql
from flask import Flask
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello():
    return "Home Page"

'''
db = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306,
                     user='cs4400_group14', passwd='AMEb4bEi', db='cs4400_group14')

cursor = db.cursor()
cursor.execute("show tables")
tables = cursor.fetchall()
print tables
db.close()
'''
