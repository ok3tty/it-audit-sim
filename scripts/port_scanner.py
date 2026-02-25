import socket
import json
import datetime

TARGETS = {'webserver': ('localhost', [80, 8080]),
	   'database': ('localhost', [3306]),
           'workstation': ('localhost', [22, 2222])}

results = {'scan_data': str(datetime.datetime.now()), 'assets': {}}

for name, (host, ports) in TARGETS.items():
    open_ports = []
    for port in ports:
        try:
            s = socket.create_connection((host, port), timeout=2)
            open_ports.append(port)
            s.close()
        except:
	        pass

    results['assets'][name] = {'open_ports': open_ports}
    print(f'{name}: open_ports = {open_ports}')


with open('../findings/port_scan_results.json', 'w') as file:
    json.dump(results, file, indent=2)
print('Results have been saved to findings/port_scan_results.json file')
