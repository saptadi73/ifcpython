
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

from models.issue_activity import issueActivitiesCreate,issueActivitiesEdit

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


def create_new_issue_activity(tasks: issueActivitiesCreate, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            INSERT INTO issue_activities (activity, date_activity, photo, issue_id, user_issue_activities_id, created_at)
            VALUES (%s, %s, %s, %s, %s, now())
            RETURNING id;
        """
        cursor.execute(sql_command, (
            tasks.activity,
            tasks.date_activity,
            filename,
            tasks.issue_id,
            tasks.user_issue_activities_id,
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil tambah aktivitas issue", "data": new_id}

        return response

        # return {"status": "ok", "message": "berhasil tambah aktivitas issue", "data": issues, "filename": filename}

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal tambah aktivitas issue", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def edit_issue_activitas(tasks: issueActivitiesEdit, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE issue_activities SET activity=%s, date_activity=%s, photo=%s, issue_id=%s, user_issue_activities_id=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.activity,
            tasks.date_activity,
            filename,
            tasks.issue_id,
            tasks.user_issue_activities_id,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit aktivitas issue", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal edit issue", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def edit_issue_activities_nofile(tasks: issueActivitiesEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE issue_activities SET activity=%s, date_activity=%s, issue_id=%s, user_issue_activities_id=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.activity,
            tasks.date_activity,
            tasks.issue_id,
            tasks.user_issue_activities_id,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit aktivitas issue", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal edit aktivitas issue", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def delete_issue_activity(tasks: issueActivitiesEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            DELETE FROM issue_activities where id=%s returning id;
        """
        cursor.execute(sql_command, (
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil delete issue", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"berhasil delete issue", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def getAllissuesActivity(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command="""
        select ia.activity, ia.date_activity , ia.photo, t.name as issue, u.name as user
        from issue_activities ia
        left join users u on u.id = ia.user_task_activities_id
        left join issues t on t.id = ia.task_id
        where ta.issue_id = %s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data aktivitas issue","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data aktivitas issue","result":""}
        return response
    
    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"berhasil delete issue", "data": e}

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
