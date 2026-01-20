import customtkinter as ctk
from tkinter import messagebox

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Welcome Banner
        self.banner = ctk.CTkFrame(self, fg_color=("#3B8ED0", "#1f538d"), corner_radius=15, height=130)
        self.banner.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 20))
        self.banner.grid_propagate(False)
        self.banner.grid_columnconfigure(0, weight=1)
        self.banner.grid_rowconfigure(0, weight=1)
        
        self.welcome_label = ctk.CTkLabel(self.banner, text="CleanSweep Analytics Dashboard", font=ctk.CTkFont(size=26, weight="bold"), text_color="white")
        self.welcome_label.grid(row=0, column=0, padx=20, pady=20)

        # Stats Grid
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="ew", padx=20)
        
        self.stat_vars = {}
        self.stat_cards = {}
        
        self.create_stat_card("Analyzed Files", "0", 0, "total_files", "#2ecc71")
        self.create_stat_card("Total Scan Size", "0 MB", 1, "total_size", "#e67e22")
        self.create_stat_card("Duplicate Items", "0", 2, "duplicates", "#e74c3c")

        # Action buttons frame
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0), padx=30)
        self.actions_frame.grid_columnconfigure((0, 1), weight=1)

        # Start Scan Shortcut
        self.scan_shortcut_btn = ctk.CTkButton(
            self.actions_frame, 
            text="🚀 START NEW SCAN", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            width=200,
            fg_color="#3B8ED0",
            hover_color="#1f538d",
            command=lambda: master.master.show_scanner() 
        )
        self.scan_shortcut_btn.grid(row=0, column=0, padx=10)

        # Clear Metrics Button
        self.clear_metrics_btn = ctk.CTkButton(
            self.actions_frame,
            text="🧹 CLEAR ALL METRICS",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            width=200,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.clear_metrics_action
        )
        self.clear_metrics_btn.grid(row=0, column=1, padx=10)

        # Visual Analytics Section (Professional Standards)
        self.analytics_frame = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color="gray30")
        self.analytics_frame.grid(row=3, column=0, sticky="nsew", padx=30, pady=(20, 30))
        self.analytics_frame.grid_columnconfigure(0, weight=1)

        self.chart_title = ctk.CTkLabel(self.analytics_frame, text="📊 STORAGE COMPOSITION (By File Type)", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray60")
        self.chart_title.pack(anchor="w", padx=25, pady=(20, 10))
        
        self.chart_container = ctk.CTkFrame(self.analytics_frame, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        self.refresh_stats()

    def create_stat_card(self, title, default_value, col_idx, key, accent_color):
        card = ctk.CTkFrame(self.stats_frame, corner_radius=12, border_width=2, border_color="gray25")
        card.grid(row=0, column=col_idx, sticky="nsew", padx=10, pady=10)
        self.stat_cards[key] = card
        accent = ctk.CTkFrame(card, width=5, fg_color=accent_color, corner_radius=0)
        accent.pack(side="left", fill="y")
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        title_lbl = ctk.CTkLabel(content, text=title.upper(), font=ctk.CTkFont(size=11, weight="bold"), text_color="gray60")
        title_lbl.pack(anchor="w")
        self.stat_vars[key] = ctk.StringVar(value=default_value)
        value_lbl = ctk.CTkLabel(content, textvariable=self.stat_vars[key], font=ctk.CTkFont(size=28, weight="bold"))
        value_lbl.pack(anchor="w", pady=(2, 0))
        self.stats_frame.grid_columnconfigure(col_idx, weight=1)

    def refresh_stats(self):
        if not self.db: return
        stats = self.db.get_dashboard_stats()
        self.stat_vars["total_files"].set(f"{stats['total_files']:,}")
        size = stats['total_size_mb']
        self.stat_vars["total_size"].set(f"{size/1024:.2f} GB" if size > 1024 else f"{size:.2f} MB")
        self.stat_vars["duplicates"].set(f"{stats['duplicates_count']:,}")

        # Refresh Visual Analytics (Simple bar indicators for type distribution)
        for widget in self.chart_container.winfo_children():
            widget.destroy()
            
        type_distribution = self._get_type_distribution()
        if not type_distribution:
            ctk.CTkLabel(self.chart_container, text="No scan data available for analysis.", text_color="gray50").pack(pady=40)
            return

        total_size = sum(size for _, size in type_distribution)
        for ext, size_mb in type_distribution:
            percentage = (size_mb / total_size) if total_size > 0 else 0
            
            row = ctk.CTkFrame(self.chart_container, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            label_box = ctk.CTkFrame(row, fg_color="transparent", width=120)
            label_box.pack(side="left", padx=(0, 10))
            label_box.pack_propagate(False)
            
            ctk.CTkLabel(label_box, text=ext.upper() or "OTHER", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
            
            progress = ctk.CTkProgressBar(row, height=12, fg_color="gray20", progress_color="#3B8ED0")
            progress.pack(side="left", fill="x", expand=True, padx=10)
            progress.set(percentage)
            
            ctk.CTkLabel(row, text=f"{percentage*100:.1f}%", font=ctk.CTkFont(size=11), width=50).pack(side="right")

    def _get_type_distribution(self):
        """Fetches storage distribution by file extension"""
        with self.db.get_connection() as conn:
            query = """
                SELECT extension, SUM(size_mb) as total_size 
                FROM files 
                GROUP BY extension 
                ORDER BY total_size DESC 
                LIMIT 6
            """
            return conn.execute(query).fetchall()

    def clear_metrics_action(self):
        """Resets the dashboard by clearing the database"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to clear all scanned metrics?"):
            self.db.clear_database()
            self.refresh_stats()
            messagebox.showinfo("Success", "Dashboard metrics cleared.")
