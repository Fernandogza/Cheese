import sys
import shlex
from turtle import *

#Writer = Screen()
#Writer.setup(400,200)
cheese = Turtle()
screen = cheese.getscreen()
cheese.pendown()
screen.colormode(255)

instructionMemory = []
jumpStack = []
stackPointer = 0
segmentLength = 7050
inferiorLimit = 10000
returnStack = []

passingParameters = False
passingArray = 0
globalMemory = list(range(0, 10050))
methodsMemory = list(range(0,7050600))
memoryMap = [globalMemory, methodsMemory]

PC = 0

def EQU(op1, op2, result):
    if result >= inferiorLimit:
        # if passingParameters:
        #     result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
        # else:
        result = (result-inferiorLimit) + segmentLength*stackPointer
        methodsMemory[result] = op1
    elif result < inferiorLimit:
        globalMemory[result] = op1
    print ("RESULT_MOD: ", result)

def SUM(op1, op2, result):
    op2 = int(op2)
    op1 = int(op1)
    try:
        if result >= inferiorLimit:
            if passingParameters:
                result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
            else:
                result = (result-inferiorLimit) + segmentLength*stackPointer;
            if op2 < inferiorLimit:
                methodsMemory[result] = op1 + globalMemory[(op2 - inferiorLimit) + segmentLength*(stackPointer)]
            else:
                methodsMemory[result] = op1 + methodsMemory[(op2 - inferiorLimit) + segmentLength*(stackPointer)]
        elif result < inferiorLimit:
            if op2 < inferiorLimit:
                methodsMemory[result] = op1 + globalMemory[(op2 - inferiorLimit) + segmentLength*(stackPointer)]
            else:
                methodsMemory[result] = op1 + methodsMemory[(op2 - inferiorLimit) + segmentLength*(stackPointer)]
    except:
        raise TypeError("Operation invalid for specified operand types")

def VER(op1, op2, result):
    if op1 >= op2:
        print('ERROR: Index out of bounds, cannot access index {} of an array of size {}'.format(op1, op2))
        raise SystemExit
    else:
        if result < inferiorLimit:
            for i in range(0, op2):
                globalMemory[i+result] = 0
        else:
            for i in range(0, op2):
                methodsMemory[i+result] = 0

#   BEGIN ARITHMETIC OPERATIONS
def ADD(op1, op2, result):
    global passingArray
    try:
        if result >= inferiorLimit:
            if passingParameters:
                result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
            else:
                result = (result-inferiorLimit) + segmentLength*stackPointer;
            if passingArray == 1:
                if op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] + op2
                else:
                    print('MEM: ', methodsMemory[op1])
                    methodsMemory[result] = methodsMemory[op1] + op2
            elif passingArray == 2:
                if op2 < inferiorLimit:
                    methodsMemory[result] = op1 + globalMemory[op2]
                else:
                    methodsMemory[result] = op1 + methodsMemory[op2]
            elif passingArray == 3:
                if op1 < inferiorLimit and op2 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] + globalMemory[op2]
                elif op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] + methodsMemory[op2]
                elif op2 < inferiorLimit:
                    methodsMemory[result] = methodsMemory[op1] + globalMemory[op2]
                else:
                    methodsMemory[result] = methodsMemory[op1] + methodsMemory[op2]
            else:
                methodsMemory[result] = op1 + op2
        elif result < inferiorLimit:
            if passingArray == 1:
                if op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] + op2
                else:
                    methodsMemory[result] = methodsMemory[op1] + op2
            elif passingArray == 2:
                if op2 < inferiorLimit:
                    methodsMemory[result] = op1 + globalMemory[op2]
                else:
                    methodsMemory[result] = op1 + methodsMemory[op2]
            elif passingArray == 3:
                if op1 < inferiorLimit and op2 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] + globalMemory[op2]
                elif op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] + methodsMemory[op2]
                elif op2 < inferiorLimit:
                    methodsMemory[result] = methodsMemory[op1] + globalMemory[op2]
                else:
                    methodsMemory[result] = methodsMemory[op1] + methodsMemory[op2]
            else:
                methodsMemory[result] = op1 + op2
    except:
        try:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = str(op1) + str(op2)
            elif result < inferiorLimit:
                globalMemory[result] = str(op1) + str(op2)
        except:
            raise TypeError("Operation invalid for specified operand types")
    passingArray = 0

