import sqlite3
from datetime import datetime


DB_NAME = "files.db"



def get_connection():

    conn = sqlite3.connect(DB_NAME)

    return conn



def init_db():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS files
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            size INTEGER,
            upload_time TEXT
        )
        """
    )


    conn.commit()

    conn.close()



def add_file(
    filename,
    size
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO files
        (
            filename,
            size,
            upload_time
        )
        VALUES
        (?, ?, ?)
        """,
        (
            filename,
            size,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )


    conn.commit()

    conn.close()



def get_files():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
        filename,
        size,
        upload_time
        FROM files
        """
    )


    rows = cursor.fetchall()


    conn.close()


    result=[]


    for row in rows:

        result.append(
            {
                "filename": row[0],
                "size": row[1],
                "upload_time": row[2]
            }
        )


    return result


def delete_file_record(filename):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM files
        WHERE filename = ?
        """,
        (
            filename,
        )
    )


    conn.commit()

    conn.close()