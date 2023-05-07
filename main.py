#Import essential library
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation
import course as c
import list_graph as graph
import os.path

# Create a directed graph
G = nx.DiGraph()
F = nx.DiGraph()

 #Read course information from the file and return a list of Course objects.
def read_course_info(file_name):
    # Validate the file if exists
    if (os.path.exists(file_name) == False):
        print("File does not exist. Please Try again")
        exit()
    # Initialize an empty dictionary to store the course information
    course_list = []
    # Open the file in read mode
    with open(file_name, 'r') as file:
        # For each line in the file
        for line in file:
            course_list.append(c.Course(line))
    return course_list

#Request the user to input the maximum number of credits per quarter and the starting quarter.
def request_user_input():
    max_credits = int(input("Enter the maximum number of credits per quarter (Minimum is 8): "))
    starting_quarter = int(input("Enter the starting quarter (1 for fall, 2 for winter, 3 for spring): "))
    return max_credits, starting_quarter

#Draw the graph using networkx and matplotlib.
def draw_graph(program):
    for layer, nodes in enumerate(nx.topological_generations(G)):
    # `multipartite_layout` expects the layer as a node attribute, so add the
    # numeric layer value as a node attribute
        for node in nodes:
            G.nodes[node]["layer"] = layer

    # Compute the multipartite_layout using the "layer" node attribute
    pos = nx.multipartite_layout(G, subset_key="layer")

    fig, ax = plt.subplots()
    ax.set_title(str(program) + " Academic Program")

    def init():
        return []
    def update(frame):
        if frame < len(G.nodes):
            node = list(G.nodes)[frame]
            nx.draw_networkx_nodes(G, pos, nodelist=[node], ax=ax, node_size=1300, node_shape="s")
            nx.draw_networkx_labels(G, pos, labels={node: node}, font_size=6)
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v in G.edges if u == node or v == node], ax=ax,
                                    arrows=True, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.2')
        return []

    animate = FuncAnimation(fig, update, frames=range(len(G.nodes) + 1), init_func=init, blit=True, interval=500)
    plt.show()

    
#Create edges between courses and their prerequisites in the graph.
def create_edge_for_graph_viz(program,courses):
    # Loop over each course in the courses list
    for course in courses:
        # If the course has prerequisites
        if (len(course.prerequisites) > 0):
            # Loop over each prerequisite in the prerequisite list
            for req in course.prerequisites:
                if(len(req)> 1):
                    for r in req:
                        G.add_edge(r, course.code)
                else:
                    G.add_edge(req[0], course.code)
                # Add an edge from the prerequisite to the course          
    draw_graph(program)
    
#indexOf - helper function
def indexOf(n,courses):
    for c in courses:
        if (n==c):
            return 1
    return -1
#indexOfList - helper function
def indexOfList(n,courses):
    for c in courses:
        for cc in c:
            if (n==c.code):
                return 1
    return -1

#Check if a course is in the course list
def Check(code,courses):
    for c in courses:
        if (c == code):
            return 1
    return -1

#Get a list of all unique course codes
def get_all_courses(courses):
    arr = []
    for c in courses:
        if (indexOf(c.code,arr) == -1):
            arr.append(c.code)
        for cr in c.prerequisites:
             if (indexOf(cr,arr) == -1):
                arr.append(cr)
    return arr
    
#Create a local graph based on the course elements and their prerequisites.
def create_local_graph(elements,courses):
    local_graph = graph.ListGraph(elements)
    for course in courses:
        if (len(course.prerequisites) > 0):
            for r in course.prerequisites:
                if not local_graph.IsConnected(r, course.code):
                    local_graph.AddEdge(r, course.code)
                    
# Create a mapping from quarter number to color
def course_quarter_color(course_code, course_plan):
    color_map = {
        0: "green",   # Fall
        1: "blue",    # Winter
        2: "yellow",  # Spring
        3: "red"      # Summer
    }

    for i, quarter in enumerate(course_plan):
        for course in quarter:
            if course.code == course_code:
                return color_map[i % 4]

    return "gray"

