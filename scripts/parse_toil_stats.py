import json
import sys

with open(sys.argv[1]) as f:
    jsondata = f.read()
    data = json.loads(jsondata)


max_ram = 0
max_ram_name = ""

max_cpu = 0
max_cpu_name = ""

max_cpu_wait = 0
max_cpu_wait_name = ""

max_cpu_total = 0
max_cpu_total_name = ""
for name, job in data["job_types"].items():
    if job["max_memory"] > max_ram:
        max_ram = job["max_memory"]
        max_ram_name = name
    if job["max_memory"] > 8e6:
        print(f"Job {name} used >8GB RAM -- {job['max_memory']/1e6:.2f} GB used")

    if job["max_clock"] > max_cpu:
        max_cpu = job["max_clock"]
        max_cpu_name = name

    if job["max_wait"] > max_cpu_wait:
        max_cpu_wait = job["max_wait"]
        max_cpu_wait_name = name

    if (job["max_clock"] + job["max_wait"]) > max_cpu_total:
        max_cpu_total = job["max_clock"] + job["max_wait"]
        max_cpu_total_name = name

print("\n== Summary ==")
print("Total core hours used by workflow:")
print(f"{data['jobs']['total_clock']/3600:.3f} h used")
print(f"{data['jobs']['total_wait']/3600:.3f} h wait")
print(f"{(data['jobs']['total_clock']/3600 + data['jobs']['total_wait']/3600):.3f} h used+wait")
print(f"Max RAM of {max_ram/1e6:.3f}GB used by {max_ram_name}")
print(f"Max CPU hours of {max_cpu/3600:.3f}h used by {max_cpu_name}")
print(f"Max CPU hours of {max_cpu_wait/3600:.3f}h spent waiting by {max_cpu_wait_name}")
print(f"Max CPU hours of {max_cpu_total/3600:.3f}h (used+wait) by {max_cpu_total_name}")
