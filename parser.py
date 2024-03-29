import sys
import ply.yacc as yacc
from lexer import tokens
from lexer import reserved
from procedureDirectory import procedureDirectory, Variable
from quadrupleGenerator import quadrupleGenerator
from semanticCube import getResultingType

currentDirectory = procedureDirectory("global")
functionDirectory = None
instructions = quadrupleGenerator()

variableStack = []
seenType = None
parameterCounter = 0
parameterCounterInt = 0
parameterCounterDou = 0
parameterCounterStr = 0
Function_Or_Var_Name = []
arrayType = []

precedence =    (
                ('left', 'AND', 'OR'),
                ('left', '+', '-'),
                ('left', '*', '/')
                )


start = 'program'

def p_program(p):
    '''program  : program2 program3 main_ahead main_method'''
    print("Compilation completed...")
    # sys.exit(0);

def p_main_ahead(p):
    '''main_ahead :'''
    global instructions, currentDirectory
    while len(instructions.jumpStack) is not 0:
        pendingJump = instructions.popJumpStack()
        instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)
    name = 'main cheese'
    # print (functionId)
    currentDirectory.add_directory(name)
    currentDirectory = currentDirectory.get_directory(name)
    currentDirectory.Type = 'main'

def p_program2(p):
    '''program2 : variable_declaration program2
                | empty'''

def p_program3(p):
    '''program3 : method_declaration program3
                | empty'''

def p_variable_declaration(p):
    '''variable_declaration  : type variable_declaration2'''

def p_variable_declaration2(p):
    '''variable_declaration2 : variable_declarator variable_declaration3'''

def p_variable_declaration3(p):
    '''variable_declaration3 : COMMA variable_declaration2
                             | SEMICOLON'''

def p_variable_declarator(p):
    '''variable_declarator  : ID variable_declarator2 variable_declarator3'''

def p_variable_declarator2(p):
    '''variable_declarator2 : LSQUARE CSTINT RSQUARE
                            | empty'''
    global currentDirectory, instructions
    if p[1]:
        currentDirectory.add_variable(p[-2], seenType, p[2])
        variable = currentDirectory.get_variable(p[-2])
        if variable.Type is int:
            instructions.generateQuadruple('INI', variable.Address, variable.Dimension, 1)
        elif variable.Type is float:
            instructions.generateQuadruple('INI', variable.Address, variable.Dimension, 2)
        elif variable.Type is str:
            instructions.generateQuadruple('INI', variable.Address, variable.Dimension, 3)
    else:
        currentDirectory.add_variable(p[-2], seenType, 0)

def p_variable_declarator3(p):
    '''variable_declarator3 : '=' superexpression
                            | empty'''
    global instructions, currentDirectory
    if p[1]:
        variable = currentDirectory.get_variable(p[-3])
        if variable and variable.Dimension == 0:
            op1 = instructions.popOperand()
            result = variable
            operator = p[1]

            validType = getResultingType(operator, result.Type, op1.Type)
            if validType:
                operator = 'EQU'
                instructions.generateQuadruple(operator, op1, 0, result)
            else:
                print ("ERROR: Invalid types in line {}. Variable '{}' of type '{}' cannot store '{}'!".format(p.lineno(1), currentDirectory.get_variable(result.Name).Name, currentDirectory.get_variable(result.Name).Type, currentDirectory.get_variable(op1.Name).Name))
                raise SystemExit
        else:
            if variable.Dimension > 0:
                print("ERROR: Variable '{}' cannot be initialized since it is an array, in line {}!".format(p[-3], p.lineno(1)))
            else:
                print("ERROR: Variable '{}' not declared in this scope, in line {}!".format(p[-3], p.lineno(1)))
                raise SystemExit

def p_method_declaration(p):
    '''method_declaration : FUNC type ID seen_function_id '(' method_declaration2 method_declaration3'''
    global currentDirectory
    instructions.generateQuadruple('RET',0,0,0)
    currentDirectory = currentDirectory.parent

def p_seen_function_id(p):
    '''seen_function_id :'''
    global currentDirectory
    functionId = p[-1]
    # print (functionId)
    currentDirectory.add_directory(functionId)
    currentDirectory = currentDirectory.get_directory(functionId)
    currentDirectory.Type = seenType

