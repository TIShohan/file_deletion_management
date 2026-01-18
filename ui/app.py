import customtkinter as ctk
import os
from .views.dashboard_view import DashboardView
from .views.scanner_view import ScannerView
from .views.settings_view import SettingsView
from backend.database import DatabaseManager

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # System Settings
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Database
        self.db = DatabaseManager()

        # Window Setup
        self.title("File Deletion Management Tool")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # Grid Layout 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Navigation)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CleanSweep", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.sidebar_btn_dashboard.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_btn_scanner = ctk.CTkButton(self.sidebar_frame, text="Scanner", command=self.show_scanner)
        self.sidebar_btn_scanner.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_btn_settings = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings)
        self.sidebar_btn_settings.grid(row=3, column=0, padx=20, pady=10)
        
        # Appearance Mode
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Content Area - Views
        self.active_view = None
        
        # Initialize Views
        self.dashboard_view = DashboardView(self, db=self.db, corner_radius=0, fg_color="transparent")
        self.scanner_view = ScannerView(self, db=self.db, corner_radius=0, fg_color="transparent")
        self.settings_view = SettingsView(self, db=self.db, corner_radius=0, fg_color="transparent")
        
        # Start with dashboard
        self.select_frame_by_name("Dashboard")

    def show_dashboard(self):
        self.dashboard_view.refresh_stats()
        self.select_frame_by_name("Dashboard")

    def show_scanner(self):
        self.select_frame_by_name("Scanner")

    def show_settings(self):
        self.select_frame_by_name("Settings")

    def select_frame_by_name(self, name):
        # Update buttons state
        self.sidebar_btn_dashboard.configure(fg_color=("gray75", "gray25") if name == "Dashboard" else "transparent")
        self.sidebar_btn_scanner.configure(fg_color=("gray75", "gray25") if name == "Scanner" else "transparent")
        self.sidebar_btn_settings.configure(fg_color=("gray75", "gray25") if name == "Settings" else "transparent")

        # Hide current view
        if self.active_view:
            self.active_view.grid_forget()

        # Show new view
        if name == "Dashboard":
            self.active_view = self.dashboard_view
        elif name == "Scanner":
            self.active_view = self.scanner_view
        elif name == "Settings":
            self.active_view = self.settings_view
            
        self.active_view.grid(row=0, column=1, sticky="nsew")
        self.animate_view_entry(self.active_view)

    def animate_view_entry(self, view):
        """Subtle slide-up effect for CTk"""
        view.grid(row=0, column=1, pady=(20, 0), sticky="nsew") # Start lower
        def slide_up(current_y=20):
            if current_y > 0:
                new_y = current_y - 2
                view.grid(row=0, column=1, pady=(new_y, 0), sticky="nsew")
                self.after(10, lambda: slide_up(new_y))
        slide_up()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
