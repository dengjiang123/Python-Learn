import os
import linecache

allfile=[]
os.system("dir /a /b *.txt>all.txt")
f=open("all.txt","r")
x=f.readline().strip('\n')
while(x):
    if(x=="all.txt" or not x):
        pass
    else:
        allfile.append(x)
    x = f.readline().strip('\n')
f.close()

def judge(line):
    all=line.split()
    if(int(all[7])==0 or int(all[7])==32700 or int(all[8])==0 or int(all[8])==32700 or int(all[9])==0 or int(all[9])==32700):
        return 0
    return 1

for i in allfile:
    f=open(i,'r')
    f1=open("new/"+i,'w')
    line=f.readline().strip("\n")
    while(line):
        if(judge(line)):
            f1.write(str(line))
            f1.write("\n")
        line=f.readline().strip("\n")
    f.close()
    f1.close()
