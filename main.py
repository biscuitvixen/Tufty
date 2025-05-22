from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import random
import json

display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332, rotate=180)
WIDTH, HEIGHT = display.get_bounds()


# --- Load all themes from JSON ---
def load_all_themes():
    with open("/secrets/themes.json", "r") as f:
        data = json.load(f)

    if not data:
        raise ValueError("No themes found in /secrets/themes.json")

    themes = {}
    for name, entry in data.items():
        colours = entry["colours"]
        palette = [display.create_pen(r, g, b) for r, g, b in colours]
        themes[name] = palette

    return themes


# Set up themes and default theme
ALL_THEMES = load_all_themes()
THEME_NAME = list(ALL_THEMES.keys())[0]
PALETTE = ALL_THEMES[THEME_NAME]


# --- Background Rendering ---
def render_background():
    band_height = HEIGHT // len(PALETTE)

    for i, colour in enumerate(PALETTE):
        y_top = i * band_height
        y_bottom = y_top + band_height
        points = []

        if i == 0:
            points = [(0, y_top), (WIDTH, y_top), (WIDTH, y_bottom), (0, y_bottom)]
        else:
            x = 0
            points.append((0, y_top))
            while x < WIDTH:
                tri_width = random.randint(10, 30)
                tri_height = random.randint(5, 20)

                peak_x = x + tri_width // 2
                next_x = x + tri_width

                points.append((x, y_top))
                points.append((peak_x, y_top - tri_height))
                points.append((next_x, y_top))

                x = next_x

            points += [(WIDTH, y_bottom), (0, y_bottom)]

        display.set_pen(colour)
        display.polygon(points)


# --- Draw theme name ---
def draw_theme_label():
    display.set_pen(display.create_pen(255, 255, 255))  # White
    display.text(THEME_NAME, 5, 5, scale=2)


# --- Main ---
display.set_pen(display.create_pen(0, 0, 0))
display.clear()

render_background()
draw_theme_label()
display.update()
