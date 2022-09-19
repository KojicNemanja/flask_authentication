from hashlib import sha256
from flaskr.models.user import User
from flaskr.db.db import get_db

class DBUser:

    @staticmethod
    def save(user: User):
        conn = get_db()
        hash_password = sha256(user.password.encode('utf-8')).hexdigest()
        query = "INSERT INTO `user` VALUES ('%s', '%s')"%(user.username, hash_password)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def get_for_username(username: str) -> User:
        conn = get_db()
        query = "SELECT * FROM `user` WHERE `username`='%s'"%(username)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        if data is not None:
            return User(data[0], data[1])
        return None
    
    def test() -> float:
        pass