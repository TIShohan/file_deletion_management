import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import tkinter
import threading
import os
from send2trash import send2trash
from backend.worker import ScanWorker

class ScannerView(ctk.CTkFrame):
    def __init__(self, master, db=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db
        self.worker = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        # 1. Control Bar (Path Selection)
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        self.path_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Select directory to scan...")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=15)
        
        self.browse_btn = ctk.CTkButton(self.control_frame, text="Browse Folder", width=120, command=self.browse_path)
        self.browse_btn.pack(side="left", padx=(0, 20), pady=15)

        # 2. Action Bar (Scan, Dry Run)
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.scan_btn = ctk.CTkButton(self.action_frame, text="Start Deep Scan", fg_color="green", hover_color="darkgreen", command=self.start_scan)
        self.scan_btn.pack(side="left")
        
        self.progress_bar = ctk.CTkProgressBar(self.action_frame)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=20)
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self.action_frame, text="Ready to scan")
        self.status_label.pack(side="right")

        # 3. Results Table (Treeview)
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", 
                             background="#2b2b2b", 
                             foreground="white", 
                             fieldbackground="#2b2b2b",
                             borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#1f538d')])
        
        self.style.configure("Treeview.Heading",
                             background="#565b5e",
                             foreground="white",
                             relief="flat")
        self.style.map("Treeview.Heading",
                       background=[('active', '#3484F0')])

        self.tree = ttk.Treeview(self, columns=("path", "size", "type"), show="headings", selectmode="extended")
        self.tree.heading("path", text="File Path")
        self.tree.heading("size", text="Size")
        self.tree.heading("type", text="Type")
        
        self.tree.column("path", width=500)
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("type", width=80, anchor="c")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))
        scrollbar.grid(row=2, column=1, sticky="ns", pady=(0, 10))

        # 4. Management Bar (Delete, Select All)
        self.mgmt_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mgmt_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        self.select_all_btn = ctk.CTkButton(self.mgmt_frame, text="Select All", width=100, command=self.select_all)
        self.select_all_btn.pack(side="left", padx=(0, 10))
        
        self.deselect_all_btn = ctk.CTkButton(self.mgmt_frame, text="Deselect", width=100, command=self.deselect_all)
        self.deselect_all_btn.pack(side="left")

        self.delete_btn = ctk.CTkButton(self.mgmt_frame, text="Delete Selected (Recycle Bin)", fg_color="red", hover_color="darkred", command=self.delete_selected)
        self.delete_btn.pack(side="right")

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def select_all(self):
        for item in self.tree.get_children():
            self.tree.selection_add(item)

    def deselect_all(self):
        for item in self.tree.get_children():
            self.tree.selection_remove(item)

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select files to delete first.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to move {len(selected_items)} files to the Recycle Bin?")
        if not confirm:
            return

        deleted_count = 0
        errors = []

        for item in selected_items:
            file_path = self.tree.item(item, 'values')[0]
            try:
                # Normalize path for Windows (converts / to \ and handles long paths)
                file_path = os.path.normpath(file_path)
                
                if os.path.exists(file_path):
                    send2trash(file_path)
                    self.tree.delete(item)
                    deleted_count += 1
                else:
                    errors.append(f"File not found: {file_path}")
            except Exception as e:
                errors.append(f"Error deleting {file_path}: {e}")

        self.status_label.configure(text=f"Deleted {deleted_count} files.")
        if errors:
            messagebox.showerror("Errors Occurred", "\n".join(errors[:5]) + ("\n..." if len(errors) > 5 else ""))

    def start_scan(self):
        root_path = self.path_entry.get()
        if not root_path:
            self.status_label.configure(text="Please select a path first!", text_color="orange")
            return

        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.progress_bar.set(0)
        self.status_label.configure(text="Initializing...", text_color="white")
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Start Worker
        self.worker = ScanWorker(
            root_path, 
            self.db, 
            skip_extensions=[".sys", ".dll", ".exe", ".ini", ".dat"], # Todo: Load from settings
            progress_callback=self.on_progress, 
            completion_callback=self.on_complete
        )
        self.worker.start()

    def on_progress(self, count, message):
        # Schedule UI update on main thread
        self.after(0, lambda: self._update_progress_ui(count, message))

    def _update_progress_ui(self, count, message):
        self.status_label.configure(text=message)
        # Indeterminate progress or based on estimation
        if "Scanning" in message:
             self.progress_bar.configure(mode="indeterminate")
             self.progress_bar.start()
        else:
             self.progress_bar.configure(mode="determinate")
             self.progress_bar.stop()
             self.progress_bar.set(1.0) # Just fill it for processing steps

    def on_complete(self, message):
        self.after(0, lambda: self._scan_finished(message))

    def _scan_finished(self, message):
        self.scan_btn.configure(state="normal", text="Start Deep Scan")
        self.progress_bar.stop()
        self.progress_bar.set(1)
        self.status_label.configure(text=message)
        
        if "Error" not in message:
            self.load_results()

    def load_results(self):
        # Fetch files from DB
        try:
            with self.db.get_connection() as conn:
                # Get Top 100 largest files for now
                rows = conn.execute("SELECT path, size_bytes FROM files ORDER BY size_bytes DESC LIMIT 100").fetchall()
                
            for row in rows:
                size_mb = f"{row['size_bytes'] / (1024*1024):.2f} MB"
                ext = os.path.splitext(row['path'])[1] if '.' in row['path'] else "File"
                self.tree.insert("", "end", values=(row['path'], size_mb, ext))
                
            self.status_label.configure(text=f"Scan Complete. Loaded {len(rows)} largest files.")
        except Exception as e:
            self.status_label.configure(text=f"Error loading results: {e}", text_color="red")
