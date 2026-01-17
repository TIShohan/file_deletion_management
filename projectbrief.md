# Project Brief: File Deletion Management Tool

## Objective
Convert the prototype file management script into a professional, modern Windows application. The goal is to provide a seamless user experience from installation to daily use, helping users identify and clean up large files and duplicates effortlessly.

## User Flow
1. **Installation**: User runs a setup file that installs the application.
2. **Launch**: User opens the app via a desktop or start menu shortcut (standalone `.exe`).
3. **Configuration**: User selects the directory path they wish to scan through a modern folder picker.
4. **Operation**: User reviews scan results, applies filters, and performs "Dry Runs" or deletions as needed.

## Core Features
1. **Interactive File Scanning**:
   - Dynamic path selection (User chooses which drive or folder to scan).
   - Deep scan with multi-threaded performance.
   - Real-time progress tracking.
2. **Disk Analytics**:
   - Display top largest folders within the selected path.
   - Total scanned file count and total storage size.
3. **Advanced Filtering**:
   - Search by filename or extension.
   - Filter by minimum file size (MB).
   - Filter by file age (e.g., older than 30, 90, 365 days).
   - Filter by specific file extensions.
4. **Duplicate Detection**:
   - MD5 hash-based duplicate finding.
5. **Secure Management**:
   - "Select All" and manual selection for deletion.
   - Dry Run mode to preview actions.
   - Safe deletion using the Windows Recycle Bin.
   - Multi-step confirmation for actual deletion.

## Technical Goals & Requirements
- **GUI Framework**: **CustomTkinter** for a robust, high-performance, and modern Windows-native user interface.
- **Scanning Engine**: Optimized with **Tiered Hashing** (Size check -> Quick Hash -> Full Hash) for maximum speed.
- **Data Persistence**: **SQLite** backend for efficient handling of large datasets (scanning millions of files without RAM bloat).
- **Concurrency**: Multi-threaded architecture to keep the UI responsive during deep scans.
- **Packaging**: Standalone `.exe` via PyInstaller, bundled with a professional **Inno Setup** installer.
- **Aesthetics**: Modern "Dark Mode" design with custom-styled widgets and smooth interactions.

## Target Audience
Users looking for a simple yet powerful tool to manage local storage, find duplicates, and clean up junk files.
