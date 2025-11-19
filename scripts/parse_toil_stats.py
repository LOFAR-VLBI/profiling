import json
import sys

with open(sys.argv[1]) as f:
    jsondata = f.read()
    data = json.loads(jsondata)


max_ram = 0
max_name = ""
for name, job in data["job_types"].items():
    if job["max_memory"] > max_ram:
        max_ram = job["max_memory"]
        max_name = name
    if job["max_memory"] > 8e6:
        print(f"Job {name} used >8GB RAM -- {job['max_memory']/1e6:.2f} GB used")

print(f"Max RAM of {max_ram/1e6}MB used by {max_name}")
