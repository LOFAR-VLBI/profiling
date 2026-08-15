import json,pandas as pd,os,sys,csv,ast,numpy as np,shutil
import re
INFILE = sys.argv[1]
with open(INFILE, encoding='utf-8-sig') as f_input:
    df = pd.read_json(f_input)

csvfile = INFILE.replace('json','csv')
df.to_csv(csvfile, encoding='utf-8', index=False)

with open(csvfile,mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    irow=0
    for row in csv_reader:
        if '{' in row[8]:
            a=ast.literal_eval(row[8])
            name=a['name'].replace('ResolveIndirect','').replace('CWLWorkflow','').replace('CWLJob','').replace("Wrapper","")
            new = np.array([a['total_time'],a['total_clock'],a['total_wait'],\
                            a['total_memory'],a['total_cores']],dtype='float')
            try:
                fname = np.append(fname,name)
                fnum = np.vstack((fnum,new))
            except:
                fname = np.array([name],dtype='str')
                fnum = np.copy(new)
        irow+=1

order = np.argsort(fnum[:,0])[::-1]
fname = fname[order]
fnum = fnum[order]
#print(" "*55+"Job"+" "*2+"| Total time (m) | Total clock (m) | Total wait (m) | Total memory (Mb) | Total core |")
#for i in range(len(fname)):
#     print('%60s     %8.3f          %8.3f        %9.3f      %10d %3d'%(fname[i],fnum[i,0]/60,fnum[i,1]/60,fnum[i,2]/60,int(fnum[i,3])/1e3,fnum[i,4]))



def sum_by_base_name(jsonfile):
    """
    Takes iterable of lines from the file.
    Returns dict: {base_name: [sum_col1, sum_col2, ...]}
    """
    totals = {}

    with open(jsonfile) as f:
        jsondata = f.read()
        data = json.loads(jsondata)
    for name, jobstats in data["job_types"].items():
        name=name.replace('ResolveIndirect','').replace('CWLWorkflow','').replace('CWLJob','').replace("Wrapper","").strip()
        # Remove numeric section between first and second dot
        # finalize.10.applytarget -> finalize.applytarget
        base_name = re.sub(r'\.\d+\.', '.', name)

        jobstats.pop("name")
        jobstats["total_billed"] = (jobstats["total_time"] + jobstats["total_wait"])
        if base_name not in totals:
            totals[base_name] = jobstats
        else:
            for key, value in jobstats.items():
                totals[base_name][key] += value

    return totals

#r = sum_by_base_name("./data/toil_stats_linc_target_L337626.json")
r = sum_by_base_name("./toil_stats_LockmanD_newlinc.json")
#print(r["gsmcal.identify_bad_antennas"])
r_sorted = {k: v for k, v in sorted(r.items(), key=lambda item: item[1]["total_billed"], reverse=True)}
#print(r_sorted["gsmcal.identify_bad_antennas"])
#print(" "*55+"Job"+" "*2+"| Total time (h) | Total clock (core h) | Total wait (core h) | Total memory (MB) | Total core | Total billed (core h)")
for k,v in r_sorted.items():
    print('%-60s     %8.3f          %8.3f        %9.3f      %10d     %5d       %.2f'%(k,v["total_time"]/3600,v["total_clock"]/3600,v["total_wait"]/3600,int(v["total_memory"]),v["total_cores"], v["total_billed"] / 3600))


r_sorted = dict(list(r_sorted.items())[:5])
r_sorted_remain = dict(list(r_sorted.items())[5:])
labels = list(r_sorted.keys())
values = [x["total_billed"]/3600 for x in r_sorted.values()]
values_remain = sum([x["total_billed"]/3600 for x in r_sorted_remain.values()])

labels.append("other")
values.append(values_remain)

import matplotlib.pyplot as plt
plt.figure(figsize=(6,6), dpi=300)
plt.bar(labels, values)#, autopct='%1.1f%%')
plt.xticks(rotation=90, va="bottom", y=0.075, fontsize=12)
plt.ylabel("Core hours billed (cores + wait)")
plt.savefig("core_hours_bars_new.png", bbox_inches="tight")
#plt.show()
