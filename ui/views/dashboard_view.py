import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Welcome Banner
        self.banner = ctk.CTkFrame(self, fg_color=("#3B8ED0", "#1f538d"), corner_radius=15, height=130)
        self.banner.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 20))
        self.banner.grid_propagate(False)
        self.banner.grid_columnconfigure(0, weight=1)
        self.banner.grid_rowconfigure(0, weight=1)
        
        self.welcome_label = ctk.CTkLabel(self.banner, text="System Health & Cleanup Overview", font=ctk.CTkFont(size=26, weight="bold"), text_color="white")
        self.welcome_label.grid(row=0, column=0, padx=20, pady=20)

        # Stats Grid
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="ew", padx=20)
        
        self.stat_vars = {}
        self.stat_cards = {}
        
        self.create_stat_card("Total Files", "0", 0, "total_files", "#2ecc71")
        self.create_stat_card("Total Analyzed", "0 MB", 1, "total_size", "#e67e22")
        self.create_stat_card("Duplicates", "0", 2, "duplicates", "#e74c3c")

        # Start Scan Shortcut
        self.scan_shortcut_btn = ctk.CTkButton(
            self, 
            text="🚀 START NEW SCAN", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#3B8ED0",
            hover_color="#1f538d",
            command=lambda: master.master.show_scanner() # Navigate to scanner
        )
        self.scan_shortcut_btn.grid(row=2, column=0, pady=(20, 0), padx=30)

        # Top Folders Section
        self.folders_frame = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color="gray30")
        self.folders_frame.grid(row=3, column=0, sticky="nsew", padx=30, pady=(20, 30))
        self.folders_frame.grid_columnconfigure(0, weight=1)

        self.folder_title = ctk.CTkLabel(self.folders_frame, text="📁 TOXIC FOLDERS (Largest Space Consumers)", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray60")
        self.folder_title.pack(anchor="w", padx=25, pady=(20, 10))
        
        self.folder_list_container = ctk.CTkFrame(self.folders_frame, fg_color="transparent")
        self.folder_list_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
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

        # Refresh Folder List
        for widget in self.folder_list_container.winfo_children():
            widget.destroy()
            
        top_folders = self.db.get_top_folders(5)
        if not top_folders:
            ctk.CTkLabel(self.folder_list_container, text="No scan data available yet.", text_color="gray50").pack(pady=20)
        
        for folder, size_mb in top_folders:
            item = ctk.CTkFrame(self.folder_list_container, fg_color=("gray95", "gray25"), corner_radius=8)
            item.pack(fill="x", pady=4)
            
            name_lbl = ctk.CTkLabel(item, text=folder, font=ctk.CTkFont(size=12), anchor="w")
            name_lbl.pack(side="left", padx=15, pady=8, fill="x", expand=True)
            
            size_lbl = ctk.CTkLabel(item, text=f"{size_mb/1024:.2f} GB" if size_mb > 1024 else f"{size_mb:.2f} MB", 
                                    font=ctk.CTkFont(size=12, weight="bold"), text_color="#3B8ED0")
            size_lbl.pack(side="right", padx=15)
