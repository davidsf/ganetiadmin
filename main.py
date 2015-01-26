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

		sorted_model = Gtk.TreeModelSort(model=params.store)
		sorted_model.set_sort_column_id(0, Gtk.SortType.ASCENDING)

		self.tree = Gtk.TreeView(sorted_model)
		self.tree.connect("row-activated", self.row_clicked)
		self.tree.connect("button_release_event", self.mouse_click)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Machine", renderer, text=0)
		column.set_sort_column_id(0)
		self.tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Status", renderer, text=1)
		column.set_sort_column_id(1)
		self.tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Port", renderer, text=2)
		column.set_sort_column_id(2)
		self.tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Primary node", renderer, text=3)
		column.set_sort_column_id(3)
		self.tree.append_column(column)

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Memory", renderer, text=4)
		column.set_sort_column_id(4)
		self.tree.append_column(column)

		swH = Gtk.ScrolledWindow()
		swH.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		swH.add(self.tree)

		self.box.pack_start(swH, True, True, 0)

		self.menu()

	def row_clicked(self, widget, row, col):
		self.show_info_window()

	def show_info_window(self):
		instance_name = self.get_selected_instance()
		data = params.conn.instance_info(instance_name)
		info = infowindow.InfoWindow(instance_name)
		info.show_all()


	def info_window_cb(self, widget):
		self.show_info_window()

	def reboot_cb(self, widget):
		instance_name = self.get_selected_instance()
		dialog = ConfirmDialog(self)
		dialog.set_label("Would you like to reboot instance " + instance_name + " ?")
		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			params.conn.reboot(instance_name)

		dialog.destroy()

	def start_cb(self, widget):
		instance_name = self.get_selected_instance()
		params.conn.start(instance_name)

	def shutdown_cb(self, widget):
		instance_name = self.get_selected_instance()
		params.conn.shutdown(instance_name)

	def update_clicked(self, widget):
		params.conn.update()

	def menu(self):
		self.treeview_menu = Gtk.Menu()
		menu_item = Gtk.MenuItem("Information")
		menu_item.connect("activate", self.info_window_cb)
		self.treeview_menu.append(menu_item)

		menu_item = Gtk.MenuItem("Reboot")
		menu_item.connect("activate", self.reboot_cb)
		self.treeview_menu.append(menu_item)

		menu_item = Gtk.MenuItem("Start")
		menu_item.connect("activate", self.start_cb)
		self.treeview_menu.append(menu_item)

		menu_item = Gtk.MenuItem("Shutdown")
		menu_item.connect("activate", self.shutdown_cb)
		self.treeview_menu.append(menu_item)

	def mouse_click(self, tv, event):
		if event.button == 3:
			instance_name = self.get_selected_instance()
			info = params.machines[instance_name]
			for menuitem in self.treeview_menu.get_children():
				if menuitem.get_label()=="Reboot":
					if info['status']!="running":
						menuitem.set_sensitive(False)
					else:
						menuitem.set_sensitive(True)
				if menuitem.get_label()=="Start":
					if info['status']!="running":
						menuitem.set_sensitive(True)
					else:
						menuitem.set_sensitive(False)

				if menuitem.get_label()=="Shutdown":
					if info['status']=="running":
						menuitem.set_sensitive(True)
					else:
						menuitem.set_sensitive(False)

			self.treeview_menu.show_all()
			self.treeview_menu.popup(None, None, None, None, 1, 0)

	def get_selected_instance(self):
		selection = self.tree.get_selection()
		(model, iter) = selection.get_selected()
		if iter != None:
			return model[iter][0]
		else:
			return None

class ConfirmDialog(Gtk.Dialog):

	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Confirmation", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.set_default_size(150, 100)

	def set_label(self, text):
		label = Gtk.Label(text)
		box = self.get_content_area()
		box.add(label)
		self.show_all()

def showall():
	global win
	win.show_all()

conf = confwindow.ConfWindow(showall)
conf.connect("delete-event", Gtk.main_quit)
conf.show_all()

win = GaneAdmin()

Gtk.main()
