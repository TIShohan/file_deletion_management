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
        self.title("CleanSweep | File Deletion Management")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Grid Layout 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Side Navigation
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#ebebeb", "#1a1a1a"))
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # Brand/Logo
        self.brand_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.brand_frame.grid(row=0, column=0, padx=20, pady=40)
        
        self.logo_label = ctk.CTkLabel(
            self.brand_frame, 
            text="CleanSweep", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("#3B8ED0", "#3B8ED0")
        )
        self.logo_label.pack()
        
        self.version_label = ctk.CTkLabel(self.brand_frame, text="v1.0.4 Premium", font=ctk.CTkFont(size=10), text_color="gray50")
        self.version_label.pack()

        # Navigation Buttons
        self.dashboard_button = self.create_nav_button("📊  Dashboard", 1, self.show_dashboard)
        self.scanner_button = self.create_nav_button("🔍  Deep Scanner", 2, self.show_scanner)
        self.settings_button = self.create_nav_button("⚙️   Settings", 3, self.show_settings)
        
        # Appearance Mode Selector at bottom
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
            height=30,
            fg_color="gray25",
            button_color="gray30"
        )
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20)

        # Content Area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Initialize Views
        self.dashboard_view = DashboardView(self.content_frame, db=self.db, corner_radius=0, fg_color="transparent")
        self.scanner_view = ScannerView(self.content_frame, db=self.db, corner_radius=0, fg_color="transparent")
        self.settings_view = SettingsView(self.content_frame, db=self.db, corner_radius=0, fg_color="transparent")
        
        self.active_view = None
        self.select_frame_by_name("Dashboard")

    def create_nav_button(self, text, row, command):
        btn = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=10, 
            height=45, 
            border_spacing=10, 
            text=text,
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            anchor="w", 
            font=ctk.CTkFont(size=14, weight="bold"),
            command=command
        )
        btn.grid(row=row, column=0, sticky="ew", padx=15, pady=5)
        return btn

    def show_dashboard(self):
        self.dashboard_view.refresh_stats()
        self.select_frame_by_name("Dashboard")

    def show_scanner(self):
        self.select_frame_by_name("Scanner")

    def show_settings(self):
        self.select_frame_by_name("Settings")

    def select_frame_by_name(self, name):
        # Update buttons state
        self.dashboard_button.configure(fg_color=("#3B8ED0", "#1f538d") if name == "Dashboard" else "transparent")
        self.scanner_button.configure(fg_color=("#3B8ED0", "#1f538d") if name == "Scanner" else "transparent")
        self.settings_button.configure(fg_color=("#3B8ED0", "#1f538d") if name == "Settings" else "transparent")

        if self.active_view:
            self.active_view.grid_forget()

        if name == "Dashboard": self.active_view = self.dashboard_view
        elif name == "Scanner": self.active_view = self.scanner_view
        elif name == "Settings": self.active_view = self.settings_view
            
        self.active_view.grid(row=0, column=0, sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
