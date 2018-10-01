import random
import math

"""
    Make random initial state
"""
def initState(x,y, count):
    for i in range (0,count):
        x1 = random.randint(1,8)
        while x1 in x:
            x1 = random.randint(1,8)
        x.append(x1)
        y1 = random.randint(1,8)
        while y1 in y:
            y1 = random.randint(1,8)
        y.append(y1)
    points = []
    for i in range(0,count):
        point = []
        point.append(x[i])
        point.append(y[i])
        points.append(point)
    return points
    #print(x,y)``

"""
    Search one location
"""
def searchLocation(things, name, color, id, points):
    i = 0
    found = False
    while (i < len(things)) and (found == False):
        if (things[i][0] == color) and (things[i][1]== name) and (things[i][2] == id):
            found = True
        else:
            i += 1
    return points[i]
"""
    Search type location
"""
def searchTypeLocation(things, name, color, points):
    i = 0
    location = []
    while (i < len(things)):
        if (things[i][0] == color) and (things[i][1]== name):
            location.append(points[i])    
        i += 1
    return location

"""
    Check eats
"""
def eats(things, name, color, points):
    #location = searchLocation(things, name, color, id, points)
    location = searchTypeLocation(things, name, color, points)

    #use new variable
    count = 0
    count_kembar = 0
    for locate in location:
        points_no_me = points.copy()
        index = points.index(locate)
        #print(index)
        points_no_me.remove(locate)
        #print(points_no_me)
        me_x = locate[0]
        me_y = locate[1]
        i = 0
        for a in points_no_me:
            #jika i = index maka lompat 1
            if (i == index):
                i+=1
            xdif = abs(me_x - a[0])
            ydif = abs(me_y - a[1])
            #BILA POIN ADALAH QUEEN
            if (name == "QUEEN"):
                if (a[0] == me_x) or (a[1] == me_y) or (xdif == ydif):
                    #print(a)
                    if (things[i][1] == "QUEEN") and (things[i][0] == color):
                        count_kembar +=1
                    else:
                        count +=1
                    #print("Queen makan " + str(a))
            #BILA POIN ADALAH BISHOP
            elif (name == "BISHOP"):
                if (xdif == ydif):
                    if (things[i][1] == "BISHOP") and (things[i][0] == color):
                        count_kembar +=1
                    elif (things[i][1] != "QUEEN"):
                        count +=1
                    #print("Bishop makan " + str(a))
            #BILA POIN ADALAH ROOK
            elif (name == "ROOK"):
                if (a[0] == me_x) or (a[1] == me_y):
                    if (things[i][1] == "ROOK") and (things[i][0] == color):
                        count_kembar +=1
                    elif (things[i][1] != "QUEEN"):
                        count +=1
                    #print("Rook makan " + str(a))
            #BILA POIN ADALAH KNIGHT
            else: #name == "KNIGHT"
                if ((xdif == 2) and (ydif == 1)) or ((ydif == 2) and (xdif == 1)):
                    if (things[i][1] == "KNIGHT") and (things[i][0] == color):
                        count_kembar +=1
                    else:
                        count +=1
                    #print("Knight makan " + str(a))
            #increment untuk akses things
            i+=1
    return int(count + (count_kembar/2))
"""
    Count eaten all
"""
def eatenAll(things, points):
    count = 0
    i = 0
    while (i < len(things)):
        now_name = things[i][1]
        now_color = things[i][0]
        count += eats(things,now_name, now_color,points)
        while (i < len(things)) and (now_name == things[i][1]) and (now_color == things[i][0]):
            i +=1
    return count

"""
    Make input
"""
def makeInput():
    things = []
    thing_with_count = []
    for x in range (0,8):
        string = input()
        thing_with_count = string.split(" ")
        count = int(thing_with_count[2])
        thing = thing_with_count
        thing.remove(thing[2])
        for i in range (0,count):
            thing_with_id = []
            thing_with_id.append(thing[0])
            thing_with_id.append(thing[1])
            thing_with_id.append(i+1)
            things.append(thing_with_id)
    return things

