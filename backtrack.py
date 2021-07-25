import copy

#Define domain
class Domain:
    def __init__(self, number_domain, color_domain):
        self.domains = [[] for i in range(number_domain)]
        for i in self.domains:
            for j in range(number_domain):
                color = copy.deepcopy(color_domain)
                i.append({"number": list(range(1, number_domain+1)), "color": color})

#Define table with n^2 elements
class Table:
    def __init__(self, table, length):
        self.table = table
        self.length = length


    #check completeness
    def is_complete(self):
        for row in self.table:
            for el in row:
                if el.color == "-" or el.number == 0:
                    return False
        return True

    #Check consistency , check kon rang ba olaviate balatar addade balatar
    def is_consistent(self, i, j, value, flag):
        global colors
        if flag == "color":
            #up
            if i - 1 >= 0:
                if self.table[i-1][j].color == value:
                    return False
            #down
            if i + 1 < self.length:
                if self.table[i + 1][j].color == value:
                    return False
            #left
            if j - 1 >= 0:
                if self.table[i][j-1].color == value:
                    return False
            #right
            if j + 1 < self.length:
                if self.table[i][j+1].color == value:
                    return False
        if flag == "number":
            #check the row
            for k in range(self.length):
                if k != j and self.table[i][k].number == value:
                    return False
            #check coloumn
            for k in range(self.length):
                if k != i and self.table[k][j].number == value:
                    return False
        #check the order of the color and number assigned to the element
        el = copy.deepcopy(self.table[i][j])
        if flag == "color":
            el.color = value
        else:
            el.number = value
        if el.is_assigned():
            #up
            if i-1 >= 0 and self.table[i-1][j].is_assigned():
                if colors.index(self.table[i-1][j].color) < colors.index(el.color) and self.table[i-1][j].number < el.number:
                    return False
                if colors.index(self.table[i-1][j].color) > colors.index(el.color) and self.table[i-1][j].number > el.number:
                    return False
            #down
            if i+1 < n and self.table[i+1][j].is_assigned():
                if colors.index(self.table[i+1][j].color) < colors.index(el.color) and self.table[i+1][j].number < el.number:
                    return False
                if colors.index(self.table[i+1][j].color) > colors.index(el.color) and self.table[i+1][j].number > el.number:
                    return False
            #left
            if j-1 >= 0 and self.table[i][j-1].is_assigned():
                if colors.index(self.table[i][j-1].color) < colors.index(el.color) and self.table[i][j-1].number < el.number:
                    return False
                if colors.index(self.table[i][j-1].color) > colors.index(el.color) and self.table[i][j-1].number > el.number:
                    return False
            #right
            if j+1 < n and self.table[i][j+1].is_assigned():
                if colors.index(self.table[i][j+1].color) < colors.index(el.color) and self.table[i][j+1].number < el.number:
                    return False
                if colors.index(self.table[i][j+1].color) > colors.index(el.color) and self.table[i][j+1].number > el.number:
                    return False
        return True



#No number assigned = 0, no color assigned = '-'
class Element:
    def __init__(self, number, color):
        self.number = int(number)
        self.color = color

    def is_assigned(self):
        if self.number == 0 or self.color == "-":
            return False
        return True
    def __str__(self):
        return str(self.number) + self.color

#mrv heuristic
def mrv(sodukuTable, domain):
    global m,n
    min = m + n
    pos = []
    for i in range(n):
        for j in range(n):
            if not sodukuTable.table[i][j].is_assigned():
                mylen = 0
                if sodukuTable.table[i][j].number != 0:
                    mylen += len(domain.domains[i][j]["color"])
                elif sodukuTable.table[i][j].color != "-":
                    mylen += len(domain.domains[i][j]["number"])
                else:
                    mylen += len(domain.domains[i][j]["color"]) + len(domain.domains[i][j]["number"])

                if mylen < min:
                    min = mylen
                    pos = [(i, j)]
                elif mylen == min:
                    pos.append((i,j))
    return pos