def p_method_declaration2(p):
    '''method_declaration2 : parameter_list
                           | empty'''

def p_method_declaration3(p):
    '''method_declaration3 : ')' seen_method_start block_statement'''

def p_seen_method_start(p):
    '''seen_method_start :'''
    global currentDirectory, instructions
    currentDirectory.startAddress = instructions.nextInstruction

def p_parameter_list(p):
    '''parameter_list  : parameter parameter_list2
       parameter_list2 : COMMA parameter_list
                       | empty'''

def p_parameter(p):
    '''parameter : type ID'''
    global currentDirectory
    variableId = p[2]
    currentDirectory.parameters.append(variableId)
    currentDirectory.add_variable(variableId, seenType, 0)

def p_main_method(p):
    '''main_method : MAIN CHEESE '(' ')' block_statement'''

def p_type(p):
    '''type : INT
            | DOUBLE
            | STRING
            | VOID'''
    global seenType
    variableTypes = { 'int' : int, 'double' : float, 'string' : str, 'void' : 'void' }
    seenType = variableTypes[p[1]]

def p_variable_assignment(p):
    '''variable_assignment : ID id_or_array'''

def p_id_or_array(p):
    '''id_or_array : '=' superexpression
                   | LSQUARE seen_LSQUARE superexpression RSQUARE seen_RSQUARE '=' superexpression'''
    global instructions, currentDirectory

    variable = currentDirectory.get_variable(p[-1])

    if variable:
        if variable.Dimension > 0 and p[1] == '[':
            operator = p[6]
            op2 = variable.Dimension
            tempOp1 = instructions.popOperand()   #value to be assigned.
            op1 = instructions.popOperand()       #index of the array.
            if op1.Type is int:
                instructions.generateQuadruple('VER', op1, op2, variable.Address)
                result = currentDirectory.add_temp(int)
                result.Type = 'arr'
                arrayType.append(variable.Type)
                instructions.generateQuadruple('OFF', variable.Address, op1, result)
                instructions.pushOperand(result)
                op1 = tempOp1
                result = instructions.popOperand()
                if op1.Type is 'arr' and result.Type is 'arr':
                    result.Type = arrayType.pop()
                    op1.Type = arrayType.pop()
                    validType = getResultingType(operator, result.Type, op1.Type)
                    if validType:
                        op1 = '(' + str(op1.Address) + ')'
                        result = '(' + str(result.Address) + ')'
                        operator = 'EQU'
                        instructions.generateQuadruple(operator, op1, 0, result)
                    else:
                        print ("ERROR: Invalid types! Variable '{}' cannot store '{}'!".format(currentDirectory.get_variable(result.Name), currentDirectory.get_variable(op1.Name)))
                        raise SystemExit
                else:
                    result.Type = arrayType.pop()
                    validType = getResultingType(operator, result.Type, op1.Type)
                    if validType:
                        result = '(' + str(result.Address) + ')'
                        operator = 'EQU'
                        instructions.generateQuadruple(operator, op1, 0, result)
                    else:
                        print ("ERROR: Invalid types! Variable '{}' cannot store '{}'!".format(currentDirectory.get_variable(result.Name), currentDirectory.get_variable(op1.Name)))
                        raise SystemExit
            else:
                print("ERROR: Type error. Array index must be of type int, found {} at line {}!".format(op1.Type, p.lineno(1)))
                raise SystemExit
        elif p[1] == '=' and variable.Dimension == 0:
            op1 = instructions.popOperand()
            result = variable
            operator = p[1]

            if op1.Type is 'arr':
                op1.Type = arrayType.pop()
                validType = getResultingType(operator, result.Type, op1.Type)
                if validType:
                    op1 = '(' + str(op1.Address) + ')'
                    operator = 'EQU'
                    instructions.generateQuadruple(operator, op1, 0, result)
                else:
                    print ("ERROR: Invalid types! Variable '{}' cannot store '{}'!".format(currentDirectory.get_variable(result.Name), currentDirectory.get_variable(op1.Name)))
                    raise SystemExit
            else:
                validType = getResultingType(operator, result.Type, op1.Type)
                if validType:
                    operator = 'EQU'
                    instructions.generateQuadruple(operator, op1, 0, result)
                else:
                    print ("ERROR: Invalid types! Variable '{}' cannot store '{}'!".format(currentDirectory.get_variable(result.Name), currentDirectory.get_variable(op1.Name)))
                    raise SystemExit
        else:
            if p[1] == '=':
                print("ERROR: Variable '{}' is of type Array, must be accessed through an index, line {}!".format(p[-1], p.lineno(1)))
                raise SystemExit
            elif p[1] == '[':
                print("ERROR: Variable '{}' is not of type Array, line {}!".format(p[-1], p.lineno(1)))
                raise SystemExit
    else:
        print("ERROR: Variable '{}' not declared in this scope, line {}!".format(p[-1], p.lineno(1)))
        raise SystemExit

