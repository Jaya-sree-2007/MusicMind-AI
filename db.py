import mysql.connector
from mysql.connector import Error

# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Jaya@2007",
    "database": "musicmind_ai"
}

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)

        if conn.is_connected():
            return conn

    except Error as e:
        print("Database Connection Error:", e)
        return None

# -----------------------------
# EXECUTE SELECT QUERY
# -----------------------------
def fetch_query(query, values=None):

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

# -----------------------------
# EXECUTE INSERT / UPDATE / DELETE
# -----------------------------
def execute_query(query, values=None):

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        conn.commit()

        return True

    except Error as e:

        print("Query Error:", e)
        return False

    finally:

        cursor.close()
        conn.close()

# -----------------------------
# CHECK USER EXISTS
# -----------------------------
def user_exists(username, email):

    query = """
    SELECT * FROM users
    WHERE username=%s OR email=%s
    """

    result = fetch_query(query, (username, email))

    return len(result) > 0

# -----------------------------
# GET USER BY USERNAME
# -----------------------------
def get_user(username):

    query = """
    SELECT * FROM users
    WHERE username=%s
    """

    result = fetch_query(query, (username,))

    if result:
        return result[0]

    return None

# -----------------------------
# SAVE ANALYSIS RESULT
# -----------------------------
def save_result(username, personality, genre, score):

    query = """
    INSERT INTO results
    (username, personality, genre, score)
    VALUES (%s,%s,%s,%s)
    """

    return execute_query(
        query,
        (username, personality, genre, score)
    )

# -----------------------------
# GET USER HISTORY
# -----------------------------
def get_user_history(username):

    query = """
    SELECT *
    FROM results
    WHERE username=%s
    ORDER BY created_at DESC
    """

    return fetch_query(query, (username,))

# -----------------------------
# TOTAL USERS
# -----------------------------
def get_total_users():

    query = """
    SELECT COUNT(*) AS total
    FROM users
    """

    result = fetch_query(query)

    return result[0]["total"]

# -----------------------------
# TOTAL ANALYSES
# -----------------------------
def get_total_analyses():

    query = """
    SELECT COUNT(*) AS total
    FROM results
    """

    result = fetch_query(query)

    return result[0]["total"]

# -----------------------------
# MOST POPULAR PERSONALITY
# -----------------------------
def get_popular_personality():

    query = """
    SELECT personality,
           COUNT(*) AS count
    FROM results
    GROUP BY personality
    ORDER BY count DESC
    LIMIT 1
    """

    result = fetch_query(query)

    if result:
        return result[0]["personality"]

    return "No Data"

# -----------------------------
# SAVE OTP
# -----------------------------
def save_otp(username, otp):

    query = """
    INSERT INTO password_resets
    (username, otp)
    VALUES (%s,%s)
    """

    return execute_query(
        query,
        (username, otp)
    )

# -----------------------------
# VERIFY OTP
# -----------------------------
def verify_otp(username, otp):

    query = """
    SELECT *
    FROM password_resets
    WHERE username=%s
    AND otp=%s
    ORDER BY created_at DESC
    LIMIT 1
    """

    result = fetch_query(
        query,
        (username, otp)
    )

    return len(result) > 0