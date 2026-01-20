# System Patterns: CleanSweep Architecture

## Core Architecture
CleanSweep follows a decoupled **Frontend/Backend** architecture to ensure UI responsiveness and modular maintainability.

### 1. View-Controller Pattern (UI)
- **`app.py`**: The central orchestrator that manages navigation and view switching.
- **`ui/views/`**: Modularized frames (Dashboard, Scanner, Settings). Each view is independent and communicates with the Backend via the `DatabaseManager`.
- **CustomTkinter**: Used for modern Windows-native aesthetics and high-DPI scaling support.

### 2. Multi-Threaded Execution (Background)
- **`ScanWorker`**: Inherits from `threading.Thread`. It handles the intensive IO and CPU tasks (scanning, hashing, DB writes) to prevent the main UI thread from hanging/freezing.
- **Event-Driven Stopping**: Uses `threading.Event` (`stop_event`) to check for user cancellation signals during every major loop (scanning and hashing).

## Performance Patterns

### 1. Iterative Traversal (Stack-Based)
Instead of recursive `os.walk`, we use an iterative stack with `os.scandir`.
- **Reason**: `os.scandir` is 2-3x faster on Windows.
- **Robustness**: Prevents `RecursionError` on extremely deep directory trees.

### 2. Tiered Duplicate Detection
To eliminate 99% of non-duplicates without reading file content:
1. **Dimension Filter**: Compare file sizes first (via `os.stat`).
2. **Quick Hash**: Generate MD5 of the first 64KB for size-matched candidates.
3. **Full Proof**: Only perform full MD5 if Quick Hashes match.
4. **Parallelism**: Uses `ThreadPoolExecutor` for the hashing phases to leverage multi-core CPUs.

### 3. Data Persistence (SQLite)
- **Flat-File Indexed DB**: Stores file paths, metadata, and hashes.
- **Efficient Grouping**: Uses SQL `GROUP BY` and `HAVING COUNT(*) > 1` for near-instant duplicate identification even with 100k+ records.

## Safety & Security Patterns

### 1. Course-Safe Logic
Specialized duplication rule tailored for educational content:
- Files are only marked as duplicates if they share: **[Full Content Hash] + [Filename] + [Parent Folder Name]**.
- **Result**: Identical files in different modules (e.g., Module 1 vs Module 2) are preserved.

### 2. Industry Standard Exclusions
- **System Safe-List**: Hardcoded exclusion of `C:\Windows`, `C:\Program Files`, etc.
- **Safe-Delete**: Uses `send2trash` to move items to the Windows Recycle Bin instead of permanent deletion.
- **Dry Run**: Simulation mode to calculate potential savings before any disk modification occurs.