def p_superexpression(p):
    '''superexpression : expression superexpression2'''

def p_superexpression2(p):
    '''superexpression2 : andor superexpression
                        | empty'''

def p_andor(p):
    '''andor : AND
             | OR'''
    global instructions
    instructions.pushOperator(p[1])

def p_expression(p):
    '''expression : numeric_expression compare'''
    global instructions, currentDirectory
    if instructions.topOperatorEquals('&&') or instructions.topOperatorEquals('||') :
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()

        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
            raise SystemExit

        result = currentDirectory.add_temp(resultingType)

        if result:
            operator = {"&&" : "AND", "||" : "ORR"}[operator]
            instructions.generateQuadruple(operator, op1, op2, result)
            instructions.pushOperand(result)
        else:
            print ("EXPRESSION ERROR")

def p_compare(p):
    '''compare : compare_symbols numeric_expression seen_comp
               | empty'''

def p_compare_symbols(p):
    '''compare_symbols : CEQ
                       | CGT
                       | CGE
                       | CLT
                       | CLE
                       | CNE'''
    global instructions
    instructions.pushOperator(p[1])

def p_seen_comp(p):
    '''seen_comp :'''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()
    operator = instructions.popOperator()

    if op1.Type is 'arr' and op2.Type is 'arr':
        op2.Type = arrayType.pop()
        op1.Type = arrayType.pop()
        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
            raise SystemExit

        result = currentDirectory.add_temp(resultingType)
        op1 = '(' + str(op1.Address) + ')'
        op2 = '(' + str(op2.Address) + ')'
    elif op1.Type is 'arr':
        op1.Type = arrayType.pop()
        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
            raise SystemExit

        result = currentDirectory.add_temp(resultingType)
        op1 = '(' + str(op1.Address) + ')'
    elif op2.Type is 'arr':
        op2.Type = arrayType.pop()
        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
            raise SystemExit

        result = currentDirectory.add_temp(resultingType)
        op2 = '(' + str(op2.Address) + ')'
    else:
        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
            raise SystemExit

        result = currentDirectory.add_temp(resultingType)

    if result:
        operator = {"==" : "CEQ",
                    "!=" : "CNE",
                    "<"  : "CLT",
                    ">"  : "CGT",
                    "<=" : "CLE",
                    ">=" : "CGE"}[operator]
        instructions.generateQuadruple(operator, op1, op2, result)
        instructions.pushOperand(result)
    else:
        print ("SEEN_COMPARISON ERROR")


def p_numeric_expression(p):
    '''numeric_expression  : term seen_term numeric_expression2'''

def p_seen_term(p):
    '''seen_term :'''
    global instructions
    if instructions.topOperatorEquals('+') or instructions.topOperatorEquals('-'):
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()
        if op1.Type is 'arr' and op2.Type is 'arr':
            op2.Type = arrayType.pop()
            op1.Type = arrayType.pop()
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)
            op1 = '(' + str(op1.Address) + ')'
            op2 = '(' + str(op2.Address) + ')'
        elif op1.Type is 'arr':
            op1.Type = arrayType.pop()
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)
            op1 = '(' + str(op1.Address) + ')'
        elif op2.Type is 'arr':
            op2.Type = arrayType.pop()
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)
            op2 = '(' + str(op2.Address) + ')'
        else:
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)

        if result:
            if operator is '+':
                operator = 'ADD'
            elif operator is '-':
                operator = 'SUB'
            instructions.generateQuadruple(operator, op1, op2, result)
            instructions.pushOperand(result)
        else:
            print ("SEEN_TERM ERROR")

