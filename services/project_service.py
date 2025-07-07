
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

from models.project import projectCreate,projectEdit

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

def get_all_project():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = "SELECT * FROM projects p;"  # ganti sesuai query kamu
        cursor.execute(sql_command)
        results = cursor.fetchall()
        response={"status": "ok", "message":"berhasil dapat data project", "data": results}

        return response

    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        response={"status": "nok", "message":"gagal dapat project", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

def create_new_project(projects: projectCreate):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            INSERT INTO projects (name, description, value, start_date, end_date, created_at)
            VALUES (%s, %s, %s, %s, %s, now())
            RETURNING id;
        """
        cursor.execute(sql_command, (
            projects.name,
            projects.description,
            projects.value,
            projects.start_date,
            projects.end_date
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil tambah project", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal edit project", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def edit_project(projects: projectEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE projects SET name=%s,  description=%s, value=%s, start_date=%s, end_date=%s, updated_at=now() where id=%s returning id; 
        """
        cursor.execute(sql_command, (
            projects.name,
            projects.description,
            projects.value,
            projects.start_date,
            projects.end_date,
            projects.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil edit project", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"gagal edit project", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def delete_project(projects: projectEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            DELETE FROM projects where id=%s returning id;
        """
        cursor.execute(sql_command, (
            projects.id
        ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil delete project", "data": new_id}

        return response

    except psycopg2.Error as e:
        if connection:
            connection.rollback()  # rollback on error
        response={"status": "nok", "message":"berhasil delete project", "data": e}

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
