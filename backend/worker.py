import threading
from .scanner import FileScanner
from .database import DatabaseManager

class ScanWorker(threading.Thread):
    def __init__(self, root_path, db_manager: DatabaseManager, skip_extensions=None, progress_callback=None, completion_callback=None):
        super().__init__()
        self.root_path = root_path
        self.db = db_manager
        self.skip_extensions = skip_extensions
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self.stop_event = threading.Event()

    def run(self):
        try:
            self._update_progress(0, "Initializing scan...")
            scanner = FileScanner(self.root_path, skip_extensions=self.skip_extensions)
            
            # 1. Scanning
            self._update_progress(0, "Scanning files...")
            files = scanner.scan(progress_callback=self._update_progress)
            
            if self.stop_event.is_set(): return

            # 2. Database Insertion
            self._update_progress(len(files), "Saving to database...")
            self.db.clear_database()
            self.db.insert_files(files)

            # 3. Quick Hashing for potential duplicates (Tiered Hashing)
            self._process_hashes(scanner)

            if self.completion_callback:
                self.completion_callback("Scan complete!")
                
        except Exception as e:
            if self.completion_callback:
                self.completion_callback(f"Error: {str(e)}")

    def _update_progress(self, count, message):
        if self.progress_callback:
            self.progress_callback(count, message)

    def _process_hashes(self, scanner):
        """Tiered Hashing Implementation"""
        with self.db.get_connection() as conn:
            # Only hash files that share the exact same size
            query = """
                SELECT path FROM files 
                WHERE size_bytes IN (
                    SELECT size_bytes FROM files GROUP BY size_bytes HAVING COUNT(*) > 1
                )
            """
            paths_to_hash = [row['path'] for row in conn.execute(query).fetchall()]

        total_to_hash = len(paths_to_hash)
        for i, path in enumerate(paths_to_hash):
            if self.stop_event.is_set(): break
            
            # Step A: Quick Hash
            q_hash = scanner.get_quick_hash(path)
            if q_hash:
                self.db.update_hash(path, q_hash, quick=True)
            
            if i % 10 == 0:
                self._update_progress(i, f"Quick hashing duplicates ({i}/{total_to_hash})...")

        # Step B: Full Hash only if Quick Hashes match
        with self.db.get_connection() as conn:
            query = """
                SELECT path FROM files 
                WHERE hash_quick IN (
                    SELECT hash_quick FROM files WHERE hash_quick IS NOT NULL GROUP BY hash_quick HAVING COUNT(*) > 1
                )
            """
            paths_for_full_hash = [row['path'] for row in conn.execute(query).fetchall()]

        total_full = len(paths_for_full_hash)
        for i, path in enumerate(paths_for_full_hash):
            if self.stop_event.is_set(): break
            
            f_hash = scanner.get_full_hash(path)
            if f_hash:
                self.db.update_hash(path, f_hash, quick=False)
            
            if i % 10 == 0:
                self._update_progress(i, f"Full hashing confirmed matches ({i}/{total_full})...")

        # Mark duplicates in DB
        self.db.mark_duplicates()

    def stop(self):
        self.stop_event.set()
