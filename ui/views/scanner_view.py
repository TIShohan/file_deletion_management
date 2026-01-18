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
        self.sort_column = "size_bytes"
        self.sort_desc = True

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 
        self.grid_rowconfigure(5, weight=0) 

        # --- Header Section ---
        self.header_label = ctk.CTkLabel(self, text="Deep File Scanner", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, sticky="w", padx=30, pady=(20, 10))

        # --- Top Section: Path & Actions ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        
        self.path_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Select directory to scan...", height=40)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(10, 10))
        
        self.browse_btn = ctk.CTkButton(self.top_frame, text="Browse Folder", width=120, height=40, command=self.browse_path)
        self.browse_btn.pack(side="left", padx=5)

        self.scan_btn = ctk.CTkButton(self.top_frame, text="Start Deep Scan", fg_color="#2ecc71", hover_color="#27ae60", width=140, height=40, font=ctk.CTkFont(weight="bold"), command=self.start_scan)
        self.scan_btn.pack(side="left", padx=5)

        # --- Middle Section: Filters ---
        self.filter_container = ctk.CTkFrame(self)
        self.filter_container.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(self.filter_container, placeholder_text="🔍 Search mapping name...", width=200)
        self.search_entry.pack(side="left", padx=15, pady=15)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_results())

        self.min_size_entry = ctk.CTkEntry(self.filter_container, placeholder_text="Min MB", width=80)
        self.min_size_entry.pack(side="left", padx=5, pady=15)
        self.min_size_entry.bind("<KeyRelease>", lambda e: self.load_results())

        self.min_age_entry = ctk.CTkEntry(self.filter_container, placeholder_text="Min Days", width=80)
        self.min_age_entry.pack(side="left", padx=5, pady=15)
        self.min_age_entry.bind("<KeyRelease>", lambda e: self.load_results())

        self.dup_mode_var = ctk.StringVar(value="Content")
        self.dup_mode_seg = ctk.CTkSegmentedButton(self.filter_container, values=["Content", "Name"], 
                                                     variable=self.dup_mode_var, command=self.change_duplicate_mode)
        self.dup_mode_seg.pack(side="right", padx=15, pady=15)

        self.duplicate_var = ctk.BooleanVar(value=False)
        self.duplicate_switch = ctk.CTkSwitch(self.filter_container, text="Duplicates Only", variable=self.duplicate_var, command=self.load_results)
        self.duplicate_switch.pack(side="right", padx=15, pady=15)

        # --- Results Section: Treeview ---
        self.setup_treeview()

        # --- Bottom Section: Management & Status ---
        self.status_bar = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.status_bar.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))

        self.select_all_btn = ctk.CTkButton(self.status_bar, text="Select All", width=100, fg_color="gray30", command=self.select_all)
        self.select_all_btn.pack(side="left", padx=(10, 5))
        
        self.deselect_all_btn = ctk.CTkButton(self.status_bar, text="Deselect", width=100, fg_color="gray30", command=self.deselect_all)
        self.deselect_all_btn.pack(side="left", padx=5)

        self.dry_run_btn = ctk.CTkButton(self.status_bar, text="Dry Run", fg_color="#e67e22", hover_color="#d35400", width=120, command=self.dry_run_selected)
        self.dry_run_btn.pack(side="left", padx=20)

        self.delete_btn = ctk.CTkButton(self.status_bar, text="Move to Recycle Bin", fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(weight="bold"), command=self.delete_selected)
        self.delete_btn.pack(side="right", padx=10)

        self.progress_bar = ctk.CTkProgressBar(self, height=10)
        self.progress_bar.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self, text="Ready to scan", font=ctk.CTkFont(size=12, slant="italic"))
        self.status_label.grid(row=7, column=0, sticky="e", padx=30, pady=(0, 10))

    def setup_treeview(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", 
                             background="#1d1e1e", 
                             foreground="#dce4ee", 
                             fieldbackground="#1d1e1e",
                             rowheight=35,
                             borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#1f538d')])
        
        self.style.configure("Treeview.Heading",
                             background="#2b2b2b",
                             foreground="white",
                             relief="flat",
                             padding=5)
        self.style.map("Treeview.Heading",
                       background=[('active', '#3484F0')])

        self.tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tree_frame.grid(row=3, column=0, sticky="nsew", padx=20)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.tree_frame, columns=("path", "size", "type", "is_dup"), show="headings", selectmode="extended")
        
        # Define Headings and click to sort
        self.tree.heading("path", text="FILE PATH", command=lambda: self.set_sort("path"))
        self.tree.heading("size", text="SIZE ↓", command=lambda: self.set_sort("size_bytes"))
        self.tree.heading("type", text="TYPE", command=lambda: self.set_sort("extension"))
        self.tree.heading("is_dup", text="DUPLICATE", command=lambda: self.set_sort("is_duplicate"))
        
        self.tree.column("path", width=600, minwidth=200)
        self.tree.column("size", width=120, anchor="e", minwidth=100)
        self.tree.column("type", width=100, anchor="center", minwidth=80)
        self.tree.column("is_dup", width=120, anchor="center", minwidth=100)

        self.tree.tag_configure("duplicate", background="#3d1414", foreground="#ffaaaa")

        # Scrollbars logic
        v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid Tree & Scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

    def set_sort(self, column):
        if self.sort_column == column:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_column = column
            self.sort_desc = True
        
        # Update heading visual
        for col in ["path", "size", "type", "is_dup"]:
            text = self.tree.heading(col)["text"].replace(" ↓", "").replace(" ↑", "")
            if col == column or (col == "size" and column == "size_bytes") or (col == "type" and column == "extension") or (col == "is_dup" and column == "is_duplicate"):
                text += " ↓" if self.sort_desc else " ↑"
            self.tree.heading(col, text=text)
            
        self.load_results()

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

        confirm = messagebox.askyesno("Confirm Deletion", f"Confirm moving {len(selected_items)} files to Recycle Bin?\nThis operation is safer but permanent if deleted from Bin.")
        if not confirm:
            return

        self._perform_deletion(selected_items)

    def dry_run_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Dry Run", "Select files to simulate deletion.")
            return

        total_size_bytes = 0
        for item in selected_items:
            size_str = self.tree.item(item, 'values')[1]
            try:
                size_mb = float(size_str.split(' ')[0])
                total_size_bytes += size_mb * 1024 * 1024
            except:
                pass

        total_mb = total_size_bytes / (1024 * 1024)
        messagebox.showinfo("Dry Run Summary", 
                            f"Simulation Results:\n\n"
                            f"• Files: {len(selected_items)}\n"
                            f"• Potential Savings: {total_mb:.2f} MB\n\n"
                            f"Status: Safe (No files deleted)")

    def _perform_deletion(self, selected_items):
        deleted_count = 0
        errors = []

        for item in selected_items:
            file_path = self.tree.item(item, 'values')[0]
            try:
                file_path = os.path.normpath(file_path)
                if os.path.exists(file_path):
                    send2trash(file_path)
                    self.tree.delete(item)
                    deleted_count += 1
                else:
                    errors.append(f"Not found: {file_path}")
            except Exception as e:
                errors.append(f"Error: {e}")

        self.status_label.configure(text=f"Last action: Deleted {deleted_count} files.")
        if errors:
            messagebox.showerror("Errors Occurred", "\n".join(errors[:3]))

    def start_scan(self):
        root_path = self.path_entry.get()
        if not root_path:
            messagebox.showwarning("Path Missing", "Please select a folder to scan.")
            return

        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self.status_label.configure(text="Scanning file system...")
        
        # Clear results
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Start Worker
        skip_ext_str = self.db.get_setting("skip_extensions", ".sys,.dll,.exe,.ini,.dat")
        skip_ext_list = [ext.strip().lower() for ext in skip_ext_str.split(',') if ext.strip()]

        self.worker = ScanWorker(
            root_path, 
            self.db, 
            skip_extensions=set(skip_ext_list), 
            progress_callback=self.on_progress, 
            completion_callback=self.on_complete
        )
        self.worker.start()

    def on_progress(self, count, message):
        self.after(0, lambda: self.status_label.configure(text=f"{message} ({count} files)"))

    def on_complete(self, message):
        self.after(0, lambda: self._scan_finished(message))

    def _scan_finished(self, message):
        self.scan_btn.configure(state="normal", text="Start Deep Scan")
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)
        self.status_label.configure(text=message)
        self.load_results()

    def change_duplicate_mode(self, mode):
        if self.db:
            self.db.mark_duplicates(mode=mode.lower())
        self.load_results()

    def load_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        name_filter = f"%{self.search_entry.get()}%"
        try:
            min_size = float(self.min_size_entry.get()) if self.min_size_entry.get() else 0
        except ValueError: min_size = 0
        try:
            min_age = int(self.min_age_entry.get()) if self.min_age_entry.get() else 0
        except ValueError: min_age = 0

        try:
            with self.db.get_connection() as conn:
                params = [name_filter, min_size, min_age]
                dup_clause = "AND is_duplicate = 1" if self.duplicate_var.get() else ""
                
                order_dir = "DESC" if self.sort_desc else "ASC"
                query = f"""
                    SELECT path, size_bytes, is_duplicate, extension FROM files 
                    WHERE filename LIKE ? 
                    AND size_mb >= ? 
                    AND age_days >= ?
                    {dup_clause}
                    ORDER BY {self.sort_column} {order_dir} 
                    LIMIT 200
                """
                rows = conn.execute(query, params).fetchall()
                
            for row in rows:
                size_mb = f"{row['size_bytes'] / (1024*1024):.2f} MB"
                ext = row['extension'].upper() if row['extension'] else "FILE"
                is_dup = "MATCH" if row['is_duplicate'] else "-"
                tag = ("duplicate",) if row['is_duplicate'] else ()
                self.tree.insert("", "end", values=(row['path'], size_mb, ext, is_dup), tags=tag)
                
            self.status_label.configure(text=f"Loaded {len(rows)} matching items.")
        except Exception as e:
            print(f"Filter Error: {e}")
