# This file handles all direct database operations (raw SQL queries).

from . import get_db

class User:
    @staticmethod
    def create(email, password, name):
        db = get_db()
        cursor = db.cursor()
        query = """
            INSERT INTO users (email, password, name)
            VALUES (%s, %s, %s)
            RETURNING id, email, name, created_at
        """
        cursor.execute(query, (email, password, name))
        user = cursor.fetchone()
        db.commit()
        cursor.close()
        return {'id': user[0], 'email': user[1], 'name': user[2], 'created_at': user[3]} if user else None

    @staticmethod
    def find_by_email(email):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        return {'id': user[0], 'email': user[1], 'password': user[2], 'name': user[3]} if user else None

    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT id, email, name, created_at FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return {'id': user[0], 'email': user[1], 'name': user[2]} if user else None

class Task:
    @staticmethod
    def create(user_id, title, description):
        db = get_db()
        cursor = db.cursor()
        query = """
            INSERT INTO tasks (user_id, title, description)
            VALUES (%s, %s, %s)
            RETURNING id, user_id, title, description, completed, created_at, updated_at
        """
        cursor.execute(query, (user_id, title, description))
        task = cursor.fetchone()
        db.commit()
        cursor.close()
        # Convert row to dictionary
        return {'id': task[0], 'user_id': task[1], 'title': task[2], 'description': task[3], 'completed': task[4], 'created_at': task[5], 'updated_at': task[6]} if task else None

    @staticmethod
    def find_by_user_id(user_id):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC"
        cursor.execute(query, (user_id,))
        tasks = cursor.fetchall()
        cursor.close()
        # Convert list of tuples to list of dictionaries
        return [{'id': row[0], 'user_id': row[1], 'title': row[2], 'description': row[3], 'completed': row[4], 'created_at': row[5], 'updated_at': row[6]} for row in tasks]

    @staticmethod
    def update(task_id, title, description, completed):
        db = get_db()
        cursor = db.cursor()
        query = """
            UPDATE tasks 
            SET title = %s, description = %s, completed = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, user_id, title, description, completed, created_at, updated_at
        """
        cursor.execute(query, (title, description, completed, task_id))
        task = cursor.fetchone()
        db.commit()
        cursor.close()
        return {'id': task[0], 'user_id': task[1], 'title': task[2], 'description': task[3], 'completed': task[4], 'created_at': task[5], 'updated_at': task[6]} if task else None

    @staticmethod
    def delete(task_id):
        db = get_db()
        cursor = db.cursor()
        query = "DELETE FROM tasks WHERE id = %s RETURNING id"
        cursor.execute(query, (task_id,))
        task = cursor.fetchone()
        db.commit()
        cursor.close()
        return task is not None

    @staticmethod
    def toggle_complete(task_id):
        db = get_db()
        cursor = db.cursor()
        query = """
            UPDATE tasks 
            SET completed = NOT completed, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, user_id, title, description, completed, created_at, updated_at
        """
        cursor.execute(query, (task_id,))
        task = cursor.fetchone()
        db.commit()
        cursor.close()
        return {'id': task[0], 'user_id': task[1], 'title': task[2], 'description': task[3], 'completed': task[4], 'created_at': task[5], 'updated_at': task[6]} if task else None
