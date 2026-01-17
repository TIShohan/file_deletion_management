import flet as ft

# Color Palette
PRIMARY = "#0078D4"  # Electric Blue
BACKGROUND = "#0F0F0F"  # Deepest Charcoal
SURFACE = "#1E1E1E"  # Lighter Surface
ACCENT = "#2B2B2B"  # Stroke / Hover
TEXT_MAIN = "#FFFFFF"
TEXT_SUB = "#A0A0A0"

# Design Tokens
BORDER_RADIUS = 15
CONTENT_PADDING = 30
TRANSITION_SPEED = 400

def apply_theme(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY,
            surface=SURFACE,
            background=BACKGROUND,
            on_primary=TEXT_MAIN,
            on_surface=TEXT_MAIN,
            outline=ACCENT,
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionByRouteArrived.FADE_UPWARDS,
            macos=ft.PageTransitionByRouteArrived.ZOOM,
        )
    )
    page.bgcolor = BACKGROUND
    page.window_width = 1200
    page.window_height = 850
    page.padding = 0

class PremiumCard(ft.Container):
    def __init__(self, content, expand=False, padding=20, on_click=None):
        super().__init__()
        self.content = content
        self.expand = expand
        self.padding = padding
        self.on_click = on_click
        self.bgcolor = SURFACE
        self.border_radius = BORDER_RADIUS
        self.border = ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE))
        self.animate = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.DECELERATE)

    def on_hover(self, e):
        self.bgcolor = ACCENT if e.data == "true" else SURFACE
        self.scale = 1.02 if e.data == "true" else 1.0
        self.update()