#degree Heuristic
def degree(sodukuTable, mrv_pos):
    global n
    mmax = -1
    for pos in mrv_pos:
        i, j = pos
        deg = 0
        if sodukuTable.table[i][j].color == "-":
            if i-1 >= 0 and sodukuTable.table[i-1][j].color == "-":
                deg += 1
            if i+1 < n and sodukuTable.table[i+1][j].color == "-":
                deg += 1
            if j-1 >= 0 and sodukuTable.table[i][j-1].color == "-":
                deg += 1
            if j+1 < n and sodukuTable.table[i][j+1].color == "-":
                deg += 1
        if sodukuTable.table[i][j].number == 0:
            #the row
            for k in range(n):
                if k != j and sodukuTable.table[i][k].number == 0:
                    deg += 1
                if k != i and sodukuTable.table[k][j].number == 0:
                    deg += 1
        if deg > mmax:
            mmax = deg
            x, y = i, j
    return x, y

#select unassigned variable based on MRV and degree hueristic
def select_var(sodukuTable, domain):
    pos = mrv(sodukuTable, domain)
    if len(pos) == 1:
        return pos[0]
    return degree(sodukuTable, pos)

#forward checking
def inference(sodukuTable, domain, i, j, value):
    global n
    inferenced_domain = copy.deepcopy(domain)
    if sodukuTable.table[i][j].number != 0:
        for k in range(n):
            if k != i and sodukuTable.table[i][j].number in inferenced_domain.domains[k][j]["number"]:
                inferenced_domain.domains[k][j]["number"].remove(sodukuTable.table[i][j].number)
            if k != j and sodukuTable.table[i][j].number in inferenced_domain.domains[i][k]["number"]:
                inferenced_domain.domains[i][k]["number"].remove(sodukuTable.table[i][j].number)
    if sodukuTable.table[i][j].color != "-":
        if i-1 >= 0 and sodukuTable.table[i][j].color in inferenced_domain.domains[i-1][j]["color"]:
            inferenced_domain.domains[i-1][j]["color"].remove(sodukuTable.table[i][j].color)

        if i+1 < n and sodukuTable.table[i][j].color in inferenced_domain.domains[i+1][j]["color"]:
            inferenced_domain.domains[i+1][j]["color"].remove(sodukuTable.table[i][j].color)

        if j-1 >= 0 and sodukuTable.table[i][j].color in inferenced_domain.domains[i][j-1]["color"]:
            inferenced_domain.domains[i][j-1]["color"].remove(sodukuTable.table[i][j].color)

        if j+1 < n and sodukuTable.table[i][j].color in inferenced_domain.domains[i][j+1]["color"]:
            inferenced_domain.domains[i][j+1]["color"].remove(sodukuTable.table[i][j].color)

    if sodukuTable.table[i][j].is_assigned():
        #up
        if i-1 >= 0 and not sodukuTable.table[i-1][j].is_assigned():
            if sodukuTable.table[i-1][j].color == "-" and sodukuTable.table[i-1][j].number != 0 and sodukuTable.table[i-1][j].number < sodukuTable.table[i][j].number:
                for k in inferenced_domain.domains[i - 1][j]["number"]:
                    if (k>sodukuTable.table[i][j].number):
                        inferenced_domain.domains[i - 1][j]["number"].remove(k)
            if sodukuTable.table[i-1][j].color != "-" and sodukuTable.table[i-1][j].number == 0 and colors.index(sodukuTable.table[i-1][j].color) > colors.index(sodukuTable.table[i][j].color):
                for k in inferenced_domain.domains[i-1][j]["color"]:
                    if(colors.index(k)<colors.index(sodukuTable.table[i-1][j].color)):
                        inferenced_domain.domains[i-1][j]["color"].remove(k)
        #down
        if i+1 < n and not sodukuTable.table[i+1][j].is_assigned():
            if sodukuTable.table[i+1][j].color == "-" and sodukuTable.table[i+1][j].number != 0 and sodukuTable.table[i+1][j].number < sodukuTable.table[i][j].number:
                for k in inferenced_domain.domains[i+1][j]["number"]:
                    if (k>sodukuTable.table[i][j].number):
                        inferenced_domain.domains[i+1][j]["number"].remove(k)
            if sodukuTable.table[i+1][j].color != "-" and sodukuTable.table[i+1][j].number == 0 and colors.index(sodukuTable.table[i+1][j].color) > colors.index(sodukuTable.table[i][j].color):

                for k in inferenced_domain.domains[i+1][j]["color"]:
                    if(colors.index(k)<colors.index(sodukuTable.table[i+1][j].color)):
                        inferenced_domain.domains[i+1][j]["color"].remove(k)
        #right
        if j+1 < n and not sodukuTable.table[i][j+1].is_assigned():
            if sodukuTable.table[i][j+1].color == "-" and sodukuTable.table[i][j+1].number != 0 and sodukuTable.table[i][j+1].number < sodukuTable.table[i][j].number:
                for k in inferenced_domain.domains[i][j+1]["number"]:
                    if (k>sodukuTable.table[i][j].number):
                        inferenced_domain.domains[i][j+1]["number"].remove(k)
            if sodukuTable.table[i][j+1].color != "-" and sodukuTable.table[i][j+1].number == 0 and colors.index(sodukuTable.table[i][j+1].color) > colors.index(sodukuTable.table[i][j].color):

                for k in inferenced_domain.domains[i][j+1]["color"]:
                    if(colors.index(k)<colors.index(sodukuTable.table[i][j+1].color)):
                        inferenced_domain.domains[i][j+1]["color"].remove(k)
        #left
        if j-1 >= 0 and not sodukuTable.table[i][j-1].is_assigned():
            if sodukuTable.table[i][j-1].color == "-" and sodukuTable.table[i][j-1].number != 0 and sodukuTable.table[i][j-1].number < sodukuTable.table[i][j].number:
                for k in inferenced_domain.domains[i][j-1]["number"]:
                    if (k>sodukuTable.table[i][j].number):
                        inferenced_domain.domains[i][j-1]["number"].remove(k)
            if sodukuTable.table[i][j-1].color != "-" and sodukuTable.table[i][j-1].number == 0 and colors.index(sodukuTable.table[i][j-1].color) > colors.index(sodukuTable.table[i][j].color):

                for k in inferenced_domain.domains[i][j-1]["color"]:
                    if(colors.index(k)<colors.index(sodukuTable.table[i][j-1].color)):
                        inferenced_domain.domains[i][j-1]["color"].remove(k)

    for l in inferenced_domain.domains:
        for h in l:
            if len(h["color"]) == 0 or len(h["number"]) == 0:
                return False
    return inferenced_domain

