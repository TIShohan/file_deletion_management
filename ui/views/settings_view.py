import customtkinter as ctk

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, db=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db

        self.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Extensions to skip
        self.skip_frame = ctk.CTkFrame(self)
        self.skip_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.skip_lbl = ctk.CTkLabel(self.skip_frame, text="Skip Extensions (comma separated):")
        self.skip_lbl.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.skip_entry = ctk.CTkEntry(self.skip_frame)
        current_skip = self.db.get_setting("skip_extensions", ".sys,.dll,.exe,.ini,.dat")
        self.skip_entry.insert(0, current_skip)
        self.skip_entry.pack(fill="x", padx=20, pady=(5, 20))

        # Save Button
        self.save_btn = ctk.CTkButton(self, text="Save Settings", fg_color="blue", command=self.save_settings)
        self.save_btn.grid(row=2, column=0, padx=20, pady=20, sticky="e")

    def save_settings(self):
        val = self.skip_entry.get()
        self.db.set_setting("skip_extensions", val)
        from tkinter import messagebox
        messagebox.showinfo("Success", "Settings saved successfully!")
