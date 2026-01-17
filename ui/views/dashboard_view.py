import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        # Welcome Banner
        self.banner = ctk.CTkFrame(self, fg_color=("gray85", "gray25"))
        self.banner.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        self.welcome_label = ctk.CTkLabel(
            self.banner, 
            text="Welcome to File Deletion Manager", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.welcome_label.pack(padx=20, pady=20)

        # Stats Grid
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        
        # Placeholder Stats
        self.create_stat_card("Total Scanned", "0 Files", 0)
        self.create_stat_card("Space Reclaimed", "0 MB", 1)
        self.create_stat_card("Duplicates Found", "0", 2)

    def create_stat_card(self, title, value, col_idx):
        card = ctk.CTkFrame(self.stats_frame)
        card.grid(row=0, column=col_idx, sticky="ew", padx=(0 if col_idx==0 else 10, 0))
        
        title_lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="normal"))
        title_lbl.pack(pady=(15, 5), padx=20)
        
        value_lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=20, weight="bold"))
        value_lbl.pack(pady=(0, 15), padx=20)
        
        self.stats_frame.grid_columnconfigure(col_idx, weight=1)
