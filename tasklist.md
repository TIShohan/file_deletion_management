# Tasklist: File Deletion Management Software

This tasklist outlines the steps to convert the prototype script into a professional, modern Windows desktop application.

## Phase 1: Environment & Project Setup
- [x] Initialize Python virtual environment.
- [x] Install core dependencies (`flet`, `send2trash`, `pyinstaller`, `pandas`).
- [x] Set up project structure:
    - [x] `/backend`: Scanner, Database, and Logic.
    - [x] `/ui`: Flet views and components.
    - [x] `/assets`: Icons and branding.

## Phase 2: High-Performance Backend & Database
- [x] **SQLite Integration**: Build a database schema to store file paths, sizes, and hashes.
- [x] **Tiered Scanner Logic**:
    - [x] Directory walking with error handling.
    - [x] Size-based grouping (to avoid hashing unique files).
    - [x] Quick-hashing (64KB) for potential duplicates.
    - [x] Full-hashing for confirmed duplicates.
- [x] **Multi-threading**: Implement a `Worker` class to run the scanner in the background.

## Phase 3: Flet GUI Development
- [x] **Design System**: Set up Flet theme (colors, fonts, radii).
- [x] **Navigation Shell**: sidebar-based layout with "Dashboard", "Scanner", and "Trash" views.
- [x] **Landing Page**: Modern "Select Path" start screen.
- [x] **Real-time Dashboard**: Live progress bars and file-counting animations.
- [x] **High-Performance Data Table**: Build a Flet `DataTable` (or custom ListView) to display results from SQLite.
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
- [ ] Create a custom application icon (.ico).
- [ ] Configure PyInstaller spec file for a "One-File" executable (includes Python runtime).
- [ ] **Installer Creation**: Set up Inno Setup or a similar tool to create a user-friendly `.exe` installer.
- [ ] Test the installation and execution on a machine without Python installed.
