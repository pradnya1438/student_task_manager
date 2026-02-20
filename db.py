from mysql.connector import connect,Error

def get_db_connection():
    try:
        conn=connect(
            host="127.0.0.1",
            user="root",
            password="Pradnya@1008",
            database="student_task_manager"
        )
        if conn.is_connected():
            print("Connected database successfully")
        return conn
    except Error as e:
        print(e)
get_db_connection()