#major algortihm function for text and graph representation
def create_course_plan(program,courses,max_credits,starting_quarter):
    noreq = []
    tmpCourses = courses
    courseReq = []
    course_plan = []
    quarter = []
    curr_credit = 0
    curr_qtr = 1
    y_pos = 5
    x_pos = 1
    cq = starting_quarter
    nodelist = []
    nodelistXPos = []

    for tm in tmpCourses:
        courseReq.append([tm.code,tm.prerequisites])            
    while (cq != curr_qtr):
        course_plan.append([])
        curr_qtr += 1

    print()
    print("Program Name: " + str(program))
    print("Start Quarter: " + str(curr_qtr))
    print("Credit per quarter: " + str(max_credits))
    print()

    while len(tmpCourses) > 0:
        for ti in range(0,len(tmpCourses)):
            for tj in range(0,len(tmpCourses)):
                if (len(tmpCourses[ti].code)== 9):
                    crs_lvl_idx = 5
                else:
                    crs_lvl_idx = 4
                if (len(tmpCourses[tj].code)== 9):
                    crs_lvl_jdx = 5
                else:
                    crs_lvl_jdx = 4
                if (int(tmpCourses[ti].code[crs_lvl_idx]) < int(tmpCourses[tj].code[crs_lvl_jdx])):
                    tmp = tmpCourses[ti]
                    tmpCourses[ti] = tmpCourses[tj]
                    tmpCourses[tj] = tmp
                            
        for c in tmpCourses:
            if (tmpCourses.index(c) == len(tmpCourses)-1):
                course_plan.append(quarter)
                curr_credit = 0
                quarter = []
                curr_qtr += 1
                y_pos = 5
                x_pos = x_pos + 0.25
                if curr_qtr == 5:
                    curr_qtr = 1
                    y_pos = 5
            
            if curr_credit + c.credit > max_credits:
                course_plan.append(quarter)
                curr_credit = 0
                quarter = []
                curr_qtr += 1
                y_pos = 5
                x_pos = x_pos + 0.25
                if curr_qtr == 5:
                    curr_qtr = 1
                    y_pos = 5
                break

            else:
                rlen = len(c.prerequisites)
                if rlen == 0:
                    curr_credit += c.credit
                    if curr_qtr in c.availability:
                        quarter.append(c)
                        noreq.append(c)
                        
                        if (len(course_plan)==0):
                            F.add_node(c.code,pos=(x_pos,y_pos))
                            nodelist.append(c.code)
                            nodelistXPos.append(x_pos)
                    
                            # Add an edge from the prerequisite to the course   
                            y_pos = y_pos + 1000
                        else:
                            if (Check(c.code,course_plan) == -1):
                                F.add_node(c.code,pos=(x_pos,y_pos))
                                nodelist.append(c.code)
                                nodelistXPos.append(x_pos)
                                y_pos = y_pos + 1000
                     
                        tmpCourses.remove(c)
                        
                        for tmpcourse in tmpCourses:
                            tmpcourse.RemoveRequirement(c.code)

    for course in courseReq:
        # If the course has prerequisites
        if (len(course[1]) > 0):
            # Loop over each prerequisite in the prerequisite list
            for req in course[1]:
                if(len(req)> 1):
                    for r in req:
                        if (Check(r,nodelist) == 1):
                            posR = nodelist.index(r)
                            posCourse = nodelist.index(course[0])
                            if (nodelistXPos[posR] < nodelistXPos[posCourse]):
                               F.add_edge(r, course[0])
                else:
                    if (Check(req[0],nodelist) == 1):
                        posR = nodelist.index(req[0])
                        posCourse = nodelist.index(course[0])
                        if (nodelistXPos[posR] < nodelistXPos[posCourse]):
                            F.add_edge(req[0], course[0])    
    
    curr_qtr = 0 
    year = 1
    x_coor = []
    y_coor = []
    counter = 5
    course_lst_label = []

    year_labels = {1: "Freshman Year", 
                2: "Sophomore Year", 
                3: "Junior Year", 
                4: "Senior Year",
                5: "5th Year"}

    for cp in course_plan:
        quarter_credits = 0
        
        for qt in cp:
            quarter_credits += qt.credit
        
        if (curr_qtr == 0):
            if int(year) in year_labels:
                print(year_labels[int(year)])
            print()
            print("Fall (Total credits: " + str(quarter_credits) + ")")
            year += 0.25
        elif (curr_qtr == 1):
            print("Winter (Total credits: " + str(quarter_credits) + ")")
            year += 0.25
        elif (curr_qtr == 2):
            print("Spring (Total credits: " + str(quarter_credits) + ")")
            year += 0.25
        elif (curr_qtr == 3):
            print("Summer (Total credits: " + str(quarter_credits) + ")")
            year += 0.25
            
        for qt in cp:
            course_info = f"{qt.code} ({qt.credit} credits)"
            print(course_info)
            course_lst_label.append(qt.code)
            x_coor.append(year)
            y_coor.append(counter)
            counter = counter + 5
        print()
        curr_qtr = curr_qtr + 1
        if (curr_qtr == 4):
            curr_qtr = 0
            year += 0.25
            counter = 5
    
    node_colors = [course_quarter_color(course_code, course_plan) for course_code in F.nodes]
    pos = nx.get_node_attributes(F,'pos')
    nx.draw_networkx(F,pos=pos,font_size=6,node_size = 1300, node_shape ="s", node_color=node_colors)
    ax = plt.gca()
    
    x_labels = ['Freshman', 'Sophomore', 'Junior', 'Senior', '5th Year']
    x_positions = [1.25, 2.25, 3.25, 4.25, 5.25]
    y_position = 2200
    for x_pos, label in zip(x_positions, x_labels):
        ax.text(x_pos, y_position, label, horizontalalignment='center')
        
    custom_lines = [Line2D([0], [0], color='green', lw=4),
                Line2D([0], [0], color='blue', lw=4),
                Line2D([0], [0], color='yellow', lw=4),
                Line2D([0], [0], color='red', lw=4)]
    ax.legend(custom_lines, ['Fall', 'Winter', 'Spring', 'Summer'])

    plt.axis('off')
    plt.title(str(program) + " Program Academic Plan")
    
    plt.show() 

