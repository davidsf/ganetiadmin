#!/usr/bin/env python3

from gi.repository import Gtk, GLib, Gio
from http.client import HTTPSConnection
from base64 import b64encode
import json

import confwindow
import conn
import params
import infowindow


class GaneAdmin(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Ganeti Admin")
		self.set_border_width(10)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_default_size(500,500)
		self.set_wmclass("Ganeti Admin", "Ganeti Admin")
		self.connect("delete-event", Gtk.main_quit)

		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = "Ganeti Admin"
		self.set_titlebar(hb)

		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="view-refresh-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		button.connect("clicked", self.update_clicked)
		hb.pack_end(button)

		self.box = Gtk.Box(spacing=6)
		self.add(self.box)

		tree = Gtk.TreeView(params.store)
		tree.connect("row-activated", self.row_clicked)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Machine", renderer, text=0)
		tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Status", renderer, text=1)
		tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Port", renderer, text=2)
		tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Primary node", renderer, text=3)
		tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Memory", renderer, text=4)
		tree.append_column(column)

		swH = Gtk.ScrolledWindow()
		swH.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		swH.add(tree)

		self.box.pack_start(swH, True, True, 0)

	def row_clicked(self, widget, row, col):
		global connection, headers, machines

		model = widget.get_model()
		instance_name = model[row][0]

		data = params.conn.instance_info(instance_name)
		info = infowindow.InfoWindow(instance_name)
		info.show_all()


	def update_clicked(self, widget):
		params.conn.update()

def showall():
	global win
	win.show_all()

conf = confwindow.ConfWindow(showall)
conf.connect("delete-event", Gtk.main_quit)
conf.show_all()

win = GaneAdmin()

Gtk.main()
