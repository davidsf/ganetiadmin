from gi.repository import Gtk, GLib, Gio
from http.client import HTTPSConnection
from base64 import b64encode
import json
import params

global connection
global headers

class ganeti_conn:
	def __init__(self, ip, port, username, password):
		global connection, headers
		connection = HTTPSConnection(ip, port=port)

		userpass = username+":"+password
		userAndPass = b64encode(bytes(userpass, "utf-8")).decode("ascii")
		headers = { 'Authorization' : 'Basic %s' %  userAndPass }

	def update(self):
		global connection, headers
		connection.request('GET', '/2/instances?bulk=1', headers=headers)

		response = connection.getresponse()
		data = json.loads(response.read().decode())

		if 'message' in data and data['message']=="Unauthorized":
			return False

		params.store.clear()
		for d in data:
			params.store.append([d['name'], d['status'], d['network_port'], d['pnode'], d['beparams']['memory']])
			params.machines[d['name']] = d

	def instance_info(self, instance_name):
		connection.request('GET', '/2/instances/' + instance_name + '/info?static', headers=headers)

		response = connection.getresponse()
		return json.loads(response.read().decode())

	def reboot(self, instance_name):
		connection.request('POST', '/2/instances/'+instance_name+'/reboot', headers=headers)
