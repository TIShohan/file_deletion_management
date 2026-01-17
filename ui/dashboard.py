from ui.style import PremiumCard, PRIMARY, TEXT_SUB, CONTENT_PADDING, BORDER_RADIUS

class DashboardView(ft.Container):
    def __init__(self, page: ft.Page, state: dict):
        super().__init__()
        self.page = page
        self.state = state
        self.expand = True
        self.content = self.build_ui()

    def build_ui(self):
        if not self.state["selected_path"]:
            return self.build_welcome_screen()
        return self.build_dashboard_content()

    def build_welcome_screen(self):
        def pick_folder_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.state["selected_path"] = e.path
                self.content = self.build_ui()
                self.update()

        pick_folder_dialog = ft.FilePicker(on_result=pick_folder_result)
        self.page.overlay.append(pick_folder_dialog)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(ft.icons.FOLDER_OPEN_ROUNDED, size=80, color=PRIMARY),
                        padding=30,
                        bgcolor=ft.colors.with_opacity(0.1, PRIMARY),
                        border_radius=50,
                    ),
                    ft.Text("Storage Analyzer", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text("Connect a local drive or select a folder to start the cleaning process.", color=TEXT_SUB, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton(
                        "Scan New Directory",
                        icon=ft.icons.ADD_ROUNDED,
                        on_click=lambda _: pick_folder_dialog.get_directory_path(),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=PRIMARY,
                            padding=25,
                            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            expand=True,
            alignment=ft.alignment.center,
        )

    def build_dashboard_content(self):
        # Fetch actual data from DB
        stats = self.get_db_stats()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column([
                                ft.Text("System Overview", size=28, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Target: {self.state['selected_path']}", color=TEXT_SUB),
                            ]),
                            ft.IconButton(ft.icons.REFRESH_ROUNDED, on_click=lambda _: self.update_dashboard())
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        [
                            self.summary_card("Total Files", stats['count'], ft.icons.INSERT_DRIVE_FILE, ft.colors.BLUE_400),
                            self.summary_card("Duplicates Found", stats['dupes'], ft.icons.COPY_ALL, ft.colors.ORANGE_400),
                            self.summary_card("Potential Recovery", f"{stats['size']} GB", ft.icons.STORAGE, ft.colors.GREEN_400),
                        ],
                        spacing=20,
                    ),
                    ft.Divider(height=20, color=ft.colors.with_opacity(0.1, ft.colors.WHITE)),
                    ft.Text("Storage Distribution", size=20, weight=ft.FontWeight.BOLD),
                    self.build_folder_summary(),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                spacing=25,
            ),
            padding=CONTENT_PADDING,
            expand=True,
        )

    def get_db_stats(self):
        with self.state["db"].get_connection() as conn:
            row = conn.execute("SELECT COUNT(*), SUM(size_mb) FROM files").fetchone()
            dupe_row = conn.execute("SELECT COUNT(*) FROM files WHERE is_duplicate = 1").fetchone()
            
            count = row[0] if row[0] else 0
            size = round(row[1] / 1024, 2) if row[1] else 0
            dupes = dupe_row[0] if dupe_row[0] else 0
            
            return {"count": str(count), "size": str(size), "dupes": str(dupes)}

    def summary_card(self, title, value, icon, color):
        return PremiumCard(
            content=ft.Column(
                [
                    ft.Icon(icon, color=color, size=30),
                    ft.Text(title, size=14, color=TEXT_SUB),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD),
                ],
                spacing=5
            ),
            expand=True
        )

    def build_folder_summary(self):
        with self.state["db"].get_connection() as conn:
            folders = conn.execute("SELECT folder, SUM(size_mb) as total FROM files GROUP BY folder ORDER BY total DESC LIMIT 5").fetchall()
        
        controls = []
        for folder in folders:
            size_gb = round(folder['total'] / 1024, 2)
            controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.FOLDER),
                    title=ft.Text(os.path.basename(folder['folder']) if folder['folder'] else "Root"),
                    subtitle=ft.Text(folder['folder'], size=11, color=TEXT_SUB),
                    trailing=ft.Text(f"{size_gb} GB", weight=ft.FontWeight.BOLD, color=PRIMARY),
                )
            )
        return PremiumCard(content=ft.Column(controls) if controls else ft.Text("No data available. Run a scan."))

    def update_dashboard(self):
        self.content = self.build_ui()
        self.update()