def p_numeric_expression2(p):
    '''numeric_expression2 : arithOp numeric_expression
                           | empty'''

def p_arithOp(p):
    '''arithOp : '+'
               | '-' '''
    global instructions
    instructions.pushOperator(p[1])

def p_term(p):
    '''term  : factor term2'''

def p_term2(p):
    '''term2 : geomOp term
             | empty'''

def p_geomOp(p):
    '''geomOp : '*'
              | '/' '''
    global instructions
    instructions.pushOperator(p[1])

def p_factor(p):
    '''factor  : cst_expression
               | '(' seen_lpar superexpression ')' seen_rpar '''
    global instructions
    if instructions.topOperatorEquals('*') or instructions.topOperatorEquals('/'):
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()

        if op1.Type is 'arr' and op2.Type is 'arr':
            op2.Type = arrayType.pop()
            op1.Type = arrayType.pop()
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)
            op1 = '(' + str(op1.Address) + ')'
            op2 = '(' + str(op2.Address) + ')'
        elif op1.Type is 'arr':
            op1.Type = arrayType.pop()
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)
            op1 = '(' + str(op1.Address) + ')'
        elif op2.Type is 'arr':
            op2.Type = arrayType.pop()
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)
            op2 = '(' + str(op2.Address) + ')'
        else:
            resultingType = getResultingType(operator, op1.Type, op2.Type)
            if resultingType is None:
                print ("ERROR: Operation '{}' between '{}' and '{}' cannot be performed. Incompatible types!".format(operator, op1.Type, op2.Type))
                raise SystemExit

            result = currentDirectory.add_temp(resultingType)

        if result:
            if operator is '*':
                operator = 'MUL'
            elif operator is '/':
                operator = 'DIV'
            instructions.generateQuadruple(operator, op1, op2, result)
            instructions.pushOperand(result)
        else:
            print ("FACTOR ERROR")

def p_seen_lpar(p):
    '''seen_lpar :'''
    global instructions
    instructions.pushOperator(p[-1])

def p_seen_rpar(p):
    '''seen_rpar :'''
    global instructions
    instructions.popOperator()

def p_cst_expression(p):
    '''cst_expression  : CSTDOUBLE
                       | CSTINT
                       | CSTSTRING
                       | ID seen_id_or_func cst_expression2'''
    global instructions, currentDirectory
    op1 = None
    if type(p[1]) is str:
        if p[1][0] == "\"":
            op1 = currentDirectory.add_const(str, p[1])
    else:
        varType = type(p[1])
        op1 = currentDirectory.add_const(varType, p[1])
    if op1:
        instructions.pushOperand(op1)

def p_seen_id_or_func(p):
    '''seen_id_or_func :'''
    global Function_Or_Var_Name
    Function_Or_Var_Name.append(p[-1])


def p_cst_expression2(p):
    '''cst_expression2 : LSQUARE seen_LSQUARE superexpression RSQUARE seen_RSQUARE
                       | function_call
                       | empty'''
    global instructions, arrayType
    name = Function_Or_Var_Name[len(Function_Or_Var_Name)-1]
    if p[1] and p[1] != "[":
        variable = currentDirectory.get_directory(name).getReturnVariable()
    else:
        variable = currentDirectory.get_variable(name)

    Function_Or_Var_Name.pop()

    if p[1] == "[" and variable:
        op2 = variable.Dimension
        op1 = instructions.popOperand()
        if op1.Type is int:
            instructions.generateQuadruple('VER', op1, op2, variable.Address)
            result = currentDirectory.add_temp(int)
            result.Type = 'arr'
            arrayType.append(variable.Type)
            instructions.generateQuadruple('OFF', variable.Address, op1, result)
            instructions.pushOperand(result)
        else:
            print("ERROR: Type error. Array index must be of type int, found {} at line {}!".format(op1.Type, p.lineno(1)))
            raise SystemExit
    elif variable:
        instructions.pushOperand(variable)
    else:
        print("ERROR: Variable '{}' not declared in this scope!".format(name))
        raise SystemExit

def p_seen_LSQUARE(p):
    '''seen_LSQUARE : '''
    global instructions
    instructions.pushOperator('(')

