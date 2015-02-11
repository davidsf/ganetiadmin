from gi.repository import Gtk, GLib, Gio
import json
import params


class InfoWindow(Gtk.Window):
	def	__init__(self, instance_name):
		info = params.machines[instance_name]
		Gtk.Window.__init__(self, title="Machine info: " + instance_name)

		self.instance_name = instance_name
		self.set_border_width(10)
		self.set_position(Gtk.WindowPosition.CENTER)
		hbox = Gtk.Box(spacing=6)
		self.add(hbox)

		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		hbox.pack_start(listbox, True, True, 0)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Primary Node:")
		hbox.pack_start(label, True, True, 0)

		self.input_ip = Gtk.Entry()
		self.input_ip.set_text(info['pnode'])
		hbox.pack_start(self.input_ip, False, True, 0)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Secondary Nodes:")
		hbox.pack_start(label, True, True, 0)

		self.input_ip = Gtk.Entry()
		self.input_ip.set_text(','.join(info['snodes']))
		hbox.pack_start(self.input_ip, False, True, 0)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Bridges:")
		hbox.pack_start(label, True, True, 0)

		self.input_ip = Gtk.Entry()
		self.input_ip.set_text(','.join(info['nic.bridges']))
		hbox.pack_start(self.input_ip, False, True, 0)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("Memory (Mb):")
		hbox.pack_start(label, True, True, 0)

		self.input_ip = Gtk.Entry()
		self.input_ip.set_text(str(info['beparams']['memory']))
		hbox.pack_start(self.input_ip, False, True, 0)

		listbox.add(row)

		disks = info['disk.sizes']
		i = 0
		for disk in disks:
			row = Gtk.ListBoxRow()
			hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
			row.add(hbox)

			label = Gtk.Label("Disk Size #"+str(i)+" (Mb):")
			hbox.pack_start(label, True, True, 0)

			self.input_ip = Gtk.Entry()
			self.input_ip.set_text(str(info['disk.sizes'][i]))
			hbox.pack_start(self.input_ip, False, True, 0)

			listbox.add(row)
			i=i+1

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		label = Gtk.Label("vcpus:")
		hbox.pack_start(label, True, True, 0)

		self.input_ip = Gtk.Entry()
		self.input_ip.set_text(str(info['beparams']['vcpus']))
		hbox.pack_start(self.input_ip, False, True, 0)

		listbox.add(row)


		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		self.reboot_button = Gtk.Button(label="Reboot")
		self.reboot_button.connect("clicked", self.reboot)
		hbox.pack_start(self.reboot_button, True, True, 0)
		if info['status']!="running":
			self.reboot_button.set_sensitive(False)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)

		self.ok_button = Gtk.Button(label="Ok")
		self.ok_button.connect("clicked", self.close)
		hbox.pack_start(self.ok_button, True, True, 0)

		listbox.add(row)

	def close(self, widget):
		self.hide()

	def reboot(self, widget):
		params.conn.reboot(self.instance_name)
		self.hide()
