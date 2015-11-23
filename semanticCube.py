def getResultingType(operator, op1, op2):
    semanticCube = {
        int: {
          int: {
            '+'   : int,
            '-'   : int,
            '*'   : int,
            '/'   : int,
            '<'   : bool,
            '<='  : bool,
            '>'   : bool,
            '>='  : bool,
            '=='  : bool,
            '!='  : bool,
            '&&'  : None,
            '||'  : None,
            '='   : int
          },
          float: {
            '+'   : float,
            '-'   : float,
            '*'   : float,
            '/'   : float,
            '<'   : bool,
            '<='  : bool,
            '>'   : bool,
            '>='  : bool,
            '=='  : bool,
            '!='  : bool,
            '&&'  : None,
            '||'  : None,
            '='   : None
          },
          str: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : None,
            '!='  : None,
            '&&'  : None,
            '||'  : None,
            '='   : None
          },
          bool: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : None,
            '!='  : None,
            '&&'  : None,
            '||'  : None,
            '='   : None
          }
        },

        float: {
          int: {
            '+'   : float,
            '-'   : float,
            '*'   : float,
            '/'   : float,
            '<'   : bool,
            '<='  : bool,
            '>'   : bool,
            '>='  : bool,
            '=='  : bool,
            '!='  : bool,
            '&&'  : None,
            '||'  : None,
            '='   : float
          },
          float: {
            '+'   : float,
            '-'   : float,
            '*'   : float,
            '/'   : float,
            '<'   : bool,
            '<='  : bool,
            '>'   : bool,
            '>='  : bool,
            '=='  : bool,
            '!='  : bool,
            '&&'  : None,
            '||'  : None,
            '='   : float
          },
          str: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : None,
            '!='  : None,
            '&&'  : None,
            '||'  : None,
            '='   : None
          },
          bool: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : None,
            '!='  : None,
            '&&'  : None,
            '||'  : None,
            '='   : None
          }
        },

        str: {
          int: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : None,
            '!='  : None,
            '&&'  : None,
            '||'  : None,
            '='   : None
          },
          float: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : None,
            '!='  : None,
            '&&'  : None,
            '||'  : None,
            '='   : None
          },
          str: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : None,
            '!='  : None,
            '&&'  : None,
            '||'  : None,
            '='   : str
          },
          bool: {
            '+'   : None,
            '-'   : None,
            '*'   : None,
            '/'   : None,
            '<'   : None,
            '<='  : None,
            '>'   : None,
            '>='  : None,
            '=='  : bool,
            '!='  : bool,
            '&&'  : None,
            '||'  : None,
            '='   : None
          }
        },

        bool: {
            int: {
              '+'   : None,
              '-'   : None,
              '*'   : None,
              '/'   : None,
              '<'   : None,
              '<='  : None,
              '>'   : None,
              '>='  : None,
              '=='  : None,
              '!='  : None,
              '&&'  : None,
              '||'  : None,
              '='   : None
            },
            float: {
              '+'   : None,
              '-'   : None,
              '*'   : None,
              '/'   : None,
              '<'   : None,
              '<='  : None,
              '>'   : None,
              '>='  : None,
              '=='  : None,
              '!='  : None,
              '&&'  : None,
              '||'  : None,
              '='   : None
            },
            str: {
              '+'   : None,
              '-'   : None,
              '*'   : None,
              '/'   : None,
              '<'   : None,
              '<='  : None,
              '>'   : None,
              '>='  : None,
              '=='  : None,
              '!='  : None,
              '&&'  : None,
              '||'  : None,
              '='   : None
            },
            bool: {
              '+'   : None,
              '-'   : None,
              '*'   : None,
              '/'   : None,
              '<'   : None,
              '<='  : None,
              '>'   : None,
              '>='  : None,
              '=='  : None,
              '!='  : None,
              '&&'  : bool,
              '||'  : bool,
              '='   : bool
            }
          }

    }
    try:
        return semanticCube[op1][op2][operator]
    except KeyError:
        raise KeyError("WARNING! KeyError in getResultingType: semanticCube[{}][{}][{}]".format(op1, op2, operator))
        return None

#Test routine
if __name__ == '__main__':
    op1 = [ int, float, str, bool ]
    op2 = [ int, float, str, bool ]
    operator = [ '+', '-', '*', '/', '<', '<=', '>', '>=', '==', '<>', '&&', '||', '=' ]

    for i in op1:
        for j in op2:
            for k in operator:
                print ("{:15} {:^5} {:15} => {:15}".format(i, k, j, getResultingType(i, j, k)))
            print
        print