def p_seen_RSQUARE(p):
    '''seen_RSQUARE : '''
    global instructions
    instructions.popOperator()

def p_function_call(p):
    '''function_call :  seen_func_id '(' args ')' '''
    global instruction, currentDirectory, functionDirectory, parameterCounter
    if len(functionDirectory.parameters) == parameterCounter:
        instructions.generateQuadruple('CAL',0,0,functionDirectory.startAddress)
    else:
        print ("ERROR: Function '{}' received {} arguments, expected {} in line {}!".format(functionDirectory.identifier, parameterCounter,len(functionDirectory.parameters), p.lineno(2)))
        raise SystemExit
    instructions.operatorStack.pop()
    #Function_Or_Var_Name.pop()
    p[0] = True

def p_seen_func_id(p):
    '''seen_func_id : '''
    global currentDirectory, functionDirectory, parameterCounter, instructions, parameterCounterInt, parameterCounterDou, parameterCounterStr
    name = Function_Or_Var_Name[len(Function_Or_Var_Name)-1]
    #Function call as a statement
    functionDirectory = currentDirectory.get_directory(name)

    if not functionDirectory:
        print ("ERROR: Undeclared function: '{}'!".format(name))
        raise SystemExit

    parameterCounter = 0
    parameterCounterInt = 0
    parameterCounterDou = 0
    parameterCounterStr = 0
    instructions.operatorStack.append("(")
    instructions.generateQuadruple("ERA", 7050, 0, 0);

def p_args(p):
    '''args : arg
            | empty'''

def p_arg(p):
    '''arg : numeric_expression seen_arg more_args'''

def p_seen_arg(p):
    '''seen_arg : '''
    global instructions,currentDirectory,functionDirectory,parameterCounter, parameterCounterInt, parameterCounterDou, parameterCounterStr
    op1 = instructions.popOperand()

    if parameterCounter < len(functionDirectory.parameters):
        nextParam = functionDirectory.parameters[parameterCounter]
        variable = functionDirectory.get_variable(nextParam)
        compatibleType = getResultingType('=', variable.Type, op1.Type)
        if variable.Type is compatibleType:
            if variable.Type is int:
                instructions.generateQuadruple('EQU', op1, 0, Variable('Param{}'.format(parameterCounter), variable.Type, parameterCounterInt + 10000))
                parameterCounterInt += 1
            elif variable.Type is float:
                instructions.generateQuadruple('EQU', op1, 0, Variable('Param{}'.format(parameterCounter), variable.Type, parameterCounterDou + 11000))
                parameterCounterDou += 1
            elif variable.Type is str:
                instructions.generateQuadruple('EQU', op1, 0, Variable('Param{}'.format(parameterCounter), variable.Type, parameterCounterStr + 12000))
                parameterCounterStr += 1
        else:
            print ("ERROR: Incompatible arguments. Received '{}', expected '{}'!".format(op1.Type,functionDirectory.get_variable(nextParam).Type))
            raise SystemExit
        parameterCounter += 1
    else:
        print ("ERROR: Function '{}' received more arguments than expected!".format(functionDirectory.identifier))
        raise SystemExit

def p_more_args(p):
    '''more_args : COMMA arg
                | empty'''

