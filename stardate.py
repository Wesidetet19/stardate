#!/usr/bin/env python3

import gi
import time
from datetime import datetime
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk
import cairo

# Function to calculate the Stardate
def calculate_stardate():
    now = datetime.now()
    year = now.year
    day_of_year = now.timetuple().tm_yday

    # Stardate formula
    stardate = (year - 2000) * 1000.0 + (day_of_year / 365.0) * 100.0
    return f"{stardate:.1f}"

# Main application window
class StardateWidget(Gtk.Window):
    def __init__(self):
        super().__init__(title="Stardate Widget")
        self.set_default_size(200, 100)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.connect("draw", self.on_draw)

        # Load custom CSS for styling
        self.load_css()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.box)

        # Create a label to display the Stardate
        self.label = Gtk.Label(label=calculate_stardate())
        self.label.set_name("stardate-label")  # Assign a CSS class
        self.box.pack_start(self.label, True, True, 0)
        self.close_button = Gtk.Button(label="×")  # Unicode "×" for close symbol
        self.close_button.set_name("close-button")  # Assign a CSS class
        self.close_button.connect("clicked", self.on_close_clicked)
        self.box.pack_end(self.close_button, False, False, 0)

        # Update the Stardate every second
        GLib.timeout_add_seconds(1, self.update_stardate)

    # Function to update the Stardate
    def update_stardate(self):
        self.label.set_text(calculate_stardate())
        return True

    def on_close_clicked(self, button):
        self.destroy()

    # Load custom CSS
    def load_css(self):
        css = """
        window {
            background-color: transparent;
            border-radius: 20px; /* Rounded corners */
        }
        #stardate-label {
            font-family: 'Roddenberry', sans-serif;
            font-size: 48px;
            font-weight: bold;
            color: #FFD700; /* Gold color */
            background-color: #000033; /* Dark blue background */
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #FFD700;
        }
        #close-button {
            font-family: 'Arial', sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: #FFD700; /* Gold color */
            background-color: transparent;
            border: none;
            padding: 5px;
            opacity: 0; /* Hidden by default */
            transition: opacity 0.2s ease-in-out;
        }
        #close-button:hover {
            opacity: 1; /* Visible on hover */
        }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        return False


if __name__ == "__main__":
    win = StardateWidget()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
