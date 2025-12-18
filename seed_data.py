import pymysql
import random
from config import config

def seed_student_progress():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=config['MYSQL_PASSWORD'],
        database=config['DATABASE_NAME'],
        charset='utf8mb4'
    )
    
    try:
        with conn.cursor() as cursor:
            # 1. 获取测试学生ID (3016216097)
            stu_id = '3016216097'
            print(f"Seeding data for student: {stu_id}")
            
            # 2. 生成随机的完成状态 (118位)
            # 模拟约 60% 的课程已完成
            finished_list = []
            for _ in range(118):
                if random.random() < 0.6:
                    finished_list.append('1')
                else:
                    finished_list.append('0')
            
            finished_co_str = "".join(finished_list)
            
            print(f"Generated FINISHED_CO: {finished_co_str}")
            
            # 3. 更新数据库
            sql = f"UPDATE EDU_STU_PLAN SET FINISHED_CO = '{finished_co_str}' WHERE STU_NO = '{stu_id}'"
            cursor.execute(sql)
            conn.commit()
            
            print("Successfully updated student progress data.")
            
            # 4. 同时为了保证一致性，我们也可以在 CHOOSE 表里添加一些对应的选课记录（可选，但推荐）
            # 获取所有课程
            cursor.execute("SELECT CO_NO, CO_100 FROM EDUCATION_PLAN")
            all_courses = cursor.fetchall()
            
            # 清除旧的选课记录（为了避免主键冲突，简单起见）
            # cursor.execute(f"DELETE FROM CHOOSE WHERE STU_NO = '{stu_id}'")
            
            print("Updating CHOOSE table...")
            for co_no, co_100 in all_courses:
                try:
                    idx = int(co_100) - 1 # CO_100 从 1 开始
                    if 0 <= idx < len(finished_list) and finished_list[idx] == '1':
                        # 插入或更新选课记录
                        # 随机分数 60-100
                        grade = random.randint(60, 100)
                        # 使用 INSERT IGNORE 或 REPLACE
                        insert_sql = f"""
                        REPLACE INTO CHOOSE (AD_YEAR, MAJOR, STU_NO, CO_NO, GRADE, COMMENT)
                        VALUES ('2016', '软件工程', '{stu_id}', '{co_no}', {grade}, '5')
                        """
                        cursor.execute(insert_sql)
                except Exception as e:
                    print(f"Error processing course {co_no}: {e}")
                    
            conn.commit()
            print("Successfully updated CHOOSE table.")

    finally:
        conn.close()

if __name__ == "__main__":
    seed_student_progress()
