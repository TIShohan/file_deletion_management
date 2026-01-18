import customtkinter as ctk
from tkinter import messagebox

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, db=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db

        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_label = ctk.CTkLabel(self, text="Application Settings", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, sticky="w", padx=30, pady=(30, 20))
        
        # Extensions to skip Card
        self.card = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color="gray30")
        self.card.grid(row=1, column=0, sticky="ew", padx=30, pady=10)
        
        self.info_lbl = ctk.CTkLabel(self.card, text="Excluded File Types", font=ctk.CTkFont(size=16, weight="bold"))
        self.info_lbl.pack(anchor="w", padx=25, pady=(20, 5))
        
        self.desc_lbl = ctk.CTkLabel(self.card, text="Files with these extensions will be ignored during the scan process.", font=ctk.CTkFont(size=12), text_color="gray60")
        self.desc_lbl.pack(anchor="w", padx=25, pady=(0, 15))
        
        self.skip_entry = ctk.CTkEntry(self.card, height=45, placeholder_text=".exe, .dll, .sys")
        current_skip = self.db.get_setting("skip_extensions", ".sys,.dll,.exe,.ini,.dat")
        self.skip_entry.insert(0, current_skip)
        self.skip_entry.pack(fill="x", padx=25, pady=(0, 25))

        # Action Bar
        self.action_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.action_bar.grid(row=2, column=0, sticky="ew", padx=30, pady=20)
        
        self.save_btn = ctk.CTkButton(
            self.action_bar, 
            text="Save Preferences", 
            fg_color="#3B8ED0", 
            hover_color="#1f538d",
            height=40,
            width=160,
            font=ctk.CTkFont(weight="bold"),
            command=self.save_settings
        )
        self.save_btn.pack(side="right")

    def save_settings(self):
        val = self.skip_entry.get()
        self.db.set_setting("skip_extensions", val)
        messagebox.showinfo("Settings Updated", "Your preferences have been successfully saved.")
