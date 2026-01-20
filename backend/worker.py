import threading
from .scanner import FileScanner
from .database import DatabaseManager

class ScanWorker(threading.Thread):
    def __init__(self, root_path, db_manager: DatabaseManager, skip_extensions=None, skip_directories=None, progress_callback=None, completion_callback=None):
        super().__init__()
        self.root_path = root_path
        self.db = db_manager
        self.skip_extensions = skip_extensions
        self.skip_directories = skip_directories
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self.stop_event = threading.Event()

    def run(self):
        try:
            self._update_progress(0, "Initializing scan...")
            scanner = FileScanner(self.root_path, skip_extensions=self.skip_extensions, skip_directories=self.skip_directories)
            
            # 1. Scanning
            self._update_progress(0, "Scanning files...")
            files = scanner.scan(progress_callback=self._update_progress, stop_event=self.stop_event)
            
            if self.stop_event.is_set(): 
                if self.completion_callback:
                    self.completion_callback("Scan cancelled.")
                return

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
        """Ultra-Fast Parallel Hashing Implementation"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        with self.db.get_connection() as conn:
            # PHASE A: Candidate selection (Strict Triple Check)
            query = """
                SELECT path FROM files 
                WHERE (filename, folder, size_bytes) IN (
                    SELECT filename, folder, size_bytes FROM files GROUP BY filename, folder, size_bytes HAVING COUNT(*) > 1
                )
            """
            paths_to_hash = [row['path'] for row in conn.execute(query).fetchall()]

        total_to_hash = len(paths_to_hash)
        if total_to_hash == 0:
            self.db.mark_duplicates()
            return

        # Parallel Quick Hashing
        self._update_progress(0, f"Quick hashing {total_to_hash} candidates...")
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = {executor.submit(scanner.get_quick_hash, p): p for p in paths_to_hash}
            try:
                for i, future in enumerate(as_completed(futures)):
                    if self.stop_event.is_set():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    
                    path = futures[future]
                    q_hash = future.result()
                    if q_hash:
                        self.db.update_hash(path, q_hash, quick=True)
                    if i % 20 == 0:
                        self._update_progress(i, f"Analyzing candidates ({i}/{total_to_hash})...")
            except Exception:
                executor.shutdown(wait=False, cancel_futures=True)
                raise

        if self.stop_event.is_set(): return

        # PHASE B: Full Hash only if Quick Hashes match
        with self.db.get_connection() as conn:
            query = """
                SELECT path FROM files 
                WHERE hash_quick IN (
                    SELECT hash_quick FROM files WHERE hash_quick IS NOT NULL GROUP BY hash_quick HAVING COUNT(*) > 1
                )
            """
            paths_for_full_hash = [row['path'] for row in conn.execute(query).fetchall()]

        total_full = len(paths_for_full_hash)
        if total_full > 0:
            self._update_progress(0, f"Deep analysis of {total_full} files...")
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = {executor.submit(scanner.get_full_hash, p): p for p in paths_for_full_hash}
                try:
                    for i, future in enumerate(as_completed(futures)):
                        if self.stop_event.is_set():
                            executor.shutdown(wait=False, cancel_futures=True)
                            break
                            
                        path = futures[future]
                        f_hash = future.result()
                        if f_hash:
                            self.db.update_hash(path, f_hash, quick=False)
                        if i % 5 == 0:
                            self._update_progress(i, f"Verifying identical items ({i}/{total_full})...")
                except Exception:
                    executor.shutdown(wait=False, cancel_futures=True)
                    raise

        if self.stop_event.is_set(): return

        # Final Grouping
        self._update_progress(total_to_hash, "Finalizing duplicate groups...")
        self.db.mark_duplicates()

    def stop(self):
        self.stop_event.set()
