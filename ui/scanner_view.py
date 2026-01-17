import flet as ft
from ui.style import PremiumCard, PRIMARY, TEXT_SUB, CONTENT_PADDING, BORDER_RADIUS, SURFACE
from backend.worker import ScanWorker

class ScannerView(ft.Container):
    def __init__(self, page: ft.Page, state: dict):
        super().__init__()
        self.page = page
        self.state = state
        self.expand = True
        self.worker = None
        self.content = self.build_ui()

    def build_ui(self):
        # Scan Controls
        self.progress_ring = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)
        self.progress_text = ft.Text("Ready", color=TEXT_SUB, size=12)
        self.scan_button = ft.ElevatedButton(
            "Start Depth Scan", 
            icon=ft.icons.PLAY_ARROW_ROUNDED, 
            on_click=self.start_scan,
            style=ft.ButtonStyle(bgcolor=PRIMARY, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10)),
            disabled=not self.state["selected_path"]
        )

        # Filters
        self.search_box = ft.TextField(
            hint_text="Search files...",
            prefix_icon=ft.icons.SEARCH,
            bgcolor=SURFACE,
            border_radius=10,
            on_change=lambda _: self.load_results(),
            expand=True
        )
        
        self.dupe_filter = ft.Checkbox(label="Only Duplicates", on_change=lambda _: self.load_results())
        
        self.results_list = ft.ListView(expand=True, spacing=5, padding=10)
        self.selected_files = set()

        # Action Buttons
        self.dry_run_btn = ft.OutlinedButton(
            "Dry Run", 
            icon=ft.icons.PREVIEW, 
            on_click=self.show_dry_run,
            visible=False
        )
        self.delete_btn = ft.ElevatedButton(
            "Delete Selected", 
            icon=ft.icons.DELETE_FOREVER, 
            bgcolor=ft.colors.RED_700, 
            color=ft.colors.WHITE,
            on_click=self.confirm_delete,
            visible=False
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("File Scanner", size=28, weight=ft.FontWeight.BOLD),
                            ft.Row([self.progress_ring, self.progress_text], spacing=10),
                            self.scan_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row([self.search_box, self.dupe_filter], spacing=20),
                    ft.Container(
                        content=self.results_list,
                        expand=True,
                        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                        border_radius=BORDER_RADIUS,
                    ),
                    ft.Row(
                        [
                            ft.Text(f"0 files selected", id="selection_text", color=TEXT_SUB),
                            ft.Row([self.dry_run_btn, self.delete_btn], spacing=10)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        visible=False,
                        id="action_row"
                    )
                ],
                spacing=20,
            ),
            padding=CONTENT_PADDING,
            expand=True,
        )

    def start_scan(self, _):
        if not self.state["selected_path"]: return

        self.scan_button.disabled = True
        self.progress_ring.visible = True
        self.selected_files.clear()
        self.update_actions()
        self.update()

        def on_progress(count, message):
            self.progress_text.value = f"{count} files | {message[:30]}..."
            self.update()

        def on_complete(message):
            self.progress_text.value = "Scan successful"
            self.progress_ring.visible = False
            self.scan_button.disabled = False
            self.load_results()
            self.update()

        # Parse skip extensions from settings
        skip_list = {ext.strip().lower() for ext in self.state.get("skip_extensions", "").split(",") if ext.strip()}

        self.worker = ScanWorker(
            self.state["selected_path"],
            self.state["db"],
            skip_extensions=skip_list,
            progress_callback=on_progress,
            completion_callback=on_complete
        )
        self.worker.start()

    def update_actions(self):
        row = self.content.controls[3]
        sel_text = row.controls[0]
        count = len(self.selected_files)
        
        row.visible = count > 0
        sel_text.value = f"{count} files selected"
        self.dry_run_btn.visible = count > 0
        self.delete_btn.visible = count > 0
        self.update()

    def on_file_select(self, e, file_path):
        if e.control.value:
            self.selected_files.add(file_path)
        else:
            self.selected_files.discard(file_path)
        self.update_actions()

    def show_dry_run(self, _):
        # Create a preview list
        preview_items = ft.ListView(expand=True, spacing=5)
        for path in list(self.selected_files)[:50]: # Limit preview
             preview_items.controls.append(ft.Text(path, size=11, color=TEXT_SUB))
        
        if len(self.selected_files) > 50:
            preview_items.controls.append(ft.Text(f"...and {len(self.selected_files)-50} more", italic=True))

        dlg = ft.AlertDialog(
            title=ft.Text("Dry Run Preview"),
            content=ft.Container(content=preview_items, height=300),
            actions=[ft.TextButton("Close", on_click=lambda e: self.page.close(dlg))],
        )
        self.page.open(dlg)

    def confirm_delete(self, _):
        def do_delete(e):
            self.page.close(dlg)
            self.perform_deletion()

        dlg = ft.AlertDialog(
            title=ft.Text("Danger Zone!"),
            content=ft.Text(f"Are you sure you want to move {len(self.selected_files)} files to the Recycle Bin?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dlg)),
                ft.ElevatedButton("Yes, Delete Them", bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, on_click=do_delete),
            ],
        )
        self.page.open(dlg)

    def perform_deletion(self):
        import send2trash
        success = 0
        errors = 0
        
        for path in self.selected_files:
            try:
                send2trash.send2trash(path)
                # Remove from DB
                with self.state["db"].get_connection() as conn:
                    conn.execute("DELETE FROM files WHERE path = ?", (path,))
                success += 1
            except Exception:
                errors += 1

        self.selected_files.clear()
        self.load_results()
        self.update_actions()
        
        snack = ft.SnackBar(ft.Text(f"Deleted {success} files. Errors: {errors}"))
        self.page.open(snack)

    def load_results(self):
        search = self.search_box.value.lower()
        only_dupes = self.dupe_filter.value
        
        query = "SELECT * FROM files WHERE (filename LIKE ? OR folder LIKE ?)"
        params = [f"%{search}%", f"%{search}%"]
        
        if only_dupes:
            query += " AND is_duplicate = 1"
            
        query += " ORDER BY size_bytes DESC LIMIT 200"

        with self.state["db"].get_connection() as conn:
            files = conn.execute(query, params).fetchall()
            
        self.results_list.controls.clear()
        for f in files:
            is_dupe = f['is_duplicate']
            path = f['path']
            self.results_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(
                        ft.icons.INSERT_DRIVE_FILE if not is_dupe else ft.icons.COPY_ALL, 
                        color=ft.colors.BLUE_200 if not is_dupe else ft.colors.ORANGE_400
                    ),
                    title=ft.Text(f['filename'], weight=ft.FontWeight.BOLD if is_dupe else None),
                    subtitle=ft.Text(f"{f['size_mb']} MB • {f['folder']}", size=11, color=TEXT_SUB),
                    trailing=ft.Checkbox(
                        value=path in self.selected_files,
                        on_change=lambda e, p=path: self.on_file_select(e, p)
                    ),
                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.ORANGE_900) if is_dupe else None,
                )
            )
        self.update()