"""
    Neighbor matrix
"""
def makeMatrix(things, points):
    row = []
    i_things = 0
    for a in points:
        column = []
        #i_things = searchColumn(points,i)
        ax = a[0]
        ay = a[1]
        for i in range(1,9):
            points_now = points.copy()
            point_rem = a
            points_now.remove(a)
            new_point = []
            new_point.append(ax)
            new_point.append(i)
            if not(checkOcc(points_now,new_point)):
                points_now.insert(i_things, new_point)
                #print(points_now)
                #print(eatenAll(things,points_now))
            else:
                points_now.insert(i_things, point_rem)
            column.append(eatenAll(things,points_now))
        #print(str(things[i_things][1]) + " : " + str(column))
        row.append(column)
        i_things +=1
    return row

"""
    search in column x
"""
def searchColumn(points,x):
    i = 0
    found = False
    while (i < len(points)) and not(found):
        if (points[i][0] == x):
            found = True
        else:
            i+=1
    return i


"""
    Print Matrix
"""
def printMatrix(things,matrix):
    i = 0
    for a in matrix:
        print(str(things[i][0]) + " " + str(things[i][1]) + " " + str(things[i][2]) + " : " + str(a))
        i += 1

"""
    Check if tile occupied
"""
def checkOcc(points, point):
    if point in points:
        return True
    else:
        return False

"""
    Find minimum
"""
def minimumCost(matrix):
    min = 999
    for x in matrix:
        for y in x:
            if y < min:
                min = y
    return min

"""
    Hill climbing
"""
def hillClimbing(things, points,matrix):
    i = 0
    min = minimumCost(matrix)
    found = False
    while (i < len(matrix)) and not(found):
        j = 0
        while (j < len(matrix[i])) and not(found):
            if (matrix[i][j] == min):
                found = True
            else:
                j += 1
        i += 1
    i -= 1
    #print(str(i) + " " + str(j))
    points_now = points.copy()
    a = points_now[i]
    ax = a[0]
    ay = a[1]
    points_now.remove(a)
    new_point = []
    new_point.append(ax)
    new_point.append(j+1)
    points_now.insert(i, new_point)
    #print(points_now)
    new_matrix = makeMatrix(things,points_now)
    #printMatrix(things, new_matrix)
    if (minimumCost(new_matrix) < min):
        hillClimbing(things, points_now, new_matrix)
    else:
        finalOutput(things,points_now)
        print(eatenAll(things, points_now), end =" ")
        print(0) #b = 0

"""
    Print final output
"""
def finalOutput(things,points):
    i = 8
    while (i >= 1):
        for j in range(1,9):
            new_point = [j,i]
            if new_point in points:
                thing = things[points.index(new_point)]
                if thing[0] == "WHITE":
                    if thing[1] == "KNIGHT":
                        print("K", end = " ")
                    elif thing[1] == "BISHOP":
                        print("B", end = " ")
                    elif thing[1] == "QUEEN":
                        print("Q", end = " ")
                    else: #ROOK
                        print("R", end = " ")
                else: #BLACK
                    if thing[1] == "KNIGHT":
                        print("k", end = " ")
                    elif thing[1] == "BISHOP":
                        print("b", end = " ")
                    elif thing[1] == "QUEEN":
                        print("q", end = " ")
                    else: #ROOK
                        print("r", end = " ")
            else:
                print(".", end = " ")
        i -=1
        print()
                    
things = makeInput()
#print(things)
x = []
y = []
points = initState(x,y, len(things))
#points = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8]]
#print(points)
eaten = eatenAll(things, points)
#print(eaten)
matrix = makeMatrix(things,points)
#printMatrix(things,matrix)
#print(minimumCost(matrix))
hillClimbing(things,points,matrix)




