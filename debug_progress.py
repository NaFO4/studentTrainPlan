import pymysql
from config import config

def inspect_student_progress():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=config['MYSQL_PASSWORD'],
        database=config['DATABASE_NAME'],
        charset='utf8mb4'
    )
    
    try:
        with conn.cursor() as cursor:
            # 1. 获取一个测试学生ID
            cursor.execute("SELECT STU_NO FROM STUDENT LIMIT 1")
            stu_id = cursor.fetchone()
            if not stu_id:
                print("Error: No students found in database.")
                return
            stu_id = stu_id[0]
            print(f"Checking progress for student: {stu_id}")
            
            # 2. 查看 EDU_STU_PLAN 中的 FINISHED_CO
            cursor.execute(f"SELECT FINISHED_CO FROM EDU_STU_PLAN WHERE STU_NO='{stu_id}'")
            result = cursor.fetchone()
            if not result:
                print(f"Error: No plan record found for student {stu_id}")
                return
                
            finished_co = result[0]
            print(f"FINISHED_CO string length: {len(finished_co) if finished_co else 0}")
            print(f"FINISHED_CO content: {finished_co}")
            
            if not finished_co or '1' not in finished_co:
                print("Warning: FINISHED_CO contains no '1's (no completed courses). This explains the empty progress bars.")
                
                # Propose a fix: Simulate some completed courses
                print("\nAttempting to simulate data...")
                # 创建一个包含一些1的字符串 (长度120左右)
                mock_finished = '1' * 60 + '0' * 60 
                # 截取或填充到正确长度，这里假设原来的长度也是合适的，或者直接更新
                # 注意：这只是测试脚本，实际逻辑需要根据 EDUCATION_PLAN 的 CO_100 对应关系来
                
                # 让我们看看 EDUCATION_PLAN 有多少课程
                cursor.execute("SELECT COUNT(*) FROM EDUCATION_PLAN")
                count = cursor.fetchone()[0]
                print(f"Total courses in EDUCATION_PLAN: {count}")
                
    finally:
        conn.close()

if __name__ == "__main__":
    inspect_student_progress()
