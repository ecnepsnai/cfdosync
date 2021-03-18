import requests
import json
import os
import sys

firewall_id = os.environ.get('FIREWALL_ID', None)
if firewall_id is None or len(firewall_id) == 0:
    print('Required environment variable FIREWALL_ID not set')
    sys.exit(1)

api_key = os.environ.get('API_KEY', None)
if api_key is None or len(api_key) == 0:
    print('Required environment variable API_KEY not set')
    sys.exit(1)

firewall_response = requests.get('https://api.digitalocean.com/v2/firewalls/' + firewall_id, headers={'Authorization': 'Bearer ' + api_key})
if firewall_response.status_code != 200:
    print("HTTP " + str(firewall_response.status_code) + " getting firewall")
    print(firewall_response.text)
    sys.exit(1)

firewall = firewall_response.json()["firewall"]

ipv4_hosts_response = requests.get('https://www.cloudflare.com/ips-v4')
if ipv4_hosts_response.status_code != 200:
    print("HTTP " + str(ipv4_hosts_response.status_code) + " getting IPv4 hosts")
    sys.exit(1)
ipv6_hosts_response = requests.get('https://www.cloudflare.com/ips-v6')
if ipv6_hosts_response.status_code != 200:
    print("HTTP " + str(ipv6_hosts_response.status_code) + " getting IPv6 hosts")
    sys.exit(1)

ipv4_hosts = ipv4_hosts_response.text.rstrip().split('\n')
ipv6_hosts = ipv6_hosts_response.text.rstrip().split('\n')
cloudflare_hosts = []
cloudflare_hosts.extend(ipv4_hosts)
cloudflare_hosts.extend(ipv6_hosts)

firewall["inbound_rules"][0]["sources"]["addresses"] = cloudflare_hosts

# The DigitalOcean API is dumb in that you can't simply pass back the object you get from it
# Even though it returns "ports": "0", it won't accept that.
# For ICMP, delete the ports property.
# For everything else, replace "0" with "all"
i = 0
while i < len(firewall["outbound_rules"]):
    rule = firewall["outbound_rules"][i]
    protocol = rule["protocol"]

    if protocol == "icmp":
        del firewall["outbound_rules"][i]["ports"]
    elif rule["ports"] == "0":
        firewall["outbound_rules"][i]["ports"] = "all"

    i += 1

update_response = requests.put('https://api.digitalocean.com/v2/firewalls/' + firewall_id, json=firewall, headers={'Authorization': 'Bearer ' + api_key})
if update_response.status_code != 200:
    print("HTTP " + str(update_response.status_code) + " updating firewall")
    print(update_response.text)
    sys.exit(1)

print("Updated firewall: " + firewall["name"])
