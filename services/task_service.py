
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

from models.task import taskCreate,taskEdit

connection_pool = pool.SimpleConnectionPool(
    1, 10,
    dbname="bim",
    user="openpg",
    password="openpgpwd",
    host="localhost",
    port="5432"
)

def get_db_connection():
    return connection_pool.getconn()  # dapatkan koneksi dari pool

def release_db_connection(conn):
    connection_pool.putconn(conn)  # kembalikan koneksi ke pool


def create_new_task(tasks: taskCreate, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            INSERT INTO tasks (name, globalid, expressid, value, status, user_issued_id, user_assign_id, project_id, location, url_photo, start_date, end_date, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
            RETURNING id;
        """
        cursor.execute(sql_command, (
            tasks.name,
            tasks.globalid,
            tasks.expressid,
            tasks.value,
            tasks.status,
            tasks.user_issued_id,
            tasks.user_assign_id,
            tasks.project_id,
            tasks.location,
            filename,
            tasks.start_date,
            tasks.end_date
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil tambah task", "data": new_id}

        return response

        # return {"status": "ok", "message": "berhasil tambah task", "data": tasks, "filename": filename}

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal tambah task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def edit_task(tasks: taskEdit, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE tasks SET name=%s,  globalid=%s, expressid=%s, value=%s, status=%s, user_issued_id=%s, user_assign_id=%s, project_id=%s, location=%s, url_photo=%s, start_date=%s, end_date=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.name,
            tasks.globalid,
            tasks.expressid,
            tasks.value,
            tasks.status,
            tasks.user_issued_id,
            tasks.user_assign_id,
            tasks.project_id,
            tasks.location,
            filename,
            tasks.start_date,
            tasks.end_date,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit task", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal edit task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def edit_task_nofile(tasks: taskEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE tasks SET name=%s,  globalid=%s, expressid=%s, value=%s, status=%s, user_issued_id=%s, user_assign_id=%s, project_id=%s, location=%s, start_date=%s, end_date=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.name,
            tasks.globalid,
            tasks.expressid,
            tasks.value,
            tasks.status,
            tasks.user_issued_id,
            tasks.user_assign_id,
            tasks.project_id,
            tasks.location,
            tasks.start_date,
            tasks.end_date,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit task", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal edit task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def delete_task(tasks: taskEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            DELETE FROM tasks where id=%s returning id;
        """
        cursor.execute(sql_command, (
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil delete task", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal delete task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def getAllTasksDone(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command="""
        select t.project_id, t.name, t.id, t.globalid, t.expressid,t.value,t.start_date,t.end_date,u.name as assign_to,u2.name as issued_by,t.location
        from tasks t
        left join users u on t.user_assign_id = u.id
        left join users u2 on t.user_issued_id = u2.id
        where t.status ='done' and t.project_id=%s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data task selesai","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data task selesai","result":""}
        return response
    
    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal delete task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def getAllTasks(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql_command="""
        select t.project_id, t.status, t.name, t.id, t.globalid, t.expressid,t.value,t.start_date,t.end_date,u.name as assign_to,u2.name as issued_by,t.location
        from tasks t
        left join users u on t.user_assign_id = u.id
        left join users u2 on t.user_issued_id = u2.id
        where t.project_id=%s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data task","result":record};
        else:
            response = {"status":"nok","message":"gagal dapat data task","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection


# if __name__ == "__main__":
#     import sys

#     if len(sys.argv) > 1 and sys.argv[1] == "get_all_project":
#         projects = get_all_project()
#         if projects:
#             for project in projects:
#                 print(project)
#         else:
#             print("No projects found or error occurred.")