def p_loop_statement(p):
    '''loop_statement : loophead block_statement seen_loop_block'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

def p_loophead(p):
    '''loophead : FOR '(' variable_assignment seen_assignment1 SEMICOLON superexpression seen_for_exp SEMICOLON variable_assignment seen_assignment2 ')'
                | WHILE '(' seen_while_LPAR superexpression seen_while_exp ')' '''

def p_seen_assignment1(p):
    '''seen_assignment1 : '''
    global instructions
    instructions.pushJumpStack(instructions.nextInstruction)

def p_seen_for_exp(p):
    '''seen_for_exp : '''
    global instructions
    condition = instructions.popOperand()

    if condition.Type is bool:
        pendingJump = instructions.popJumpStack()
        instructions.generateQuadruple('GTF', condition, 0, 0)
        instructions.pushJumpStack(instructions.nextInstruction - 1)
        #Pending: exit jump address

        instructions.generateQuadruple('GTO', 0, 0, 0)
        instructions.pushJumpStack(instructions.nextInstruction)
        instructions.pushJumpStack(instructions.nextInstruction - 1)
        #Pending: loop start jump address

        instructions.pushJumpStack(pendingJump)
    else:
        print ("ERROR: Expected type bool, but found {} in FOR Loop!".format(condition.Type))
        raise SystemExit

def p_seen_assignment2(p):
    '''seen_assignment2 : '''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple('GTO', 0, 0, pendingJump)
    #After assigning, jump to condition evaluation

    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)
    #Loop start jump address is right after assigning, where the loop header ends.

def p_seen_while_LPAR(p):
    '''seen_while_LPAR : '''
    global instructions
    instructions.pushJumpStack(instructions.nextInstruction)

def p_seen_while_exp(p):
    '''seen_while_exp : '''
    global instructions
    condition = instructions.popOperand()

    if condition.Type is bool:
        pendingJump = instructions.popJumpStack()
        instructions.generateQuadruple('GTF', condition, 0, 0)
        instructions.pushJumpStack(instructions.nextInstruction - 1)
        instructions.pushJumpStack(pendingJump)
    else:
        print ("ERROR: Expected type bool, but found {} in WHILE Loop!".format(condition.Type))
        raise SystemExit

def p_seen_loop_block(p):
    '''seen_loop_block  :'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GTO", 0, 0, pendingJump)

def p_if_statement(p):
    '''if_statement  : IF '(' superexpression ')' seen_condition block_statement seen_condition_block if_statement2'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

def p_seen_condition(p):
    '''seen_condition   :'''
    global instructions
    condition = instructions.popOperand()

    if condition.Type is bool:
        instructions.generateQuadruple("GTF", condition, 0, 0)
        instructions.pushJumpStack(instructions.nextInstruction - 1)
    else:
        print ("ERROR: Expected conditional, but found {} in IF Statement!".format(condition.Type))
        raise SystemExit

def p_seen_condition_block(p):
    '''seen_condition_block :'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GTO", 0, 0, 0)
    instructions.pushJumpStack(instructions.nextInstruction -1)
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

def p_if_statement2(p):
    '''if_statement2 : ELSE block_statement
                     | empty'''

def p_block_statement(p):
    '''block_statement  : LBRACKET block_statement2 RBRACKET
       block_statement2 : statement block_statement2
                        | empty'''

def p_read_statement(p):
    '''read_statement : SCAN '(' ID ')' SEMICOLON'''
    global instructions
    name = p[3]
    variable = currentDirectory.get_variable(name);
    if variable:
        if variable.Type is int:
            instructions.generateQuadruple('RED', variable, 1, 0);
        elif variable.Type is float:
            instructions.generateQuadruple('RED', variable, 2, 0);
        elif variable.Type is str:
            instructions.generateQuadruple('RED', variable, 3, 0);
    else:
        print ("ERROR: Variable '{}' not declared in this scope, line {}!".format(name, p.lineno(1)))
        raise SystemExit

def p_print_statement(p):
    '''print_statement  : PRINT '(' superexpression ')' SEMICOLON'''
    global instructions
    op1 = instructions.popOperand()
    if op1.Type is 'arr':
        op1.Type = arrayType.pop()
        op1 = '(' + str(op1.Address) + ')'
    instructions.generateQuadruple('PRT', op1, 0, 0);

def p_geometry_statement(p):
    '''geometry_statement : move
                          | rotate
                          | arc
                          | home
                          | pdown
                          | pup
                          | setp
                          | pcolor
                          | psize
                          | pclear '''

def p_move(p):
    '''move : MOVE '(' superexpression ')' '''
    global instructions
    op1 = instructions.popOperand()
    if op1.Type is int or op1.Type is float:
        instructions.generateQuadruple('MVT', op1, 0, 0)
    else:
        lineNum = p.lineno(1)
        print ("ERROR: Expected type int or double, but found {} in line!".format(op1.Type, lineNum))
        raise SystemExit

def p_rotate(p):
    '''rotate : ROTATE '(' superexpression ')' '''
    global instructions
    op1 = instructions.popOperand()

    if op1.Type is int or op1.Type is float:
        instructions.generateQuadruple('ROT', op1, 0, 0)
    else:
        lineNum = p.lineno(1)
        print ("ERROR: Expected type int or double, but found {} in line!".format(op1.Type, lineNum))
        raise SystemExit

