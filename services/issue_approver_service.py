
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
import hashlib



from models.issue_approver import issueApproverCreate,issueApproverEdit

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


def create_new_issue_approver(tasks: issueApproverCreate, filename: str):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            INSERT INTO issue_approver ( issue_id, user_id, urutan, created_at)
            VALUES (%s, %s, %s, now())
            RETURNING id;
        """
        cursor.execute(sql_command, (
            tasks.issue_id,
            tasks.user_id,
            tasks.urutan
            ))

        new_id = cursor.fetchone()  # get RETURNING result
        connection.commit()  # commit transaction

        response={"status": "ok", "message":"berhasil tambah issue", "data": new_id}

        return response

        # return {"status": "ok", "message": "berhasil tambah issue", "data": tasks, "filename": filename}

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

def sign_issue_approver(tasks: issueApproverEdit):

    connection = None
    cursor = None

    data = f"{tasks.issue_id}:{tasks.user_id}:{tasks.id}".encode()
    hashed = hashlib.sha256(data).hexdigest()

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            UPDATE issue_approver SET signature=%s where id=%s returning id;
        """
        cursor.execute(sql_command, (
            hashed,
            tasks.id,
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

def delete_issue_approver(tasks: issueApproverEdit):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = """
            DELETE FROM issue_approver where id=%s returning id;
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
        response={"status": "nok", "message":"gagal delete issue", "data": e}

        return response

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

def getAllissueApprover(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command="""
        select t.name as task, u.name  as user, ta.signature
        from issue_approver ta
        left join users u on u.id = ta.user_id
        left join tasks t on t.id = ta.task_id
        where ta.task_id = %s
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
        response={"status": "nok", "message":"gagal delete issue", "data": e}

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
