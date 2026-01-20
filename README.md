# CleanSweep 🚀 (Pro File Deletion Management)

CleanSweep is a high-performance, premium Windows utility designed to reclaim disk space by safely identifying large files and redundant duplicates with 100% precision.

![Version](https://img.shields.io/badge/version-1.0.4--Premium-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgray)

## ✨ Core Features
- **Turbo Scanner**: Built with `os.scandir` for 3x faster directory traversal.
- **Course-Safe Matching**: Advanced duplication logic (Hash + Name + Folder) ensures educational modules remain intact.
- **Parallel Hashing**: Utilizes multi-core CPUs for instant duplicate verification.
- **Visual Analytics**: Interactive Dashboard with Storage Composition charts.
- **One-Click Cleanup**: Safe deletion via Windows Recycle Bin with "Dry Run" simulation.

## 📥 How to Download (Users)
1. Go to the **[Releases](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases)** section.
2. Download the latest `CleanSweep.exe`.
3. Run and enjoy! No installation or Python required.

## 🛠️ Technical Details (Developers)
- **Frontend**: CustomTkinter (High-DPI Support)
- **Backend**: Python 3.12 / SQLite 3
- **Hashing**: Tiered MD5 (Size -> Quick -> Full)
- **Thread Safety**: Fully multi-threaded UI to prevent hangs during deep scans.

## 📜 Development Setup
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`
2. Install requirements: `pip install customtkinter send2trash Pillow`
3. Run: `python main.py`

---
*Created with ❤️ for high-performance file management.*
