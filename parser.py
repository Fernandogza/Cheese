import sys
import ply.yacc as yacc
from lexer import tokens
from procedureDirectory import procedureDirectory, Variable
from quadrupleGenerator import quadrupleGenerator
from semanticCube import getResultingType

currentDirectory = procedureDirectory("global")
functionDirectory = None
instructions = quadrupleGenerator()

variableStack = []
seenType = None
parameterCounter = 0
Function_Or_Var_Name = []

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
    global instructions
    while len(instructions.jumpStack) is not 0:
        pendingJump = instructions.popJumpStack()
        instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

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
    '''variable_declarator  : ID seen_id variable_declarator2 variable_declarator3'''


def p_seen_id(p):
    '''seen_id :'''

def p_variable_declarator2(p):
    '''variable_declarator2 : LSQUARE CSTINT RSQUARE
                            | empty'''
    global currentDirectory
    if p[1]:
        currentDirectory.add_variable(p[-2], seenType, p[2])
    else:
        currentDirectory.add_variable(p[-2], seenType, 0)

def p_variable_declarator3(p):
    '''variable_declarator3 : '=' superexpression
                            | empty'''

def p_method_declaration(p):
    '''method_declaration : FUNC type ID seen_function_id '(' method_declaration2 method_declaration3'''
    global currentDirectory
    instructions.generateQuadruple("RET",0,0,0)
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
    currentDirectory.startAddress = instructions.nextInstruction - 1

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
    '''variable_assignment : ID '=' superexpression SEMICOLON'''
    global instructions, currentDirectory

    variable = currentDirectory.get_variable(p[1])

    if variable:
        op1 = variable
        result = instructions.popOperand()
        operator = p[2]

        validType = getResultingType(operator, result.Type, op1.Type)
        if validType:
            operator = 'EQU'
            instructions.generateQuadruple(operator, op1, 0, result)
        else:
            print ("ERROR: Invalid types! Variable \"{}\" cannot store \"{}\"!".format(currentDirectory.get_variable(result.Name), currentDirectory.get_variable(op1.Name)))
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
            print ("ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name))
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

    resultingType = getResultingType(operator, op1.Type, op2.Type)
    if resultingType is None:
        print ("ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name))
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

        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            print ("ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name))
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

        resultingType = getResultingType(operator, op1.Type, op2.Type)

        if resultingType is None:
            print ("ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name))
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
        print (varType)
        op1 = currentDirectory.add_const(varType, p[1])
    if op1:
        instructions.pushOperand(op1)

def p_seen_id_or_func(p):
    '''seen_id_or_func :'''
    global Function_Or_Var_Name
    Function_Or_Var_Name.append(p[-1])


def p_cst_expression2(p):
    '''cst_expression2 : LSQUARE superexpression RSQUARE
                       | '(' cst_expression3 ')'
                       | empty'''
    global instructions
    name = Function_Or_Var_Name[len(Function_Or_Var_Name)-1]
    if p[1] == "(":
        variable = currentDirectory.get_directory(name).getReturnVariable()
    else:
        variable = currentDirectory.get_variable(name)

    Function_Or_Var_Name.pop()

    if variable:
        instructions.pushOperand(variable)
    else:
        print ("ERROR! Variable \"{}\" not found!".format(name))
        raise SystemExit


def p_cst_expression3(p):
   '''cst_expression3 : superexpression cst_expression4'''

def p_cst_expression4(p):
    '''cst_expression4 : COMMA cst_expression3
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
        print ("ERROR: Expected type bool, but found {}!".format(condition.Type))
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
        print ("ERROR: Expected type bool, but found {}!".format(condition.Type))
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
        print ("ERROR: Expected conditional, but found {}!".format(condition.Type))
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
        instructions.generateQuadruple('RED', op1, 0, 0);
    else:
        print ("ERROR: Variable \"{}\" undeclared!".format(name))
        raise SystemExit

def p_print_statement(p):
    '''print_statement  : PRINT '(' superexpression ')' SEMICOLON'''
    global instructions
    op1 = instructions.popOperand()
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
    if op1.Type is int:
        instructions.generateQuadruple('ROT', op1, 0, 0)
    else:
        lineNum = p.lineno(1)
        print ("ERROR: Expected type int, but found {} in line!".format(op1.Type, lineNum))
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
                 | variable_assignment
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
       print("Syntax error at '{}' in line {}".format(p.value, p.lineno))
   global instructions, currentDirectory
   # print (currentDirectory)
   print (instructions)

#Test routine
if __name__ == '__main__':
    if len(sys.argv) == 2:
        f = open(sys.argv[1], 'r')
        s = f.read()
        parser = yacc.yacc()
        parser.parse(s);
        print (currentDirectory)
        print (instructions)

        # myFile = open("loroCode.vwl", 'w')
        # myFile.write(str(currentDirectory.getConstantDeclarations()))
        # myFile.write(str(instructions))
        # myFile.close()
    else:
        print ("Usage syntax: %s filename" %sys.argv[0])
