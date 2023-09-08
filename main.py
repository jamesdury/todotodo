from configparser import ConfigParser
import requests
import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango


class TextViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="todotodo")

        self.set_default_size(800, 200)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.create_textview()
        self.create_buttons()

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textview.set_border_width(10)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textbuffer = self.textview.get_buffer()

        scrolledwindow.add(self.textview)

    def create_buttons(self):
        button = Gtk.Button.new_with_label("Submit")
        button.connect("clicked", self.on_click_me_clicked)
        self.grid.attach(button, 2, 2, 1, 1)

    def get_todotodo(self):
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        text = self.textbuffer.get_text(start_iter, end_iter, False)
        return text

    def on_click_me_clicked(self, button):
        data = {"content": self.get_todotodo()}

        bearer = self.get_config().get("API", "token")
        url_post = "https://api.todoist.com/rest/v2/tasks"
        headers = {"Authorization": "Bearer {}".format(bearer)}
        post_response = requests.post(url_post, json=data, headers=headers)

        if post_response.status_code != 200:
            post_response.raise_for_status()

        Gtk.main_quit()

    def get_config(self):
        config_location = self.config_file()

        try:
            open(config_location)
        except IOError:
            raise IOError("{} does not exist".format(config_location))

        config = ConfigParser()
        config.read(self.config_file())

        return config

    def config_file(self):
        if "APPDATA" in os.environ:
            confighome = os.environ["APPDATA"]
        elif "XDG_CONFIG_HOME" in os.environ:
            confighome = os.environ["XDG_CONFIG_HOME"]
        else:
            confighome = os.path.join(os.environ["HOME"], ".config")

        configpath = os.path.join(confighome, "todotodo")
        return configpath


win = TextViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
