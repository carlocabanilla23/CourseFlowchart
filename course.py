class Course:
    code = ""
    name = ""
    credit = 0
    availability = []
    prerequisites = []
    
    
    def __init__(self,obj):
        info = obj.strip().split(',')
        # Extract the course code, name, credits, requirements, and quarters
        # from the list of strings
        # print(info) 
        if (len(info) != 5):
            print("Error in parsing the data !!")
            print("Try to run the program again....")
            exit()
        self.code = info[0].strip()
        self.name = info[1].strip()
        self.credit = int(info[2].strip())
        self.prerequisites = info[3].strip()
        self.prerequisites = self.prerequisites.split(' ') if self.prerequisites else []
        self.availability = [int(x) for x in info[4].strip().split()]
        
        delim = ['AND']
        requirements = []
        row = []
        req = self.prerequisites
        
        
        for r in req:
            if (r != "OR"):
                row.append(r)
            else:
                for d in delim:
                    if d in row:
                        count = row.count(d)
                        for i in range(0,count):
                            row.remove(d)
                # print(row)

                requirements.append(row)
                row = []
        
        for d in delim:
                    if d in row:
                        count = row.count(d)
                        for i in range(0,count):
                            row.remove(d)
        requirements.append(row)
        row = []
        
        req = requirements
        
        temp = []
        for reqs in req:
            # print(req)
            tmp = []
            andTmp = []
            if (len(reqs) != 0):
                for rq in reqs:
                    tmp.append(rq)
                    if (len(tmp) == 2):
                        andTmp.append(self.MergeArray(tmp))
                        tmp = []
                # print(andTmp)
                temp.append(andTmp)
                andTmp = []        
                # print(reqs)
                
        
        # print(temp)
        self.prerequisites = temp
    
        # print(self.prerequisites)

    def Print(self):
        print(str(self.code) + " " , end="")
        print(str(self.name) + ", " , end="")
        print(str(self.credit) + " " , end="")
        print(str(self.availability) + " " , end="")
        print(str(self.prerequisites) + " " , end="")
        print()
        # print(prerequisites)
        # Store the course information in the dictionary
        # courses = {'code':code,'name': name, 'credits': credits, 'reqs': reqs.split(' ') if reqs else [], 'quarters': quarters}
        # print(courses[code])
    def PrintTable(self):
        print(str(self.code) + "     " , end="")
        print(str(self.credit) + "     " , end="")
        print(self.prerequisites)
    
    def MergeArray(self,arr):
        return ' '.join(arr)
    
    def RemoveRequirement(self,course):
        # print(self.code)
        rlen = len(self.prerequisites)
        if (rlen == 0):
            return
        i = 0
        # print(self.prerequisites)
        # print(len(self.prerequisites))
        if (rlen > 0):
            while(i < rlen):
                # print(self.prerequisites[i])
                if (len(self.prerequisites[i]) == 1):
                    if (self.prerequisites[i][0] == course):
                        # print("asdasdadad")
                        self.prerequisites = []
                        return
                else:
                    for req in self.prerequisites[i]:
                        if (req == course):
                            # print("founditt")
                            self.prerequisites[i].remove(course)

                i = i + 1
