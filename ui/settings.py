import flet as ft
from flet import Colors as colors
Icons = ft.icons.Icons
from ui.style import PremiumCard, CONTENT_PADDING, TEXT_SUB, BORDER_RADIUS, PRIMARY

class SettingsView(ft.Container):
    def __init__(self, page: ft.Page, state: dict):
        super().__init__()
        self._page = page
        self.state = state
        self.expand = True
        
        # Load current skip extensions from backend scanner default if not in state
        if "skip_extensions" not in self.state:
            # For now default to a standard set
            self.state["skip_extensions"] = ".sys, .dll, .exe, .ini, .dat"
            
        self.content = self.build_ui()

    def build_ui(self):
        self.extensions_input = ft.TextField(
            label="Skip Extensions (comma separated)",
            value=self.state["skip_extensions"],
            hint_text="e.g. .sys, .dll, .tmp",
            border_radius=10,
            on_change=self.save_settings
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Settings", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Configure application behavior and defaults.", color=TEXT_SUB),
                    ft.Divider(height=20, color=colors.with_opacity(0.1, colors.WHITE)),
                    
                    ft.Text("Scan Filters", size=18, weight=ft.FontWeight.BOLD),
                    PremiumCard(
                        content=ft.Column([
                            ft.Text("Exclusion List", weight=ft.FontWeight.BOLD),
                            ft.Text("Files with these extensions will be ignored during scans.", size=12, color=TEXT_SUB),
                            self.extensions_input,
                        ], spacing=10)
                    ),
                    
                    ft.Text("Privacy & Safety", size=18, weight=ft.FontWeight.BOLD),
                    PremiumCard(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("Recycle Bin Backup", weight=ft.FontWeight.BOLD),
                                ft.Text("Always move files to Recycle Bin instead of permanent deletion.", size=12, color=TEXT_SUB),
                            ], expand=True),
                            ft.Switch(value=True, disabled=True) # Forced for now
                        ])
                    ),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            "Save & Apply Settings",
                            icon=Icons.SAVE,
                            style=ft.ButtonStyle(bgcolor=PRIMARY, color=colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda _: self.save_and_show_snack()
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ],
                spacing=20,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            padding=CONTENT_PADDING,
            expand=True
        )

    def save_and_show_snack(self):
        self.state["skip_extensions"] = self.extensions_input.value
        snack = ft.SnackBar(ft.Text("Settings saved!"))
        self._page.snack_bar = snack
        snack.open = True
        self._page.update()

    def save_settings(self, e):
        self.state["skip_extensions"] = self.extensions_input.value
