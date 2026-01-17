import sqlite3
import os
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path="file_data.db"):
        self.db_path = db_path
        self._initialize_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _initialize_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Table for scanned files
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    path TEXT UNIQUE,
                    folder TEXT,
                    extension TEXT,
                    size_bytes INTEGER,
                    size_mb REAL,
                    modified_at TEXT,
                    age_days INTEGER,
                    hash_quick TEXT,
                    hash_full TEXT,
                    is_duplicate INTEGER DEFAULT 0
                )
            ''')
            
            # Index for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_size ON files(size_bytes)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash_quick ON files(hash_quick)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash_full ON files(hash_full)')
            
            conn.commit()

    def clear_database(self):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM files")
            conn.commit()

    def insert_files(self, files_data):
        """Batch insert files data into the database"""
        query = '''
            INSERT OR REPLACE INTO files 
            (filename, path, folder, extension, size_bytes, size_mb, modified_at, age_days)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        with self.get_connection() as conn:
            conn.executemany(query, files_data)
            conn.commit()

    def update_hash(self, path, hash_val, quick=True):
        column = "hash_quick" if quick else "hash_full"
        with self.get_connection() as conn:
            conn.execute(f"UPDATE files SET {column} = ? WHERE path = ?", (hash_val, path))
            conn.commit()

    def mark_duplicates(self):
        """Identifies duplicates based on full hash and marks them"""
        with self.get_connection() as conn:
            # First reset
            conn.execute("UPDATE files SET is_duplicate = 0")
            # Mark all as duplicates if their full hash appears more than once
            conn.execute('''
                UPDATE files SET is_duplicate = 1 
                WHERE hash_full IN (
                    SELECT hash_full FROM files 
                    WHERE hash_full IS NOT NULL 
                    GROUP BY hash_full 
                    HAVING COUNT(*) > 1
                )
            ''')
            conn.commit()
