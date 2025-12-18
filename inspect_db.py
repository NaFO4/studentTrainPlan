import pymysql
from config import config

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password=config['MYSQL_PASSWORD'],
        database=config['DATABASE_NAME'],
        charset='utf8mb4'
    )

def inspect_data():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 查看课程分类和总学分
            print("--- Course Classifications & Total Credits ---")
            cursor.execute("""
                SELECT CLASSIFICATION, SUM(CREDITS) 
                FROM EDUCATION_PLAN 
                GROUP BY CLASSIFICATION
            """)
            for row in cursor.fetchall():
                print(row)
                
            # 查看学生选课情况样例
            print("\n--- Student Chosen Courses Sample ---")
            cursor.execute("SELECT * FROM CHOOSE LIMIT 5")
            for row in cursor.fetchall():
                print(row)

            # 查看EDU_STU_PLAN样例
            print("\n--- EDU_STU_PLAN Sample ---")
            cursor.execute("SELECT * FROM EDU_STU_PLAN LIMIT 1")
            for row in cursor.fetchall():
                print(row)
                
    finally:
        conn.close()

if __name__ == "__main__":
    inspect_data()
