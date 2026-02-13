import json,pandas as pd,os,sys,csv,ast,numpy as np,shutil
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
            name=a['name'].replace('ResolveIndirect','').replace('CWLWorkflow','').replace('CWLJob','')
            new = np.array([a['total_time'],a['total_clock'],a['total_wait'],\
                            a['total_memory']],dtype='float')
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
print(" "*55+"Job"+" "*2+"| Total time (m) | Total clock (m) | Total wait (m) | Total memory (Mb)")
for i in range(len(fname)):
     print('%60s     %8.3f          %8.3f        %9.3f      %10d'%(fname[i],fnum[i,0]/60,fnum[i,1]/60,fnum[i,2]/60,int(fnum[i,3])/1e3))

