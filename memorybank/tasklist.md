# Tasklist: File Deletion Management Software

This tasklist outlines the steps to convert the prototype script into a professional, modern Windows desktop application.

## Phase 1: Environment & Project Setup
- [x] Initialize Python virtual environment.
- [x] Install core dependencies (`customtkinter`, `send2trash`, `pyinstaller`, `pandas`).
- [x] Set up project structure:
    - [x] `/backend`: Scanner, Database, and Logic.
    - [x] `/ui`: CustomTkinter views and components.
    - [x] `/assets`: Icons and branding.

## Phase 2: High-Performance Backend & Database
- [x] **SQLite Integration**: Build a database schema to store file paths, sizes, and hashes.
- [x] **Tiered Scanner Logic**:
    - [x] Directory walking with error handling.
    - [x] Size-based grouping (to avoid hashing unique files).
    - [x] Quick-hashing (64KB) for potential duplicates.
    - [x] Full-hashing for confirmed duplicates.
- [x] **Multi-threading**: Implement a `Worker` class to run the scanner in the background.

## Phase 3: CustomTkinter GUI Development
- [x] **Design System**: Set up CustomTkinter theme (colors, fonts).
- [x] **Navigation Shell**: sidebar-based layout with "Dashboard", "Scanner", and "Trash" views.
- [x] **Landing Page**: Modern "Select Path" start screen.
- [x] **Real-time Dashboard**: Live progress bars and file-counting animations.
- [x] **High-Performance Data Table**: Build a styled `ttk.Treeview` to display results from SQLite.
- [x] **Interactive Filters**: Dynamic UI filters that query SQLite (instant search).

## Phase 4: Feature Implementation
- [x] **Integration**: Connect backend signals to UI progress bars and labels.
- [x] **Dry Run**: Implement the preview mechanism to show what *would* happen.
- [x] **Secure Deletion**: Hook up `send2trash` for safe recycle bin operations.
- [x] **Confirmation Flow**: Design and implement a "Danger Zone" confirmation dialog.

## Phase 5: Polishing & UX
- [x] Add smooth transitions between app views.
- [x] Implement hover effects and button micro-animations.
- [x] Ensure full responsiveness and High-DPI support for Windows.
- [x] Add a settings panel for global "Skip Extensions".

## Phase 6: Packaging & Deployment
- [x] Create a custom application icon (.ico).
- [x] Configure PyInstaller spec file for a "One-File" executable (includes Python runtime).
- [x] **Installer Creation**: Set up Inno Setup or a similar tool to create a user-friendly `.exe` installer.
- [x] Build standalone executable via PyInstaller.

## Phase 7: Final Development & Refinement (Completed)
- [x] **7.1 Dashboard Stats**: Connect database queries to display real metrics (Total Scanned, Space, Duplicates).
- [x] **7.2 Advanced Filtering**: Add UI inputs for Name search, Min Size (MB), and File Age (Days) in Scanner View.
- [x] **7.3 Duplicate Management**: Implement highlighting and a "Show Duplicates Only" filter in the results table.
- [x] **7.4 Dry Run Mode**: Implement a safe preview mode to calculate potential results without actual deletion.
- [x] **7.5 Settings Persistence**: Ensure "Skip Extensions" and other preferences are saved/loaded correctly.
