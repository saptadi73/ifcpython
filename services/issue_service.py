
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

from models.issue import issueCreate,issueEdit

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


def create_new_issue(tasks: issueCreate, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            INSERT INTO issues (name, globalid, expressid, description, status, user_issued_id, user_assign_id, project_id, location, photo, date_issued, closed_date, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
            RETURNING id;
        """
        cursor.execute(sql_command, (
            tasks.name,
            tasks.globalid,
            tasks.expressid,
            tasks.description,
            tasks.status,
            tasks.user_issued_id,
            tasks.user_assign_id,
            tasks.project_id,
            tasks.location,
            filename,
            tasks.date_issued,
            tasks.closed_date
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil tambah issue", "data": new_id}

        return response

        # return {"status": "ok", "message": "berhasil tambah task", "data": tasks, "filename": filename}

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal tambah issue", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def edit_issue(tasks: issueEdit, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE issues SET name=%s,  globalid=%s, expressid=%s, description=%s, status=%s, user_issued_id=%s, user_assign_id=%s, project_id=%s, location=%s, url_photo=%s, date_issued=%s, closed_date=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.name,
            tasks.globalid,
            tasks.expressid,
            tasks.description,
            tasks.status,
            tasks.user_issued_id,
            tasks.user_assign_id,
            tasks.project_id,
            tasks.location,
            filename,
            tasks.date_issued,
            tasks.closed_date,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit issue", "data": new_id}

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

def edit_issue_nofile(tasks: issueEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE issues SET name=%s,  globalid=%s, expressid=%s, description=%s, status=%s, user_issued_id=%s, user_assign_id=%s, project_id=%s, location=%s, date_issued=%s, closed_date=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            tasks.name,
            tasks.globalid,
            tasks.expressid,
            tasks.description,
            tasks.status,
            tasks.user_issued_id,
            tasks.user_assign_id,
            tasks.project_id,
            tasks.location,
            tasks.date_issued,
            tasks.closed_date,
            tasks.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit issue", "data": new_id}

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

def delete_issue(tasks: issueEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            DELETE FROM issues where id=%s returning id;
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

def getAllIssueDone(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command="""
        select i.project_id, i.name, i.id,i.globalid, i.expressid, i.location, i.description, i.photo, i.date_issued, i.closed_date, u.name as user_assign_to, u2.name as user_issued_by
        from issues i
        left join users u on u.id = i.user_assign_id
        left join users u2 on u2.id = i.user_issued_id
        where i.status ='done' and i.project_id = %s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data issue selesai","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data issue selesai","result":""}
        return response
    
    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal data issue selesai", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def getAllIssue(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql_command="""
        select i.project_id, i.status, i.name, i.id,i.globalid, i.expressid, i.location, i.description, i.photo, i.date_issued, i.closed_date, u.name as user_assign_to, u2.name as user_issued_by
        from issues i
        left join users u on u.id = i.user_assign_id
        left join users u2 on u2.id = i.user_issued_id
        where i.project_id = %s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data issue","result":record};
        else:
            response = {"status":"nok","message":"gagal dapat data issue","result":""}
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
