from ui.style import apply_theme, BACKGROUND, SURFACE, PRIMARY
from ui.dashboard import DashboardView
from ui.scanner_view import ScannerView
from ui.settings import SettingsView
from backend.database import DatabaseManager

def main(page: ft.Page):
    apply_theme(page)
    page.title = "Antigravity File Manager"
    
    # Initialize DB
    db_manager = DatabaseManager()

    # Shared State
    state = {
        "selected_path": None,
        "db": db_manager,
        "skip_extensions": ".sys, .dll, .exe, .ini, .dat"
    }

    def route_change(e):
        page.views.clear()
        
        # Modern Navigation Rail
        sidebar = ft.NavigationRail(
            selected_index=0 if page.route in ["/", "/dashboard"] else 1 if page.route == "/scanner" else 2,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            bgcolor=SURFACE,
            unselected_label_style=ft.TextStyle(color=ft.colors.GREY_500, size=12),
            selected_label_style=ft.TextStyle(color=PRIMARY, weight=ft.FontWeight.BOLD, size=12),
            indicator_color=ft.colors.with_opacity(0.1, PRIMARY),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SEARCH_OUTLINED,
                    selected_icon=ft.icons.SEARCH,
                    label="Scanner",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=lambda e: page.go(f"/{['dashboard', 'scanner', 'settings'][e.control.selected_index]}"),
        )

        content_view = ft.Container(expand=True)
        if page.route == "/dashboard" or page.route == "/":
            content_view.content = DashboardView(page, state)
        elif page.route == "/scanner":
            content_view.content = ScannerView(page, state)
        elif page.route == "/settings":
            content_view.content = SettingsView(page, state)

        page.views.append(
            ft.View(
                page.route,
                [
                    ft.Row(
                        [
                            sidebar,
                            ft.VerticalDivider(width=1, color=ft.colors.with_opacity(0.1, ft.colors.WHITE)),
                            content_view,
                        ],
                        expand=True,
                        spacing=0,
                    )
                ],
                padding=0,
            )
        )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)
