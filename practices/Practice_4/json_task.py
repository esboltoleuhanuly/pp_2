import json

# 1. Load the data from the file
with open('sample-data.json', 'r') as file:
    data = json.load(file)

# 2. Print the Header to match the assignment format
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 50 + " " + "-" * 20 + " " + "-" * 7 + " " + "-" * 6)

# 3. Loop through the 'imdata' list
for item in data["imdata"]:
    # Drill down into the nested structure
    attributes = item["l1PhysIf"]["attributes"]
    
    dn = attributes["dn"]
    description = attributes.get("descr", "")  # Use empty string if missing
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    
    # 4. Print the row with specific column widths
    # <50 means left-aligned with 50 character width
    print(f"{dn:<50} {description:<20} {speed:<7} {mtu:<6}")
    