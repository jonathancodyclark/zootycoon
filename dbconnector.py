import pymysql
#peyton was here
# Open database connection
db = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306,
                     user='cs4400_group14', passwd='AMEb4bEi', db='cs4400_group14')

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute("show tables")
'''
cursor.execute("CREATE TABLE exhibits ("
               "name_exhibit varchar(100) NOT NULL, "
               "water_feature boolean NOT NULL, "
               "size int NOT NULL, "
               "PRIMARY KEY (name_exhibit))")

cursor.execute("insert into exhibits values ('polar', TRUE, '5')")
'''
cursor.execute("select * from exhibits")
tables = cursor.fetchall()
print(tables)
db.close()

'''
# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS rsstracker")

# Create table as per requirement
sql = """CREATE TABLE rsstracker (
   article_title  varchar(255),
   article_url  varchar(1000),
   article_summary varchar(1000)
   summary )"""
cursor.execute(sql)

# disconnect from server
db.close()
'''
