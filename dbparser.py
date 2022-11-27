import sys

fileLines = []
currentPath = []
lineCounter = 0
usedVariables = []

def handleType(typename):
    if (typename.find("Array") != -1):
        return arrayify(typename)
    elif (typename.find("Struct") != -1):
        return structify()
    elif (typename.find("String") != -1):
        return stringify()
    elif (typename.find("Int") != -1):
        return intify()
    elif (typename.find("Bool") != -1):
        return boolify()
    else:
        raise Exception("Type" + typename + "not supported yet")
    

def getType(line):
    return line.rsplit(":")[1].strip()

def getVarname(line):  
    return line.rsplit(":")[0].strip()

def arrayify(typename):
    global currentPath
    global lineCounter
    sRet = ""
    nRangeBegin = typename.find('[')+1
    nRagneEnd = typename.find(']')
    begin, end = typename[nRangeBegin:nRagneEnd].split("..")
    begin = int(begin)
    end = int(end)
    if (begin != 0):
        raise Exception("Array index not starting from 0 is not supported")

    arrayType = typename.split("of")[1].strip()

    sRet += "[\n"
    
    lineCounterBegin = lineCounter
    currentPathLast = currentPath[-1]
    for i in range(0, end+1):
        lineCounter = lineCounterBegin  # reset line counter for every iteration so structs will get created correctly
        currentPath[-1] = currentPath[-1] + "["+str(i)+"]"
        sRet += indent()
        sRet += handleType(arrayType)
        sRet += ",\n"
        currentPath[-1] = currentPathLast

    sRet = sRet[:-2]    # Remove \n and ,
    sRet += "\n" # add \n back
    sRet += indent()
    sRet += "]"
    return sRet


def structify():
    sRet = "{\n"
    currentLine = getNextLine()

    while (currentLine.find("END_STRUCT") == -1 and currentLine.find("END_VAR") == -1 ):
        if (currentLine):   # Line not empty
            currentPath.append(getVarname(currentLine))
            sRet += indent()
            sRet += "\""
            sRet += getVarname(currentLine)
            sRet += "\":"
            sRet +=  handleType(getType(currentLine))
            sRet += ",\n"
            currentPath.pop()
        currentLine = getNextLine()
    sRet = sRet[:-2]    # Remove \n and ,
    sRet += "\n" # add \n back
    sRet += indent()
    sRet += "}"
    return sRet

def stringify():
    sRet = "\"" + getCurrentPath() + "\""
    return sRet

def boolify():
    return getCurrentPath()

def intify():
    return boolify()   # same atm

def getCurrentPath():
    strPath = ""
    for s in currentPath:
        strPath += s
        strPath += '.'
    strPath = strPath[:-1]
    pushBackVariable(strPath)
    strPath = " "+(':='+strPath.strip()+':').replace(" ", "")
    return strPath

def getPathLen():
    return len(currentPath)

def indent():
    sRet = ""
    for _ in range(0, getPathLen() -1):
        sRet += "\t"
    return sRet


def getNextLine():
    global lineCounter
    nextLine = fileLines[lineCounter]
    lineCounter += 1
    return nextLine

def pushBackVariable(varname):
    usedVariables.append(varname)
    

with open(sys.argv[1]) as file: # open(stdin)
    fileLines = [line.rstrip() for line in file]

dataBlockName = getNextLine()

if (dataBlockName.find("DATA_BLOCK") == -1):
    raise Exception("DATA_BLOCK property not found")

dataBlockName = dataBlockName.split("DATA_BLOCK")[-1]
#print(dataBlockName, end =' ')

currentPath.append(dataBlockName)

currentLine = getNextLine()
while (currentLine.find("VAR") == -1):
    currentLine = getNextLine()

j = structify()

outstr = ""

for var in usedVariables:
    outstr += "<!-- AWP_In_Variable " + ("Name='"+var.strip()).replace(" ", "") +"' -->"

outstr += j

f = open(sys.argv[2], "w")
f.write(outstr)
f.close()
    