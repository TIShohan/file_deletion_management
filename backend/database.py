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
            
            # Table for settings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            # Default settings
            cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('skip_extensions', '.sys,.dll,.exe,.ini,.dat')")
            
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

    def mark_duplicates(self, mode="content"):
        """Identifies duplicates based on mode: 'content' (MD5) or 'name' (Filename)"""
        with self.get_connection() as conn:
            # First reset
            conn.execute("UPDATE files SET is_duplicate = 0")
            
            if mode == "content":
                # Mark duplicates based on full hash
                conn.execute('''
                    UPDATE files SET is_duplicate = 1 
                    WHERE hash_full IN (
                        SELECT hash_full FROM files 
                        WHERE hash_full IS NOT NULL 
                        GROUP BY hash_full 
                        HAVING COUNT(*) > 1
                    )
                ''')
            else:
                # Mark duplicates based on filename
                conn.execute('''
                    UPDATE files SET is_duplicate = 1 
                    WHERE filename IN (
                        SELECT filename FROM files 
                        GROUP BY filename 
                        HAVING COUNT(*) > 1
                    )
                ''')
            conn.commit()

    def get_dashboard_stats(self):
        """Returns a dictionary with summary statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total files and size
            result = cursor.execute("SELECT COUNT(*), SUM(size_mb) FROM files").fetchone()
            total_files = result[0] or 0
            total_size_mb = result[1] or 0
            
            # Duplicates
            duplicates_count = cursor.execute("SELECT COUNT(*) FROM files WHERE is_duplicate = 1").fetchone()[0] or 0
            
            return {
                "total_files": total_files,
                "total_size_mb": total_size_mb,
                "duplicates_count": duplicates_count
            }

    def get_setting(self, key, default=None):
        with self.get_connection() as conn:
            res = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            return res['value'] if res else default

    def set_setting(self, key, value):
         with self.get_connection() as conn:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
            conn.commit()
