import os
import hashlib
from datetime import datetime
from pathlib import Path

class FileScanner:
    def __init__(self, root_path, skip_extensions=None):
        self.root_path = root_path
        self.skip_extensions = skip_extensions or {'.sys', '.dll', '.exe', '.ini', '.dat'}

    def scan(self, progress_callback=None):
        """
        Walks through the directory and yields file metadata.
        """
        files_found = []
        count = 0
        
        for root, dirs, filenames in os.walk(self.root_path):
            # Skip hidden directories if needed (optional)
            for f in filenames:
                try:
                    path = os.path.normpath(os.path.join(root, f))
                    ext = Path(f).suffix.lower()
                    
                    if ext in self.skip_extensions:
                        continue
                        
                    stats = os.stat(path)
                    size = stats.st_size
                    mtime = stats.st_mtime
                    mod_date = datetime.fromtimestamp(mtime)
                    age_days = (datetime.now() - mod_date).days
                    
                    file_info = (
                        f,
                        path,
                        root,
                        ext,
                        size,
                        round(size / (1024 * 1024), 2),
                        mod_date.strftime("%Y-%m-%d %H:%M"),
                        age_days
                    )
                    files_found.append(file_info)
                    count += 1
                    
                    if count % 100 == 0 and progress_callback:
                        progress_callback(count, f"Last scanned: {f}")
                        
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
