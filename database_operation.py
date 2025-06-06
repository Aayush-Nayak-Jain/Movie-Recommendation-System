import sqlite3
import hashlib
import os

class MovieRecommendationDB:
    def __init__(self, db_name='movie_recommendation.db'):
        self.db_name = db_name
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize database with minimal tables"""
        with sqlite3.connect(self.db_name) as conn:
            # User table with just username and password
            conn.execute('''
            CREATE TABLE IF NOT EXISTS User (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
            ''')
            
            # SearchHistory table with ONLY username and searched_movie
            conn.execute('''
            CREATE TABLE IF NOT EXISTS SearchHistory (
                username TEXT NOT NULL,
                searched_movie TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES User(username)
            )
            ''')

    # User CRUD Operations
    def create_user(self, username, password):
        """Add new user with hashed password"""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                "INSERT INTO User VALUES (?, ?)",
                (username, self._hash_password(password))
            )
    
    def get_user(self, username):
        """Retrieve user by username"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE username=?", (username,))
            return cursor.fetchone()
    
    def delete_user(self, username):
        """Remove user and their search history"""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("DELETE FROM SearchHistory WHERE username=?", (username,))
            conn.execute("DELETE FROM User WHERE username=?", (username,))

    # Search History Operations (Simplified)
    def log_search(self, username, movie):
        """Record a movie search (just username and movie)"""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                "INSERT INTO SearchHistory VALUES (?, ?)",
                (username, movie)
            )
    
    def get_search_history(self, username):
        """Get all searches for a user"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT searched_movie FROM SearchHistory WHERE username=?",
                (username,)
            )
            return [row[0] for row in cursor.fetchall()]

    # Password Hashing
    def _hash_password(self, password):
        """Secure password hashing with salt"""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt, 
            100000
        )
        return salt + key
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        user = self.get_user(username)
        if not user:
            return False
            
        stored_password = user[1]
        salt = stored_password[:32]
        stored_key = stored_password[32:]
        
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return new_key == stored_key


# Example Usage
if __name__ == "__main__":
    db = MovieRecommendationDB()
    
    # User operations
    db.create_user("test_user", "password123")
    print("User created:", db.get_user("test_user")[0])
    
    # Search history operations
    db.log_search("test_user", "The Dark Knight")
    db.log_search("test_user", "Inception")
    print("Search history:", db.get_search_history("test_user"))
    
    # Verification
    print("Login valid:", db.verify_user("test_user", "password123"))
    
    # Cleanup
    db.delete_user("test_user")