import os
import hashlib
from datetime import datetime
from pathlib import Path

class FileScanner:
    def __init__(self, root_path, skip_extensions=None, skip_directories=None):
        self.root_path = root_path
        self.skip_extensions = skip_extensions or {'.sys', '.dll', '.exe', '.ini', '.dat'}
        self.skip_directories = skip_directories or []

    def scan(self, progress_callback=None, stop_event=None):
        """
        Fast scanning using os.scandir with cancellation support.
        """
        files_found = []
        count = 0
        
        stack = [self.root_path]
        
        while stack:
            # Check if user requested cancellation
            if stop_event and stop_event.is_set():
                return files_found
                
            current_dir = stack.pop()
            try:
                with os.scandir(current_dir) as entries:
                    for entry in entries:
                        try:
                            if entry.is_dir(follow_symlinks=False):
                                # Skip system-protected directories (SaaS standard)
                                if any(entry.path.startswith(safe) for safe in self.skip_directories):
                                    continue
                                stack.append(entry.path)
                            elif entry.is_file(follow_symlinks=False):
                                path = os.path.normpath(entry.path)
                                ext = os.path.splitext(entry.name)[1].lower()
                                
                                if ext in self.skip_extensions:
                                    continue
                                    
                                stats = entry.stat()
                                size = stats.st_size
                                mtime = stats.st_mtime
                                mod_date = datetime.fromtimestamp(mtime)
                                age_days = (datetime.now() - mod_date).days
                                
                                file_info = (
                                    entry.name,
                                    path,
                                    current_dir,
                                    ext,
                                    size,
                                    round(size / (1024 * 1024), 2),
                                    mod_date.strftime("%Y-%m-%d %H:%M"),
                                    age_days
                                )
                                files_found.append(file_info)
                                count += 1
                                
                                if count % 100 == 0 and progress_callback:
                                    progress_callback(count, f"Scanned: {entry.name}")
                        except (PermissionError, OSError):
                            continue
            except (PermissionError, OSError):
                continue
                
        return files_found

    @staticmethod
    def get_quick_hash(path):
        """Generates MD5 hash for the first 64KB of a file."""
        try:
            hasher = hashlib.md5()
            with open(path, 'rb') as f:
                hasher.update(f.read(65536))
            return hasher.hexdigest()
        except Exception:
            return None

    @staticmethod
    def get_full_hash(path):
        """Generates MD5 hash for the entire file content."""
        try:
            hasher = hashlib.md5()
            with open(path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None
