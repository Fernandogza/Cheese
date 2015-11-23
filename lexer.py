import ply.lex as lex

# List of literals operators:
literals = ['=','+','-','*','/', '(',')']

# List of token names.
tokens = [
    'ID',
    'RBRACKET',
    'LBRACKET',
    'RSQUARE',
    'LSQUARE',
    'CGT',
    'CLT',
    'CGE',
    'CLE',
    'CEQ',
    'CNE',
    'CSTINT',
    'CSTDOUBLE',
    'CSTSTRING',
    'COMMA',
    'SEMICOLON',
    'AND',
    'OR']

#List of reserved words.
reserved = {
   'main' : 'MAIN',
   'cheese' : 'CHEESE',
   'int' : 'INT',
   'double' : 'DOUBLE',
   'string' : 'STRING',
   'if' : 'IF',
   'else' : 'ELSE',
   'for' : 'FOR',
   'while' : 'WHILE',
   'scanf' : 'SCAN',
   'print' : 'PRINT',
   'move' : 'MOVE',
   'rotate' : 'ROTATE',
   'arc' : 'ARC',
   'home' : 'HOME',
   'pdown' : 'PDOWN',
   'pup' : 'PUP',
   'setp' : 'SETP',
   'pcolor' : 'PCOLOR',
   'psize' : 'PSIZE',
   'clear' : 'PCLEAR',
   'void' : 'VOID',
   'return' : 'RETURN',
   'func' : 'FUNC',
}

#Add the reserved words to the list of tokens
tokens += list(reserved.values())


#Regular Expressions for tokens
t_RBRACKET  = r'\}'
t_LBRACKET  = r'\{'
t_LSQUARE   = r'\['
t_RSQUARE   = r'\]'
t_CGT   = r'\>'
t_CLT      = r'\<'
t_CGE = r'\>\='
t_CLE    = r'\<\='
t_CEQ  = r'\=\='
t_CNE     = r'\!\='
t_SEMICOLON = r'\;'
t_COMMA     = r'\,'
t_CSTSTRING = r'\".*?\"'
t_AND       = r'\&\&'
t_OR        = r'\|\|'

def t_COMMENT(t):
    r'//.*'
    pass
    #No return value. Token discarded

#Rule for ID's, where reserved words are checked.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t

def t_CSTDOUBLE(t):
    r'[+-]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CSTINT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r'

# Error handling rule
def t_error(t):
    print("Illegal character '%s' at line '%i'" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

# Build the lex
lex.lex()
