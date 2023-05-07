class ListGraph:
    graph = []
    size = 0
    node = []
    
    def __init__(self,elements):
        self.size = len(elements)
        self.node = elements
        for i in elements:
            node = [i]
            row = []
            row.append(node)
            self.graph.append(row)
          
        
    def Print(self):
        for v in self.graph:
            print(v) 
    def PrintTimeline(self):
        for rows in self.graph:
            code = rows[0][0]
            space = ""
            level = int(code[4])
            if (level == 4):
                for i in range(0,90):
                    space = space + " "
                print(space,end="")
                print(rows)
            if (level == 3):
                for i in range(0,60):
                    space = space + " "
                print(space,end="")
                print(rows)
            if (level == 2):
                for i in range(0,30):
                    space = space + " "
                print(space,end="")
                print(rows)
            if (level == 1):
                print(space,end="")
                print(rows)
                
    def AddVertex(self,n):
        node = [n]
        row = [node]
        self.graph.append(row)
        self.node.append(n)
        self.size = self.size + 1
    
    def AddEdge(self,a,b):
        vPos = self.node.index(a)
        row = [b,1]
        self.graph[vPos].append(row)

    def IsConnected(self,a,b):
        vPos = self.node.index(a)
        row = [b,1]
        lineRow = self.graph[vPos]
        for l in lineRow:
            if (l == row):
                return True
        return False

    def AddWeigthedVertex(self,a,b,w):
        vPos = self.node.index(a)
        row = [b,w]
        self.graph[vPos].append(row)
    
    def CreateBoolTable(self,size):
        boolTable = []

        for i in range(0,size-1):
            boolTable.append(False)
        
        return boolTable
    
    def AddBiconnectedEdge(self,a,b):
        vPosA = self.node.index(a)
        vPosB = self.node.index(b)
        rowA = [a,1]
        rowB = [b,1]
        self.graph[vPosA].append(rowB)
        self.graph[vPosB].append(rowA)

    def BFS(self,n):
        print(n)
        queue = []
        L = []
        isVisited = self.CreateBoolTable(self.size)

        queue.append(n)

        pos = self.node.index(n)

        isVisited[pos] = True

        while (len(queue) > 0):
            v = queue.pop()
            x = self.node.index(v)
            isVisited[x] = True
            l =  len(self.graph[x])
            for n in self.graph[x]:
                    pos = self.node.index(n[0])
                    if (isVisited[pos] == False):
                        L.append([v,self.node[pos]])
                        print(self.node[pos])
                        queue.append(self.node[pos])
                        isVisited[pos] = True

        return L
    
    def DFS(self,n):
        print(n)
        queue = []
        L = []
        isVisited = self.CreateBoolTable(self.size)

        queue.append(n)

        pos = self.node.index(n)

        isVisited[pos] = True

        while (len(queue) > 0):
            v = queue.pop(0)
            x = self.node.index(v) + 1

            l =  len(self.node) + 1

            for n in self.graph[x]:
                    pos = self.node.index(n[0])
                    if (isVisited[pos] == False):
                        L.append([v,self.node[pos]])
                        print(self.node[pos])
                        queue.append(self.node[pos])
                        isVisited[pos] = True

        return L
    
    def FindVertex(self,n):
        pos = self.node.index(n)
        row = self.graph[pos]
        row = row[1:]
        L = []

        for r in row:
            L.append(r[0])

        return L

    def RemoveEdge(self,a,b):
        p1 = self.node.index(a)
        row = self.graph[p1]
        for i in range(1,len(row)):
            if row[i][0] == b:
                self.graph[p1].pop(i)

    def FindPath(self,a,b):
        isVisited = self.CreateBoolTable(self.size)
        # Create a stack
        stack = []
        # Push a into the stack
        stack.append(a)
        # mark a as visited
        while (len(stack) >= 0):
            head = stack[0]
            if (head == b):
                result = []
                for s in stack:
                    sidx = self.node.index(s)   
                    if (isVisited[sidx] == True):
                        result.append(s)
                result.insert(0,b)
                result.reverse()
                return result
            idx = self.node.index(head)
            isVisited[idx] = True
        # look for all the neighbors of a that is not visited
            neighbor = self.FindVertex(head)
            tmpNeighbor = []
            for n in neighbor:
                nidx = self.node.index(n)
                if (isVisited[nidx] == False):
                    tmpNeighbor.append(n)
            neighbor = tmpNeighbor
        # If there is a has no neighbor pop until we reach the head of the stack that is still not visible
            if (len(neighbor) == 0):
                while(isVisited[self.node.index(stack[0])] == True):
                    stack.pop(0)
        # Else push all the neighbors of a into the stack
            else:
                for v in neighbor:
                    stack.insert(0,v)

        return stack

    def FindWeight(self,a,b):
        p1 = self.node.index(a)
        row = self.graph[p1]
        for r in row:
            if r[0] == b:
               return r[1]
        return -1 
# Dijkstra 
    def Dijkstra(self,s,t):
        Neighbor = self.FindVertex(s)
        S = []
        D = [-1]*self.size
        D[self.node.index(s)] = 0
        for n in Neighbor:
            v = self.node.index(n)
            D[v] = int(self.FindWeight(s,n))
        S.append(s)

        while ((len(self.node) - len(S)) != 0):
            VS = []
            for n in self.node:
                if n not in S:
                    VS.append(n)

            curr = -1
            npos = -1
            for vs in VS:
                i = self.node.index(vs)
        
                if (curr == -1):
                    if (D[i] == -1):
                        curr = curr
                        npos = npos
                    else:
                        curr = D[i]
                        npos = i
                else:
                    if (D[i] == -1):
                        curr = curr
                        npos = npos
                    elif (D[i] < curr):
                        curr = D[i]
                        npos = i
            u = self.node[npos]
            
            S.append(u)
            UV = self.FindVertex(u)
            for v in UV:
                vi = self.node.index(v)
                ui = self.node.index(u)
                if ( (D[vi] > D[ui] + int(self.FindWeight(u,v))) or (D[vi] == -1) ):
                    D[vi] = D[ui] + int(self.FindWeight(u,v))
        D.sort()
        D.reverse()
        return D[0]