from gi.repository import Gtk
machines = {}
store = Gtk.ListStore(str, str, int, str, int)
cluster_ip = ""
cluster_port = ""
machine_json = ""
username = ""
password = ""
global connection