def SUB(op1, op2, result):
    global passingArray
    try:
        if result >= inferiorLimit:
            if passingParameters:
                result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
            else:
                result = (result-inferiorLimit) + segmentLength*stackPointer;
            if passingArray == 1:
                if op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] - op2
                else:
                    print('MEM: ', methodsMemory[op1])
                    methodsMemory[result] = methodsMemory[op1] - op2
            elif passingArray == 2:
                if op2 < inferiorLimit:
                    methodsMemory[result] = op1 - globalMemory[op2]
                else:
                    methodsMemory[result] = op1 - methodsMemory[op2]
            elif passingArray == 3:
                if op1 < inferiorLimit and op2 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] - globalMemory[op2]
                elif op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] - methodsMemory[op2]
                elif op2 < inferiorLimit:
                    methodsMemory[result] = methodsMemory[op1] - globalMemory[op2]
                else:
                    methodsMemory[result] = methodsMemory[op1] - methodsMemory[op2]
            else:
                methodsMemory[result] = op1 - op2
        elif result < inferiorLimit:
            if passingArray == 1:
                if op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] - op2
                else:
                    print('MEM: ', methodsMemory[op1])
                    methodsMemory[result] = methodsMemory[op1] - op2
            elif passingArray == 2:
                if op2 < inferiorLimit:
                    methodsMemory[result] = op1 - globalMemory[op2]
                else:
                    methodsMemory[result] = op1 - methodsMemory[op2]
            elif passingArray == 3:
                if op1 < inferiorLimit and op2 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] - globalMemory[op2]
                elif op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] - methodsMemory[op2]
                elif op2 < inferiorLimit:
                    methodsMemory[result] = methodsMemory[op1] - globalMemory[op2]
                else:
                    methodsMemory[result] = methodsMemory[op1] - methodsMemory[op2]
            else:
                methodsMemory[result] = op1 - op2
    except:
        raise TypeError("Operation invalid for specified operand types")
    passingArray = 0

def MUL(op1, op2, result):
    global passingArray
    try:
        if result >= inferiorLimit:
            if passingParameters:
                result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
            else:
                result = (result-inferiorLimit) + segmentLength*stackPointer;
            if passingArray == 1:
                if op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] * op2
                else:
                    print('MEM: ', methodsMemory[op1])
                    methodsMemory[result] = methodsMemory[op1] * op2
            elif passingArray == 2:
                if op2 < inferiorLimit:
                    methodsMemory[result] = op1 * globalMemory[op2]
                else:
                    methodsMemory[result] = op1 * methodsMemory[op2]
                    print('MEM: ', methodsMemory[op2])
            elif passingArray == 3:
                if op1 < inferiorLimit and op2 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] * globalMemory[op2]
                elif op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] * methodsMemory[op2]
                elif op2 < inferiorLimit:
                    methodsMemory[result] = methodsMemory[op1] * globalMemory[op2]
                else:
                    methodsMemory[result] = methodsMemory[op1] * methodsMemory[op2]
            else:
                methodsMemory[result] = op1 * op2
        elif result < inferiorLimit:
            if passingArray == 1:
                if op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] * op2
                else:
                    print('MEM: ', methodsMemory[op1])
                    methodsMemory[result] = methodsMemory[op1] * op2
            elif passingArray == 2:
                if op2 < inferiorLimit:
                    methodsMemory[result] = op1 * globalMemory[op2]
                else:
                    methodsMemory[result] = op1 * methodsMemory[op2]
            elif passingArray == 3:
                if op1 < inferiorLimit and op2 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] * globalMemory[op2]
                elif op1 < inferiorLimit:
                    methodsMemory[result] = globalMemory[op1] * methodsMemory[op2]
                elif op2 < inferiorLimit:
                    methodsMemory[result] = methodsMemory[op1] * globalMemory[op2]
                else:
                    methodsMemory[result] = methodsMemory[op1] * methodsMemory[op2]
            else:
                methodsMemory[result] = op1 * op2
    except:
        raise TypeError("Operation invalid for specified operand types")
    passingArray = 0

