
@@ -0,0 +1,70 @@
import time
Inf=9999999


class Dijkstra:
    def __init__(self,filename):
        f=open(filename).read().split()
        src=[]
        for i in f:
            src.append(int(i))
        self.vernum=src[0]
        self.edgenum=src[1]
        self.arc=[[Inf for i in range(self.vernum)]for j in range(self.vernum)]
        for i in range(self.vernum):
            self.arc[i][i]=0
        for i in range(2,len(src),3):
            self.arc[src[i] - 1][src[i + 1] - 1] = src[i + 2]
            self.arc[src[i + 1] - 1][src[i] - 1] = src[i + 2]     #无向图
        self.visited=[0 for i in range(self.vernum)]
        self.value=[Inf for i in range(self.vernum)]
        self.path=["" for i in range(self.vernum)]

    def Show_M(self):
        print("Vernum: ",self.vernum,"Edgenum: ",self.edgenum)
        for i in self.arc:
            for j in i:
                if (j == Inf):
                    print("{:>4}".format("∞"), end=" ")
                else:
                    print("{:>4}".format(j), end=" ")
            print()

    def Show_Path(self,end=0):
        print("{:<120}".format(self.path[end-1]), self.value[end-1] if self.value[end-1] != Inf else "No Path!")

    def Show_Path_All(self):
        for i in range(self.vernum):
            print("{:<120}".format(self.path[i]),self.value[i] if self.value[i]!=Inf else "No Path!")

    def Dijkstra(self,begin=1):
        for i in range(self.vernum):
            self.visited[i] = 0
            self.value[i]=self.arc[begin-1][i]
            self.path[i]="V"+str(begin)+"-->V"+str(i+1)
        self.visited[begin-1]=1
        self.value[begin-1]=0
        temp=0
        min=Inf
        for i in range(self.vernum):
            min=Inf
            temp=0
            for j in range(self.vernum):
                if(not self.visited[j] and self.value[j]<min):
                    min=self.value[j]
                    temp=j
            self.visited[temp]=1
            for j in range(self.vernum):
                if((not self.visited[j]) and self.arc[temp][j]!=Inf and (self.arc[temp][j]+self.value[temp]<self.value[j])):
                    self.value[j]=self.arc[temp][j]+self.value[temp]
                    self.path[j]=self.path[temp]+"-->V"+str(j+1)


start=time.time()
M=Dijkstra("test.txt")
#M.Show_M()
M.Dijkstra(1760)
M.Show_Path(669)
#M.Show_Path_All()
end=time.time()
print(end-start," s")
