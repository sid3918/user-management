import pymysql

from database import get_connection

COLUMNS = (
    "user_id, first_name, last_name, email, phone, gender, "
    "date_of_birth, department, designation, status, created_at, updated_at"
)       


class DuplicateEmailError(Exception):
    """Raised when the email already exists (MySQL error 1062)."""
    

def _fetch_user(cur, user_id):
    """Run a SELECT for one user using an already-open cursor."""
    cur.execute(f"SELECT {COLUMNS} FROM users WHERE user_id = %s", (user_id,))
    return cur.fetchone()
    

def create_user(data: dict) -> dict:
    
    
    conn = get_connection()     
    try:
        with conn.cursor() as cur:      
            cur.execute(
                """
                INSERT INTO users
                    (first_name, last_name, email, phone, gender,
                    date_of_birth, department, designation, status)
                VALUES
                    (%(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(gender)s,
                    %(date_of_birth)s, %(department)s, %(designation)s, %(status)s)
                """,
                data,
            )       
            new_id = cur.lastrowid     
        conn.commit()  
        with conn.cursor() as cur:
            return _fetch_user(cur, new_id)     
    except pymysql.err.IntegrityError as e:     
        conn.rollback()
        if e.args[0] == 1062:   
            raise DuplicateEmailError("Email already exists") from e
        raise
    except Exception:   
        conn.rollback()
        raise
    finally:
        conn.close()    


def get_all_users(search: str | None = None) -> list:       
    conn = get_connection()
    try:
        sql = f"SELECT {COLUMNS} FROM users"
        params = []
        if search:
            sql += " WHERE CONCAT(first_name, ' ', last_name) LIKE %s OR email LIKE %s"
            like = f"%{search}%"
            params = [like, like]
        sql += " ORDER BY user_id DESC"
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def get_user(user_id: int) -> dict | None:      
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            return _fetch_user(cur, user_id)    
    finally:
        conn.close()


def update_user(user_id: int, data: dict) -> dict | None:   
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if _fetch_user(cur, user_id) is None:
                return None
            cur.execute(
                """
                UPDATE users SET
                    first_name = %(first_name)s, last_name = %(last_name)s,
                    email = %(email)s, phone = %(phone)s, gender = %(gender)s,
                    date_of_birth = %(date_of_birth)s, department = %(department)s,
                    designation = %(designation)s, status = %(status)s
                WHERE user_id = %(user_id)s
                """,
                {**data, "user_id": user_id},  
            )       
        conn.commit()
        with conn.cursor() as cur:
            return _fetch_user(cur, user_id)
    except pymysql.err.IntegrityError as e:
        conn.rollback()
        if e.args[0] == 1062:
            raise DuplicateEmailError("Email already exists") from e
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_user(user_id: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            deleted = cur.rowcount == 1
        conn.commit()
        return deleted
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()