def DIV(op1, op2, result):
    global passingArray
    if op2 == 0:
        raise ValueError("Attempting to divide by 0")
    else:
        try:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                if passingArray == 1:
                    if op1 < inferiorLimit:
                        methodsMemory[result] = globalMemory[op1] / op2
                    else:
                        print('MEM: ', methodsMemory[op1])
                        methodsMemory[result] = methodsMemory[op1] / op2
                elif passingArray == 2:
                    if op2 < inferiorLimit:
                        methodsMemory[result] = op1 / globalMemory[op2]
                    else:
                        methodsMemory[result] = op1 / methodsMemory[op2]
                elif passingArray == 3:
                    if op1 < inferiorLimit and op2 < inferiorLimit:
                        methodsMemory[result] = globalMemory[op1] / globalMemory[op2]
                    elif op1 < inferiorLimit:
                        methodsMemory[result] = globalMemory[op1] / methodsMemory[op2]
                    elif op2 < inferiorLimit:
                        methodsMemory[result] = methodsMemory[op1] / globalMemory[op2]
                    else:
                        methodsMemory[result] = methodsMemory[op1] / methodsMemory[op2]
                else:
                    methodsMemory[result] = op1 / op2
            elif result < inferiorLimit:
                if passingArray == 1:
                    if op1 < inferiorLimit:
                        methodsMemory[result] = globalMemory[op1] / op2
                    else:
                        print('MEM: ', methodsMemory[op1])
                        methodsMemory[result] = methodsMemory[op1] / op2
                elif passingArray == 2:
                    if op2 < inferiorLimit:
                        methodsMemory[result] = op1 / globalMemory[op2]
                    else:
                        methodsMemory[result] = op1 / methodsMemory[op2]
                elif passingArray == 3:
                    if op1 < inferiorLimit and op2 < inferiorLimit:
                        methodsMemory[result] = globalMemory[op1] / globalMemory[op2]
                    elif op1 < inferiorLimit:
                        methodsMemory[result] = globalMemory[op1] / methodsMemory[op2]
                    elif op2 < inferiorLimit:
                        methodsMemory[result] = methodsMemory[op1] / globalMemory[op2]
                    else:
                        methodsMemory[result] = methodsMemory[op1] / methodsMemory[op2]
                else:
                    methodsMemory[result] = op1 / op2
        except:
            raise TypeError("Operation invalid for specified operand types: {} = {} / {}".format(result, op1, op2))
        passingArray = 0
#LOGICAL EXP

def CEQ(op1, op2, result):
    try:
        if op1 == op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
        print ("RESULT_MOD: ", result)
    except:
        raise TypeError("Operation invalid for specified operand types")

def CNE(op1, op2, result):
    try:
        if op1 != op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def CLT(op1, op2, result):
    try:
        if op1 < op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def CGT(op1, op2, result):
    try:
        if op1 > op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def CLE(op1, op2, result):
    try:
        if op1 <= op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def CGE(op1, op2, result):
    try:
        if op1 >= op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

#   BEGIN BOOLEAN OPERATIONS
def AND(op1, op2, result):
    try:
        if op1 and op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def ORR(op1, op2, result):
    try:
        if op1 or op2:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = True
            elif result < inferiorLimit:
                globalMemory[result] = True
        else:
            if result >= inferiorLimit:
                if passingParameters:
                    result = (result-inferiorLimit) + segmentLength*(stackPointer-1);
                else:
                    result = (result-inferiorLimit) + segmentLength*stackPointer;
                methodsMemory[result] = False
            elif result < inferiorLimit:
                globalMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")
#   END BOOLEAN OPERATIONS


#   BEGIN JUMP AND FUNCTION OPERATIONS
def GTO(op1, op2, result):
    global PC
    PC = result - 1

def GTF(op1, op2, result):
    global PC
    try:
        if not op1:
            PC = result - 1
    except:
        raise TypeError("Type mismatch, expected boolean")

def ERA(op1, op2, result):
    global passingParameters, stackPointer
    stackPointer+=1
    #print stackPointer
    passingParameters = True


def CAL(op1, op2, result):
    global passingParameters
    jumpStack.append(PC)
    GTO(op1, op2, result)
    passingParameters = False
   # print


def RET(op1, op2, result):
    global stackPointer
    #print op1
    stackPointer-=1
    returnStack.append(op1)
    result = jumpStack.pop()
    # print("something")
    # print(op1)
    # print(result)
    # wait = input("PRESS ENTER TO CONTINUE.")
    # print("something")
    GTO(op1, op2, result+1)
#   END JUMP AND FUNCTION OPERATIONS

def PRT(op1, op2, result):
    try:
        print (op1)
    except:
        raise TypeError("Operation invalid for specified operand type")

def MVT(op1, op2, result):
    try:
        cheese.fd(op1)
    except:
        raise TypeError("Type mismatch, expected an integer or double value")

def ROT(op1, op2, result):
    try:
        cheese.rt(op1)
    except:
        raise TypeError("Type mismatch, expected an integer or double value")

def ARC(op1, op2, result):
    try:
        cheese.circle(op1, op2)
    except:
        raise TypeError("Type mismatch, expected an integer value")

def HOM(op1, op2, result):
    cheese.home()

def PDO(op1, op2, result):
    cheese.pd()

def PUP(op1, op2, result):
    cheese.pu()

def SET(op1, op2, result):
    try:
        cheese.setpos(op1, op2)
    except:
        raise TypeError("Type mismatch, expected an integer or double value")