def p_arc(p):
    '''arc : ARC '(' superexpression COMMA superexpression ')' '''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()

    if op1.Type is int and op2.Type is int:
        instructions.generateQuadruple('ARC', op1, op2, 0)
    else:
        lineNum = p.lineno(1)
        print ("ERROR: Expected type int, but found {} and {} in line {}!".format(op1.Type, op2.Type, lineNum))
        raise SystemExit

def p_home(p):
    '''home : HOME '(' ')' '''
    global instructions
    instructions.generateQuadruple('HOM', 0, 0, 0)

def p_pdown(p):
    '''pdown : PDOWN '(' ')' '''
    global instructions
    instructions.generateQuadruple('PDO', 0, 0, 0)

def p_pup(p):
    '''pup : PUP '(' ')' '''
    global instructions
    instructions.generateQuadruple('PUP', 0, 0, 0)

def p_setp(p):
    '''setp : SETP '(' superexpression COMMA superexpression ')' '''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()

    if op1.Type is int and op2.Type is int or op1.Type is int and op2.Type is float or op1.Type is float and op2.Type is int or op1.Type is float and op2.Type is float:
        instructions.generateQuadruple('SET', op1, op2, 0)
    else:
        lineNum = p.lineno(1)
        print ("ERROR: Expected type int or double, but found {} and {} in line{}!".format(op1.Type, op2.Type, lineNum))
        raise SystemExit

def p_pcolor(p):
    '''pcolor : PCOLOR '(' superexpression COMMA superexpression COMMA superexpression ')' '''
    global instructions
    op3 = instructions.popOperand()
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()
    if op1.Type is int and op2.Type is int and op3.Type is int:
        instructions.generateQuadruple('PCO', op1, op2, op3)
    else:
        lineNum = p.lineno(1)
        print ("ERROR: Expected type int, but found {}, {} and {} in line{}!".format(op1.Type, op2.Type, op3.Type, lineNum))
        raise SystemExit

def p_psize(p):
    '''psize : PSIZE '(' superexpression ')' '''
    global instructions
    op1 = instructions.popOperand()

    if op1.Type is int:
        instructions.generateQuadruple('PSZ', op1, 0, 0)
    else:
        lineNum = p.lineno(1)
        print ("ERROR: Expected type int, but found {} in line{}!".format(op1.Type, lineNum))
        raise SystemExit

def p_pclear(p):
    '''pclear : PCLEAR '(' ')' '''
    global instructions
    instructions.generateQuadruple('PCL', 0, 0, 0)

def p_statement(p):
    '''statement : variable_declaration
                 | variable_assignment SEMICOLON
                 | superexpression SEMICOLON
                 | if_statement
                 | loop_statement
                 | return
                 | print_statement
                 | read_statement
                 | geometry_statement SEMICOLON'''

def p_return(p):
    '''return : RETURN superexpression SEMICOLON'''
    global currentDirectory, instructions
    if currentDirectory.Type is not 'void':
        var = instructions.popOperand()
        compatibleType = getResultingType('=', currentDirectory.Type, var.Type)

        if compatibleType:
            instructions.generateQuadruple('RET',var,0,0)
        else:
            print ("ERROR: Incompatible return types! Received {}, expected {}!".format(var.Type, currentDirectory.Type))
            raise SystemExit

def p_empty(p):
    'empty :'
    pass

def p_error(p):
   if p:
    if p.value in reserved:
        print("ERROR: Syntax error at '{}' in line {}. Cannot use reserved word '{}' as a variable or function!".format(p.value, p.lineno, p.value))
    else:
        print("ERROR: Syntax error at '{}' in line {}!".format(p.value, p.lineno))
    raise SystemExit

#Test routine
if __name__ == '__main__':
    if len(sys.argv) == 2:
        f = open(sys.argv[1], 'r')
        s = f.read()
        parser = yacc.yacc()
        parser.parse(s);
        # print (currentDirectory.parent)
        # print (instructions)

        myFile = open("cheeseCode.rekt", 'w')
        myFile.write(str(currentDirectory.parent.getConstantDeclarations()))
        myFile.write(str(instructions))
        myFile.close()
    else:
        print ("Usage syntax: %s filename" %sys.argv[0])
