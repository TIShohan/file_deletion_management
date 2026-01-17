import flet as ft
from flet import Colors as colors

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
    # Setup theme for Flet 0.80.2
    page.theme_mode = ft.ThemeMode.DARK
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
        self.border = ft.border.all(1, colors.with_opacity(0.1, colors.WHITE))
        self.animate = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.DECELERATE)

    def on_hover(self, e):
        self.bgcolor = ACCENT if e.data == "true" else SURFACE
        self.scale = 1.02 if e.data == "true" else 1.0
        self.update()
