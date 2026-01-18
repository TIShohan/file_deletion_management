import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Welcome Banner with a modern look
        self.banner = ctk.CTkFrame(self, fg_color=("#3B8ED0", "#1f538d"), corner_radius=15, height=150)
        self.banner.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 20))
        self.banner.grid_propagate(False)
        self.banner.grid_columnconfigure(0, weight=1)
        self.banner.grid_rowconfigure(0, weight=1)
        
        self.welcome_label = ctk.CTkLabel(
            self.banner, 
            text="System Health & Cleanup Overview", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        self.welcome_label.grid(row=0, column=0, padx=20, pady=20)

        # Stats Grid
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        
        self.stat_vars = {}
        self.stat_cards = {}
        
        self.create_stat_card("Total Files Managed", "0", 0, "total_files", "#2ecc71")
        self.create_stat_card("Storage Occupied", "0 MB", 1, "total_size", "#e67e22")
        self.create_stat_card("Redundant Duplicates", "0", 2, "duplicates", "#e74c3c")
        
        self.refresh_stats()

    def create_stat_card(self, title, default_value, col_idx, key, accent_color):
        card = ctk.CTkFrame(self.stats_frame, corner_radius=12, border_width=2, border_color="gray25")
        card.grid(row=0, column=col_idx, sticky="nsew", padx=10, pady=10)
        self.stat_cards[key] = card
        
        # Accent indicator
        accent = ctk.CTkFrame(card, width=5, fg_color=accent_color, corner_radius=0)
        accent.pack(side="left", fill="y")

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        title_lbl = ctk.CTkLabel(content, text=title.upper(), font=ctk.CTkFont(size=12, weight="bold"), text_color="gray60")
        title_lbl.pack(anchor="w")
        
        self.stat_vars[key] = ctk.StringVar(value=default_value)
        value_lbl = ctk.CTkLabel(content, textvariable=self.stat_vars[key], font=ctk.CTkFont(size=32, weight="bold"))
        value_lbl.pack(anchor="w", pady=(5, 0))
        
        # Hover effect bindings
        card.bind("<Enter>", lambda e: self._on_hover(key, True))
        card.bind("<Leave>", lambda e: self._on_hover(key, False))

        self.stats_frame.grid_columnconfigure(col_idx, weight=1)

    def _on_hover(self, key, is_entering):
        if is_entering:
            self.stat_cards[key].configure(border_color="#3B8ED0", fg_color=("gray85", "gray30"))
        else:
            self.stat_cards[key].configure(border_color="gray25", fg_color=("gray90", "gray20"))

    def refresh_stats(self):
        if not self.db:
            return
            
        stats = self.db.get_dashboard_stats()
        self.stat_vars["total_files"].set(f"{stats['total_files']:,}")
        
        size = stats['total_size_mb']
        if size > 1024:
            self.stat_vars["total_size"].set(f"{size/1024:.2f} GB")
        else:
            self.stat_vars["total_size"].set(f"{size:.2f} MB")
            
        self.stat_vars["duplicates"].set(f"{stats['duplicates_count']:,}")
