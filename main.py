import flet as ft
from flet import Colors as colors
Icons = ft.icons.Icons
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

    # Main Shell Components
    content_area = ft.Container(expand=True)
    
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        bgcolor=SURFACE,
        unselected_label_text_style=ft.TextStyle(color=colors.GREY_500, size=12),
        selected_label_text_style=ft.TextStyle(color=PRIMARY, weight=ft.FontWeight.BOLD, size=12),
        indicator_color=colors.with_opacity(0.1, PRIMARY),
        destinations=[
            ft.NavigationRailDestination(
                icon=Icons.DASHBOARD,
                selected_icon=Icons.DASHBOARD,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=Icons.SEARCH,
                selected_icon=Icons.SEARCH,
                label="Scanner",
            ),
            ft.NavigationRailDestination(
                icon=Icons.SETTINGS,
                selected_icon=Icons.SETTINGS,
                label="Settings",
            ),
        ],
        on_change=lambda e: page.push_route(f"/{['dashboard', 'scanner', 'settings'][e.control.selected_index]}"),
    )

    def route_change(e):
        # Clear page content
        page.clean()
        
        # Get current route, default to /dashboard if None or empty
        current_route = page.route if page.route else "/dashboard"
        
        # Determine view based on route
        if current_route == "/scanner":
            sidebar.selected_index = 1
            content_area.content = ScannerView(page, state)
        elif current_route == "/settings":
            sidebar.selected_index = 2
            content_area.content = SettingsView(page, state)
        else: # Default/Dashboard
            sidebar.selected_index = 0
            content_area.content = DashboardView(page, state)

        # Add the main layout directly to page
        page.add(
            ft.Row(
                [
                    sidebar,
                    ft.VerticalDivider(width=1, color=colors.with_opacity(0.1, colors.WHITE)),
                    content_area,
                ],
                expand=True,
                spacing=0,
            )
        )
        page.update()

    page.on_route_change = route_change
    # Initialize the first view directly
    route_change(None)

if __name__ == "__main__":
    ft.run(main)
