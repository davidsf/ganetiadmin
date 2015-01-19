from gi.repository import Gtk, GLib, Gio
from http.client import HTTPSConnection
from base64 import b64encode
import json

import conn
import params

class ConfWindow(Gtk.Window):
	def	__init__(self, callback):
		Gtk.Window.__init__(self, title="Configuration")
		self.set_border_width(10)
		self.set_position(Gtk.WindowPosition.CENTER)

		hbox = Gtk.Box(spacing=6)
		self.add(hbox)

		self.callback = callback

		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		hbox.pack_start(listbox, True, True, 0)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Cluster IP:")
		hbox.pack_start(label, True, True, 0)

		self.input_ip = Gtk.Entry()
		hbox.pack_start(self.input_ip, False, True, 0)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Cluster Port:")
		hbox.pack_start(label, True, True, 0)

		self.input_port = Gtk.Entry()
		self.input_port.set_text("5080")
		hbox.pack_start(self.input_port, False, True, 0)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Username:")
		hbox.pack_start(label, True, True, 0)

		self.input_username = Gtk.Entry()
		self.input_username.set_text("admin")
		hbox.pack_start(self.input_username, False, True, 0)

		listbox.add(row)


		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Password:")
		hbox.pack_start(label, True, True, 0)

		self.input_password = Gtk.Entry()
		self.input_password.set_visibility(False)
		self.input_password.connect("activate", self.on_ok_button_clicked)
		hbox.pack_start(self.input_password, False, True, 0)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		self.ok_button = Gtk.Button(label="Ok")
		self.ok_button.connect("clicked", self.on_ok_button_clicked)
		hbox.pack_start(self.ok_button, True, True, 0)

		listbox.add(row)

	def on_ok_button_clicked(self, widget):
		global cluster_ip, cluster_port, username, password, connection, headers
		cluster_ip = self.input_ip.get_text()
		cluster_port = self.input_port.get_text()
		username = self.input_username.get_text()
		password = self.input_password.get_text()
		params.conn = conn.ganeti_conn(cluster_ip, cluster_port, username, password)
		result = params.conn.update()
		if result==False:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
			Gtk.ButtonsType.OK, "Connection Error")
			dialog.format_secondary_text("Username or password incorrect")
			dialog.run()
			dialog.destroy()
		else:
			self.hide()
			self.callback()