def PCO(op1, op2, result):
    try:
        if result >= inferiorLimit:
            result = (result-inferiorLimit) + segmentLength*stackPointer;
            result = methodsMemory[result]
        else:
            result = globalMemory[result]
        if op1 <= 255 and op2 <= 255 and result <= 255:
            cheese.pencolor(op1, op2, result)
        else:
            raise ValueError("Value mismatch, expected an integer between 0 and 255")
    except:
        raise TypeError("Type mismatch, expected an integer or double value")

def PSZ(op1, op2, result):
    try:
        cheese.pensize(op1)
    except:
        raise TypeError("Type mismatch, expected an integer value")

def PCL(op1, op2, result):
    cheese.clear()

def runVM():
    global PC, operator, op1, op2, result, passingArray
    PC = 0
    methods = globals().copy()
    methods.update(locals())

    while PC < len(instructionMemory):
        op1Return = False
        op2Return = False
        #Read quadruple
        operator, op1, op2, result = instructionMemory[PC]
        result = int(result)
        #Translate addresses
        if operator not in ["SUM"]:
            if passingParameters:
                try:
                    op2 = int(op2)
                except:
                    op2 = op2[1:-1]
                    op2 = int(op2)
                    passingArray = 2
                if op2 >= inferiorLimit:
                    op2 = (op2 - inferiorLimit) + segmentLength*(stackPointer-1)
                    #print "OP2: ", op2
                    op2 = methodsMemory[op2]
                elif op2 < inferiorLimit:
                    #print "OP2: ", op2
                    op2 = globalMemory[op2]
                elif op2 == 17000:
                    op2 = returnStack.pop()

                try:
                    op1 = int(op1)
                except:
                    op1 = op1[1:-1]
                    op1 = int(op1)
                    if passingArray == 2:
                        passingArray = 3
                    else:
                        passingArray = 1
                if op1 >= inferiorLimit:
                    op1 = (op1 - inferiorLimit) + segmentLength*(stackPointer-1)
                    #print "OP1: ", op1
                    op1 = methodsMemory[op1]
                elif op1 < inferiorLimit:
                    # print ("OP1: ", op1)
                    op1 = globalMemory[op1]
                elif op1 == 17000:
                    op1 = returnStack.pop()

            else:
                try:
                    op2 = int(op2)
                except:
                    op2 = op2[1:-1]
                    op2 = int(op2)
                    passingArray = 2
                    print('ARR: ', op2)
                if op2 >= inferiorLimit:
                    op2 = (op2 - inferiorLimit) + segmentLength*(stackPointer)
                    #print "OP2: ", op2
                    op2 = methodsMemory[op2]
                elif op2 < inferiorLimit:
                    #print "OP2: ", op2
                    op2 = globalMemory[op2]
                elif op2 == 17000:
                    op2 = returnStack.pop()

                try:
                    op1 = int(op1)
                except:
                    op1 = op1[1:-1]
                    op1 = int(op1)
                    if passingArray == 2:
                        passingArray = 3
                    else:
                        passingArray = 1
                    print('ARR: ', op1)
                if op1 >= inferiorLimit:
                    op1 = (op1 - inferiorLimit) + segmentLength*(stackPointer)
                    #print "OP1: ", op1
                    op1 = methodsMemory[op1]
                elif op1 < inferiorLimit:
                    # print ("OP1: ", op1)
                    op1 = globalMemory[op1]
                elif op1 == 17000:
                    op1 = returnStack.pop()

        #print "PC: ", PC
        #print [operator, op1, op2, result]
        #Execute quadruple
        method = methods.get(str(operator))
        if not method:
            raise Exception("Method \"{}\" not implemented!".format(str(operator)))

        print("OPERATOR: ", operator)
        print("OP1: ", op1)
        print("OP2: ", op2)
        print("RESULT: ", result)
        print("Pointer: ", stackPointer)
        method(op1, op2, result)

        #Increment PC to execute next instruction
        PC += 1
    input("Press any key to exit...")
   #Debugging code
    '''
    for i,n in enumerate(instructionMemory):
        print "{}\t{}\t{}\t{}\t{}\n".format(i, n[0], n[1], n[2], n[3])
    raise SystemExit
    '''

if __name__ == '__main__':
    if len(sys.argv) == 2:
        #Load code to the VM
        with open(sys.argv[1],'r') as code:
            line = code.readline()
            fields = shlex.split(line)
            while fields[0] == 'CST':
                try:
                    op1 = int(fields[1])
                except:
                    try:
                        op1 = float(fields[1])
                    except:
                        op1 = str(fields[1])

                globalMemory[int(fields[3])] = op1

                line = code.readline()
                fields = shlex.split(line)

            instructionMemory.append(fields)
            for line in code.readlines():
                instructionMemory.append(line.split())
        #Done loading code. Execute.
        # print (instructionMemory)
        runVM()
    else:
        print ("Usage syntax: %s filename" %sys.argv[0])
