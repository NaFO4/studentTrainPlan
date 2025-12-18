import pymysql
from config import config

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=config['MYSQL_PASSWORD'],
        charset='utf8mb4'
    )
    print("Successfully connected to MySQL server.")
    
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW DATABASES LIKE '{config['DATABASE_NAME']}'")
        result = cursor.fetchone()
        if result:
            print(f"Database '{config['DATABASE_NAME']}' exists.")
        else:
            print(f"Database '{config['DATABASE_NAME']}' does NOT exist.")
            
    connection.close()
except pymysql.Error as e:
    print(f"Error connecting to MySQL: {e}")
