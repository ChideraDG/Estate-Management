import pymysql

pymysql.install_as_MySQLdb()

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database=''
)

my_cursor = connection.cursor()

# creates an estate database for new developers
create_database = 'create database if not exists estate_db'

my_cursor.execute(create_database)
my_cursor.close()