#Implement backtarck
def backtrack(sodukuTable, domain):
    if sodukuTable.is_complete():
        return sodukuTable
    i, j = select_var(sodukuTable, domain)
    if sodukuTable.table[i][j].color != "-":
        for k in domain.domains[i][j]["number"]:
            if sodukuTable.is_consistent(i, j, k, "number"):
                sodukuTable.table[i][j].number = k
                temp_domain = inference(sodukuTable, domain, i, j, k)
                if temp_domain:
                    result = backtrack(sodukuTable, temp_domain)
                    if result:
                        return result
                sodukuTable.table[i][j].number = 0
    else:
        for k in domain.domains[i][j]["color"]:
            if sodukuTable.is_consistent(i, j, k, "color"):
                sodukuTable.table[i][j].color = k
                temp_domain = inference(sodukuTable, domain, i, j, k)
                if temp_domain:
                    result = backtrack(sodukuTable, temp_domain)
                    if result:
                        return result
                sodukuTable.table[i][j].color = "-"

    return False




#Table dimensions and number of colors
m, n = input("").split(' ')
m, n = int(m), int(n)
#Colors and their order
colors = []
colors = input("").split(' ')

#Initial table
myinput = []
row = []
table_rows = []
for i in range(int(n)):
    myinput = input("").split(' ')
    for j in range(int(n)):
        if(myinput[j][0:len(myinput[j])-1] == "*" and myinput[j][-1] == "#"):
            el = Element(0, "-")
        elif myinput[j][0:len(myinput[j])-1] == "*" and myinput[j][-1] != "#":
            el = Element(0, myinput[j][-1])
        elif myinput[j][0:0:len(myinput[j])-1] != "*" and myinput[j][-1] == "#":
            el = Element(myinput[j][0:len(myinput[j])-1], "-")
        else:
            el = Element(myinput[j][0:len(myinput[j])-1], myinput[j][-1])
        row.append(el)
    table_rows.append(row)
    row = []

sodukuTable = Table(table_rows, n)
myDomain = Domain(n, colors)

#Define initial domain based on initial table
for i in range(n):
    for j in range(n):
        if(sodukuTable.table[i][j].color!="-"):
            myDomain.domains[i][j]["color"]=[sodukuTable.table[i][j].color]
        if(sodukuTable.table[i][j].number!=0):
            myDomain.domains[i][j]["number"]=[sodukuTable.table[i][j].number]
#
# for i in myDomain.domains:
#     print(i)

res = backtrack(sodukuTable, myDomain)

if res == False:
    print("No Answer")
else:
    for row in res.table:
        for el in row:
            print(el,end=" ")
        print("")