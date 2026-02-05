import json
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.colors import LogNorm

filename = sys.argv[1]
with open(filename) as f:
    data = json.load(f)

job_types = data["job_types"]

ram_gb = []
cpu_hours = []
names = []

for jt, stats in job_types.items():
    mem_bytes = stats.get("max_memory", 0)
    mem_gb = mem_bytes / 1e6

    cpu_sec = stats.get("total_clock", 0)
    cpu_hr = cpu_sec / 3600.0

    ram_gb.append(mem_gb)
    cpu_hours.append(cpu_hr)
    names.append(jt)

ram_gb = np.array(ram_gb)
cpu_hours = np.array(cpu_hours)
names = np.array(names)
highmem = ram_gb > 8

plt.figure(figsize=(6, 6), dpi=300)
hb = plt.hexbin(
    ram_gb,
    cpu_hours,
    gridsize=40,
    xscale="log",
    yscale="log",
    norm=LogNorm(),  # log colour scale
    cmap="viridis",
    mincnt=1,  # hide empty bins
)
for name, ram, cpu in zip(names[highmem], ram_gb[highmem], cpu_hours[highmem]):
    plt.scatter(ram, cpu, marker=".", color="r")
    plt.text(ram * 1.2, cpu, name.split(".")[-1], fontsize="small")

cbar = plt.colorbar(hb, orientation="horizontal")
cbar.set_label("Number of jobs")
plt.axvline(8, color="k", linestyle="--")
plt.xlabel("Peak memory usage [GB]")
plt.ylabel("CPU time [h]")
plt.xlim(1e-1, 1e3)
plt.tight_layout()
plt.savefig(f"cpu_vs_ram_heatmap_{os.path.basename(filename.rstrip('.json'))}.png")