#This is the main function that is called when the program is run. 
def main(): 
    
    #Request input from user
    program = input("Please enter the name of your academic program: ")
    file = input("Please enter your file name - end with .txt: ")
    courses = read_course_info(file)
    data = get_all_courses(courses)
    create_local_graph(data,courses)
    runOption = True
    
    #Output a simple menu
    print("Please select from the following menu")
    print("1 - Print course plan without constraint (15 credits starting fall quarter)")
    print("2 - Print course plan with constraint (input the number of credits and start quarter)")
    print("3 - Print the animation program workflow (Directed Graph Representaion)")
    
    while (runOption == True):
        choice = input("Enter Your Choice: ")
        if (choice == "1"):
            create_course_plan(program,courses,15,1)
            runOption = False
        elif (choice == "2"):
            Choice2Option = True
            while (Choice2Option == True):
                max_credits, starting_quarter = request_user_input()
                if (max_credits < 8):
                    print("Please enter a max credit higher than 7")
                elif ((starting_quarter > 4) or (starting_quarter <= 0)):
                    print("Please enter a starting quarter from 1-4")
                else:
                    create_course_plan(program,courses,max_credits,starting_quarter)
                    Choice2Option = False
            runOption = False
        elif (choice == "3"):
            create_edge_for_graph_viz(program,courses)
            runOption = False
        else:
            print("You selected a wrong option. Please try Again")
            
if __name__=="__main__":
    main()