import json

# We store the data as a string since we cannot add extra files to the folder
json_data = '''
{
  "imdata": [
    {
      "l1PhysIf": {
        "attributes": {
          "dn": "topology/pod-1/node-201/sys/phys-[eth1/33]",
          "descr": "", "speed": "inherit", "mtu": "9150"
        }
      }
    },
    {
      "l1PhysIf": {
        "attributes": {
          "dn": "topology/pod-1/node-201/sys/phys-[eth1/34]",
          "descr": "", "speed": "inherit", "mtu": "9150"
        }
      }
    },
    {
      "l1PhysIf": {
        "attributes": {
          "dn": "topology/pod-1/node-201/sys/phys-[eth1/35]",
          "descr": "", "speed": "inherit", "mtu": "9150"
        }
      }
    }
  ]
}
'''

# We use loads() (load string) instead of load() (load file)
data = json.loads(json_data)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 50, "-" * 20, "-" * 7, "-" * 6)

for item in data.get('imdata', []):
    attr = item.get('l1PhysIf', {}).get('attributes', {})
    print(f"{attr.get('dn', ''):<50} {attr.get('descr', ''):<20} "
          f"{attr.get('speed', ''):<7} {attr.get('mtu', ''):<6}")
