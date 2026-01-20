# Project Brief: CleanSweep (File Deletion Management)

## Objective
Convert a prototype file management script into a premium, modern Windows application. The goal is to help users identify and clean up large files and duplicates with 100% safety and a beautiful user interface.

## User Flow
1. **Launch**: Open the app via standalone `.exe`.
2. **Dashboard**: View system stats, total analyzed space, and the **Storage Composition** chart.
3. **Deep Scan**: Select a directory and perform a tiered hash scan.
4. **Review**: Search, filter, and group identical files.
5. **Action**: "Dry Run" to simulate savings or "Move to Recycle Bin" for safe cleanup.

## Core Features
1. **Interactive Scanner**:
   - Multi-threaded performance with real-time progress.
   - **Course-Safe Duplication**: Advanced grouping (Content + Name + Folder) to prevent accidental deletion of identical files in different modules.
2. **Disk Analytics**:
   - **Storage Composition** dashboard to see which file types (Videos, Images, etc) consume the most space.
   - Total analyzed metric (MB/GB/Files).
3. **Advanced Filtering**:
   - Instant search by filename, size threshold, and file age.
4. **Secure Management**:
   - "Select All" / Deselect logic.
   - "Dry Run" simulator.
   - Safe deletion using Windows Recycle Bin (`send2trash`).

## Technical Goals & Requirements
- **GUI Framework**: **CustomTkinter** for a professional Windows-native look.
- **Scanning Engine**: **Tiered Hashing** (Size -> Quick Hash -> Full MD5).
- **Data Persistence**: **SQLite** backend for light-speed querying of millions of files.
- **Packaging**: Standalone `.exe` via PyInstaller + Inno Setup.

## Target Audience
Windows users needing a powerful yet safe tool to reclaim disk space from large files and redundant content.
