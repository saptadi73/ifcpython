
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

from models.task_activity import taskActivitiesCreate,taskActivitiesEdit

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


def create_new_task_activity(tasks: taskActivitiesCreate, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            INSERT INTO task_activities (activity, date_activity, photo, task_id, user_task_activity_id, created_at)
            VALUES (%s, %s, %s, %s, %s, now())
            RETURNING id;
        """
        cursor.execute(sql_command, (
            tasks.activity,
            tasks.date_activity,
            filename,
            tasks.task_id,
            tasks.user_task_id_activity,
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil tambah aktivitas task", "data": new_id}

        return response

        # return {"status": "ok", "message": "berhasil tambah aktivitas task", "data": tasks, "filename": filename}

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal tambah aktivitas task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def edit_task_activitas(tasks: taskActivitiesEdit, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE task_activities SET activity=%s, date_activity=%s, photo=%s, task_id=%s, user_task_activities_id=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.activity,
            tasks.date_activity,
            filename,
            tasks.task_id,
            tasks.user_task_activities_id,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit aktivitas task", "data": new_id}

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

def edit_task_activities_nofile(tasks: taskActivitiesEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE task_activities SET activity=%s, date_activity=%s, task_id=%s, user_task_activities_id=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.activity,
            tasks.date_activity,
            tasks.task_id,
            tasks.user_task_activities_id,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit aktivitas task", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal edit aktivitas task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def delete_task_activity(tasks: taskActivitiesEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            DELETE FROM task_activities where id=%s returning id;
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
        response={"status": "nok", "message":"berhasil delete task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def getAllTasksActivity(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command="""
        select ta.activity, ta.date_activity , ta.photo, t.name as task, u.name as user
        from task_activities ta
        left join users u on u.id = ta.user_task_activities_id
        left join tasks t on t.id = ta.task_id
        where ta.task_id = %s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data aktivitas task","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data aktivitas task","result":""}
        return response
    
    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"berhasil delete task", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

# if __name__ == "__main__":
#     import sys

#     if len(sys.argv) > 1 and sys.argv[1] == "get_all_project":
#         projects = get_all_project()
#         if projects:
#             for project in projects:
#                 print(project)
#         else:
#             print("No projects found or error occurred.")
