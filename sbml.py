# NAME : David Xie
# SBU ID: 111098813

import ply.lex as lex
import ply.yacc as yacc
import sys
import string

# Global
indent_level = 0

class Node():
    def __init__(self, parent = None, lineno = 0, colno = 0):
        self.parent = parent
        self.lineno = lineno
        self.colno = colno

class Real(Node):
    def __init__(self, parent=None, lineno=0, colno=0, name=""):
        super().__init__(parent, lineno, colno)
        self.name = float(name)

    def execute(self):
        return self.name

    def __ge__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return float(self.name) >= other

    def __le__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return float(self.name) <= other

    def __gt__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return float(self.name) > other

    def __lt__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return float(self.name) < other

    def __eq__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return float(self.name) == other

class Integer(Node):
    def __init__(self, parent=None, lineno=0, colno=0, name=""):
        super().__init__(parent, lineno, colno)
        self.name = int(name)

    def execute(self):
        return self.name

    def __ge__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return int(self.name) >= other

    def __le__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return int(self.name) <= other

    def __gt__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return int(self.name) > other

    def __lt__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return int(self.name) < other

    def __eq__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return int(self.name) == other

class A_Boolean(Node):
    def __init__(self, parent=None, lineno=0, colno=0, name=""):
        super().__init__(parent, lineno, colno)
        if name == 'True':
            self.name = True
        if name == 'False':
            self.name = False
        #self.name = int(name)

    def execute(self):
        return self.name

class A_Variable(Node):
    def __init__(self, parent=None, lineno=0, colno=0, name=""):
        super().__init__(parent, lineno, colno)
        self.name = name

    def execute(self):
        global declaredVars
        #if self.name in declaredVars:
        return declaredVars[self.name]
        #else:
            #return str(self.name)
    def get_name(self):
        return str(self.name)

class A_String(Node):
    def __init__(self, parent=None, lineno=0, colno=0, name=""):
        super().__init__(parent, lineno, colno)
        self.name = str(name)

    def execute(self):
        return self.name

    def __ge__(self, other):
        if not isinstance(other, str):
            return NotImplemented
        return str(self.name) >= other

    def __le__(self, other):
        if not isinstance(other, str):
            return NotImplemented
        return str(self.name) <= other

    def __gt__(self, other):
        if not isinstance(other, str):
            return NotImplemented
        return str(self.name) > other

    def __lt__(self, other):
        if not isinstance(other, str):
            return NotImplemented
        return str(self.name) < other

    def __eq__(self, other):
        if not isinstance(other, str):
            return NotImplemented
        return str(self.name) == other

class Tuple_Creation(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def execute(self):
        return self.child

class Addition(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() + self.right.execute()

class Subtraction(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() - self.right.execute()

class Negative(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None):
        super().__init__(parent, lineno, colno)
        self.left = left

    def execute(self):
        return -self.left.execute()

class Multiplication(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() * self.right.execute()

class Division(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() / self.right.execute()

class Division_Int(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return Integer(None, None, None, self.left.execute() // self.right.execute()).execute()

class Exponentiation(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() ** self.right.execute()

class Modulus(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() % self.right.execute()

class Array_Creation(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def execute(self):
        return [self.child.execute()]

class Array_Append(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return [self.left.execute()] + self.right.execute()

class Array_Indexing(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute()[self.right.execute()]

class Array_Indexing_2d(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, middle=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.middle = middle
        self.right = right

    def execute(self):
        return self.left.execute()[self.middle.execute()][self.right.execute()]

class Tuple_Indexing(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute()[self.right]

class Array_Addition(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() + self.right.execute()

class In(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() in self.right.execute()

class Cons(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        arr = self.right.execute()
        arr.insert(0, self.left.execute())
        return arr

class Less_Than(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() < self.right.execute()

class Less_Than_Equal(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() <= self.right.execute()

class Greater_Than(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() > self.right.execute()

class Greater_Than_Equal(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() >= self.right.execute()

class Equals(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() == self.right.execute()

class Not_Equals(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() != self.right.execute()

class Negation(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def execute(self):
        return not self.child.execute()

class Conjunction(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() and self.right.execute()

class Disjunction(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        return self.left.execute() or self.right.execute()

class Parenthesis(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def execute(self):
        return self.child.execute()

class Assignment(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        if type(self.left) is A_Variable:
            global declaredVars
            #declaredVars[self.left.execute()] = self.right.execute()
            declaredVars[self.left.get_name()] = self.right.execute()
            #return self.left.execute()
        else:
            return t_error()

class Print_This(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def execute(self):
        if type(self.child) is A_Variable:
            global declaredVars
            print(self.child.execute())
        else:
            print(self.child.execute())

class Block(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def execute(self):
        return self.child.execute()

class If_Statement(Node):
    def __init__(self, parent=None, lineno=0, colno=0, expression=None, block_statement=None):
        super().__init__(parent, lineno, colno)
        self.expression = expression
        self.block_statement = block_statement

    def execute(self):
        if self.expression.execute() is True:
            return self.block_statement.execute()
        else:
            pass

class If_Else_Statement(Node):
    def __init__(self, parent=None, lineno=0, colno=0, expression=None, block_statement=None, else_statement=None):
        super().__init__(parent, lineno, colno)
        self.expression = expression
        self.block_statement = block_statement
        self.else_statement = else_statement

    def execute(self):
        if self.expression.execute() is True:
            return self.block_statement.execute()
        else:
            return self.else_statement.execute()

class While_Statement(Node):
    def __init__(self, parent=None, lineno=0, colno=0, expression=None, block_statement=None):
        super().__init__(parent, lineno, colno)
        self.expression = expression
        self.block_statement = block_statement

    def execute(self):
        while self.expression.execute() is True:
            self.block_statement.execute()
        pass

class Statement_Creation(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def execute(self):
        return self.child.execute()

class Statement_Append(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def execute(self):
        self.left.execute()
        return self.right.execute()

class Empty(Node):
    def __init__(self, parent=None, lineno=0, colno=0):
        super().__init__(parent, lineno, colno)

    def execute(self):
        return

tokens = (
    'INTEGER',
    'REAL',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'EXPONENTIATION',
    'DIVIDE',
    'INT_DIV',
    'MODULUS',
    'BOOLEAN',
    'STRING',
    'TUPLE',
    'LBRAC',
    'RBRAC',
    'LPAREN',
    'RPAREN',
    'CURLYLBRACE',
    'CURLYRBRACE',
    'HASHTAG',
    'IN',
    'COMMA',
    'CONS',
    'NOT',
    'EQUAL',
    'EQUAL_EQUAL',
    'LESS_THAN',
    'LESS_THAN_EQUAL',
    'GREATER_THAN',
    'GREATER_THAN_EQUAL',
    'NOT_EQUAL',
    'AND_ALSO',
    'OR_ELSE',
    'IF',
    'ELSE',
    'WHILE',
    'VARIABLE',
    'PRINT',
    'SEMICOLON',
)

t_EXPONENTIATION = r'\*{2}'
t_ignore = r' '

def t_PLUS(t):
    r'\+'
    t.type = 'PLUS'
    t.value = t.value
    return t

def t_MINUS(t):
    r'\-'
    t.type = 'MINUS'
    t.value = t.value
    return t

def t_REAL(t):
    r'([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][-]?[0-9]+)?'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_MULTIPLY(t):
    r'\*'
    t.type = 'MULTIPLY'
    t.value = t.value
    return t

def t_DIVIDE(t):
    r'\/'
    t.type = 'DIVIDE'
    t.value = t.value
    return t

def t_INT_DIV(t):
    r'div'
    t.type = 'INT_DIV'
    return t

def t_MODULUS(t):
    r'mod'
    t.type = 'MODULUS'
    return t

def t_BOOLEAN(t):
    #r'(Tru|Fals)?e'
    r'(True|False)'
    t.type = 'BOOLEAN'
    return t

def t_IN(t):
    r'in'
    t.type = 'IN'
    return t

def t_NOT(t):
    r'not'
    t.type = 'NOT'
    t.value = t.value
    return t

def t_TUPLE(t):
    #r'\((.*)(,\s*.+)*\)'
    #r'\((.*)(,\s*.+)+[^,]+\)'
    r'\(([^=()+]*)(,)+[^,]+\)'
    t.type = 'TUPLE'
    try:
        t.value = eval(t.value)
    except SyntaxError:
        print("SYNTAX ERROR")
    return t

def t_STRING(t):
    r'("[^\"\']+"|\'[^\"\']+\')'
    t.type = 'STRING'
    t.value = t.value[1:-1]
    return t

def t_LPAREN(t):
    r'\('
    t.type = 'LPAREN'
    t.value = t.value
    return t

def t_RPAREN(t):
    r'\)'
    t.type = 'RPAREN'
    t.value = t.value
    return t

def t_LBRAC(t):
    r'\['
    t.type = 'LBRAC'
    t.value = t.value
    return t

def t_RBRAC(t):
    r'\]'
    t.type = 'RBRAC'
    t.value = t.value
    return t

def t_CURLYLBRACE(t):
    r'\{'
    t.type = 'CURLYLBRACE'
    t.value = t.value
    return t

def t_CURLYRBRACE(t):
    r'\}'
    t.type = 'CURLYRBRACE'
    t.value = t.value
    return t

def t_HASHTAG(t):
    r'\#'
    t.type = 'HASHTAG'
    t.value = t.value
    return t

def t_COMMA(t):
    r'\,'
    t.type = 'COMMA'
    t.value = t.value
    return t

def t_CONS(t):
    r'::'
    t.type = 'CONS'
    t.value = t.value
    return t

def t_EQUAL_EQUAL(t):
    r'=='
    t.type = 'EQUAL_EQUAL'
    t.value = t.value
    return t

def t_EQUAL(t):
    r'='
    t.type = 'EQUAL'
    t.value = t.value
    return t

def t_NOT_EQUAL(t):
    r'\<\>'
    t.type = 'NOT_EQUAL'
    t.value = t.value
    return t

def t_LESS_THAN_EQUAL(t):
    r'\<='
    t.type = 'LESS_THAN_EQUAL'
    t.value = t.value
    return t

def t_LESS_THAN(t):
    r'\<'
    t.type = 'LESS_THAN'
    t.value = t.value
    return t

def t_GREATER_THAN_EQUAL(t):
    r'\>='
    t.type = 'GREATER_THAN_EQUAL'
    t.value = t.value
    return t

def t_GREATER_THAN(t):
    r'\>'
    t.type = 'GREATER_THAN'
    t.value = t.value
    return t

def t_AND_ALSO(t):
    r'andalso'
    t.type = 'AND_ALSO'
    t.value = t.value
    return t

def t_OR_ELSE(t):
    r'orelse'
    t.type = 'OR_ELSE'
    t.value = t.value
    return t

def t_PRINT(t):
    r'print'
    t.type = 'PRINT'
    t.value = t.value
    return t

def t_IF(t):
    r'if'
    t.type = 'IF'
    t.value = t.value
    return t

def t_ELSE(t):
    r'else'
    t.type = 'ELSE'
    t.value = t.value
    return t

def t_WHILE(t):
    r'while'
    t.type = 'WHILE'
    t.value = t.value
    return t

def t_VARIABLE(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = 'VARIABLE'
    t.value = t.value
    return t

def t_SEMICOLON(t):
    r';'
    t.type = 'SEMICOLON'
    t.value = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
#    print("SEMANTIC ERROR: %s at %d" % (t.value[0], t.lexer.lineno))
    global errorFlag
    global semanticFlag
    errorFlag = 1
    semanticFlag = 1
    t.lexer.skip(1)

lexer = lex.lex()

#lexer.input(' { x = 2; if ( x == 2) {print(x);} else {print("no");} } ')
#lexer.input('{ x = 0; while(x != 5) { x = x + 1;} print(x); }')
#lexer.input(' { number = 33; isPrime = 1; i = 2; while(i < 3) { i = i + 1; } print(i); }')

#while True:
#    tok = lexer.token()
#    if not tok:
#        break
#    print(tok)


precedence = (
    ('left', 'OR_ELSE'),
    ('left', 'AND_ALSO'),
    ('left', 'NOT'),
    ('left', 'LESS_THAN', 'LESS_THAN_EQUAL', 'EQUAL_EQUAL', 'NOT_EQUAL', 'GREATER_THAN_EQUAL', 'GREATER_THAN'),
    ('right', 'CONS'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('right', 'UMINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'INT_DIV', 'MODULUS'),
    ('right', 'EXPONENTIATION'),
    ('left', 'LBRAC', 'RBRAC'),
    ('left', 'TUPLE'),
    ('left', 'LPAREN', 'RPAREN')
)


#def p_calc(p):
#    '''
#    calc : expression SEMICOLON
#    '''
#    #print(p[1])
#    p[0] = p[1]


def p_block(p):
    '''
    block : CURLYLBRACE statement_list CURLYRBRACE
    '''
    p[0] = p[2]

#def p_statement_list_single(p):
#    '''
#    statement_list : statement
#    '''
#    #print(p[1])
#    #p[0] = p[1]
#    p[0] = p[1]

#def p_statement_list(p):
#    '''
#    statement_list : statement_list statement
#    '''
#    p[0] = p[2]
#    p[1].execute()

#def p_statement(p):
#    '''
#    statement : expression SEMICOLON
#    '''
#    #print(p[1])
#    p[0] = p[1]

def p_statement_list(p):
    '''
    statement_list : statement statement_tail
    '''
    #print(p[1])
    #p[0] = p[1]
    #p[1].execute()
    #p[0] = p[2]
    p[0] = Statement_Append(None, p.lineno, p.lexpos, p[1], p[2])

def p_statement_tail(p):
    '''
    statement_tail : statement statement_tail
    '''
    #p[0] = p[1]
    p[0] = Statement_Append(None, p.lineno, p.lexpos, p[1], p[2])

def p_statement_list_single(p):
    '''
    statement_list : statement
    '''
    #print(p[1])
    #p[0] = p[1]
    #p[1].execute()
    #p[0] = p[2]
    p[0] = Statement_Creation(None, p.lineno, p.lexpos, p[1])

def p_statement_tail_single(p):
    '''
    statement_tail : statement
    '''
    #p[0] = p[1]
    p[0] = Statement_Creation(None, p.lineno, p.lexpos, p[1])

def p_statement(p):
    '''
    statement : expression SEMICOLON
    '''
    #print(p[1])
    p[0] = p[1]

def p_if_else(p):
    '''
    statement : IF LPAREN expression RPAREN block ELSE block
    '''
    #print(p[1])
    p[0] = If_Else_Statement(None, p.lineno, p.lexpos, p[3], p[5], p[7])


def p_if(p):
    '''
    statement : IF LPAREN expression RPAREN block
    '''
    #print(p[1])
    p[0] = If_Statement(None, p.lineno, p.lexpos, p[3], p[5])

def p_while(p):
    '''
    statement : WHILE LPAREN expression RPAREN block
    '''
    #print(p[1])
    p[0] = While_Statement(None, p.lineno, p.lexpos, p[3], p[5])

def p_addition_number(p) :
    'expression : expression PLUS expression'
    p[0] = Addition(None, p.lineno, p.lexpos, p[1], p[3])
    p[1].parent = p[0]
    p[3].parent = p[0]
    #p[0] = p[1] + p[3]
    #print(p[0])

#def p_addition_string(p) :
#    'expression : expression PLUS STRING'
#    p[0] = Addition(None, p.lineno, p.lexpos, p[1], p[3])
#    p[1].parent = p[0]
#    p[3].parent = p[0]
#    #p[0] = p[1] + p[3]
#    #print(p[0])

#def p_addition_number(p) :
#    'expression : number PLUS number'
#    p[0] = Addition(None, p.lineno, p.lexpos, p[1], p[3])
#    p[1].parent = p[0]
#    p[3].parent = p[0]
#    #p[0] = p[1] + p[3]

#def p_addition_string(p) :
#    'expression : STRING PLUS STRING'
#    #p[0] = p[1] + p[3]
#    p[0] = Addition(None, p.lineno, p.lexpos, p[1], p[3])
#    p[1].parent = p[0]
#    p[3].parent = p[0]

#def p_addition_list(p) :
#    'expression : list PLUS list'
#    p[0] = p[1] + p[3]

def p_addition_list(p) :
    'expression : list PLUS list'
    #p[0] = p[1] + p[3]
    p[0] = Array_Addition(None, p.lineno, p.lexpos, p[1], p[3])

def p_subtraction_number(p) :
    'expression : expression MINUS expression'
    #p[0] = p[1] - p[3]
    p[0] = Subtraction(None, p.lineno, p.lexpos, p[1], p[3])
    #p[1].parent = p[0]
    #p[3].parent = p[0]

def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = Negative(None, p.lineno, p.lexpos, p[2])

def p_multiplication_number(p) :
    'expression : expression MULTIPLY expression'
    #p[0] = p[1] * p[3]
    p[0] = Multiplication(None, p.lineno, p.lexpos, p[1], p[3])
    #p[1].parent = p[0]
    #p[3].parent = p[0]

def p_exponentiatioon(p) :
    'expression : expression EXPONENTIATION expression'
    #p[0] = p[1] ** p[3]
    p[0] = Exponentiation(None, p.lineno, p.lexpos, p[1], p[3])
    #p[1].parent = p[0]
    #p[3].parent = p[0]

def p_division(p) :
    'expression : expression DIVIDE expression'
    #p[0] = float(p[1] / p[3])
    p[0] = Division(None, p.lineno, p.lexpos, p[1], p[3])
    #p[1].parent = p[0]
    #p[3].parent = p[0]

def p_int_div(p) :
    'expression : expression INT_DIV expression'
    #p[0] = p[1] // p[3]
    p[0] = Division_Int(None, p.lineno, p.lexpos, p[1], p[3])
    #p[1].parent = p[0]
    #p[3].parent = p[0]

def p_modulus(p) :
    'expression : expression MODULUS expression'
    #p[0] = p[1] % p[3]
    p[0] = Modulus(None, p.lineno, p.lexpos, p[1], p[3])
    p[1].parent = p[0]
    p[3].parent = p[0]

#def p_in_string(p) :
#    '''
#    expression : term IN STRING
#    '''
#    #'expression : STRING IN STRING'
#    #p[0] = p[1] in p[3]
#    p[0] = In(None, p.lineno, p.lexpos, p[1], A_String(None, p.lineno, p.lexpos, p[3]))

def p_in_list(p) :
    '''
    expression : expression IN expression
    '''
    #'expression : STRING IN STRING'
    #p[0] = p[1] in p[3]
    p[0] = In(None, p.lineno, p.lexpos, p[1], p[3])

#def p_expression_int_real(p):
#   '''
#   expression : number
#              | TUPLE
#              | list
#               | BOOLEAN
#    '''
#    p[0] = p[1]
#    #p[0] = p[1]

def p_expression_int_real(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term_number(p):
    '''
    term : number
    '''
    p[0] = p[1]
    #p[0] = p[1]

def p_term_string(p):
    '''
    term : STRING
    '''
    p[0] = A_String(None, p.lineno, p.lexpos, p[1])
    #p[0] = p[1]

def p_term_boolean(p):
    '''
    term : BOOLEAN
    '''
    p[0] = A_Boolean(None, p.lineno, p.lexpos, p[1])

def p_term_variable(p):
    '''
    term : VARIABLE
    '''
    p[0] = A_Variable(None, p.lineno, p.lexpos, p[1])

def p_term_list(p):
    '''
    term : list
    '''
    p[0] = p[1]

def p_term_tuple(p):
    '''
    term : TUPLE
    '''
    p[0] = Tuple_Creation(None, p.lineno, p.lexpos, p[1])
    #p[0] = p[1]

#def p_expression_string(p):
#    '''
#    expression : STRING
#    '''
#    p[0] = A_String(None, p.lineno, p.lexpos, p[1])
#    #p[0] = p[1]

def p_list(p):
    'list : LBRAC expression COMMA list_tail RBRAC'
    #p[0] = [p[2]] + p[4]
    p[0] = Array_Append(None, p.lineno, p.lexpos, p[2], p[4])
    p[2].parent = p[0]
    p[4].parent = p[0]

def p_list_tail(p):
    'list_tail : expression COMMA list_tail'
    #p[0] = [p[1]] + p[3]
    p[0] = Array_Append(None, p.lineno, p.lexpos, p[1], p[3])
    p[1].parent = p[0]
    p[3].parent = p[0]

def p_list_single_String(p):
    'list : LBRAC STRING RBRAC'
    #p[0] = [p[2]]
    p[0] = Array_Creation(None, p.lineno, p.lexpos, A_String(None, p.lineno, p.lexpos, p[2]))
    A_String(None, p.lineno, p.lexpos, p[2]).parent = p[0]

def p_list_single_INT(p):
    'list : LBRAC number RBRAC'
    #p[0] = [p[2]]
    p[0] = Array_Creation(None, p.lineno, p.lexpos, p[2])
    p[2].parent = p[0]

#def p_list_single_exp(p):
#    'list : LBRAC expression RBRAC'
#    #p[0] = [p[2]]
#    p[0] = Array_Creation(None, p.lineno, p.lexpos, p[2])
#    p[2].parent = p[0]

def p_list_tail_empty(p):
    '''
    list_tail : expression
    '''
    #p[0] = [p[1]]
    p[0] = Array_Creation(None, p.lineno, p.lexpos, p[1])
    p[1].parent = p[0]


def p_indexing(p):
    '''
    expression : expression LBRAC expression RBRAC
    '''
    #if p[3] >= 0:
    #    p[0] = p[1][p[3]]
    #else:
    #    p_error(p)

    #if p[3] >= 0:
    p[0] = Array_Indexing(None, p.lineno, p.lexpos, p[1], p[3])
    #p[1].parent = p[0]
    #p[3].parent = p[0]
    #else:
        #p_error(p)

def p_indexing_2d(p):
    '''
    expression : expression LBRAC expression RBRAC LBRAC expression RBRAC
    '''
    #if p[3] >= 0:
    #    p[0] = p[1][p[3]]
    #else:
    #    p_error(p)

    #if p[3] >= 0:
    p[0] = Array_Indexing_2d(None, p.lineno, p.lexpos, p[1], p[3], p[6])
    #p[1].parent = p[0]
    #p[3].parent = p[0]
    #else:
        #p_error(p)


#def p_tuple_arg(p):
#    '''
#    expression : HASHTAG INTEGER TUPLE
#    '''
#    if p[2] >= 1:
#        p[0] = p[3][p[2]-1]
#    else:
#        p_error(p)

def p_tuple_arg(p):
    '''
    expression : HASHTAG INTEGER TUPLE
    '''
    if p[2] >= 1:
        p[0] = Tuple_Indexing(None, p.lineno, p.lexpos, Tuple_Creation(None, p.lineno, p.lexpos, p[3]), p[2]-1)
    else:
        p_error(p)

#def p_tuple_declare(p):
#    '''
#    expression : VAR_CHAR EQUAL TUPLE
#    '''
#    global declaredVars
#    declaredVars[p[1]] = p[3]
#    p[0] = declaredVars[p[1]]

def p_assignment(p):
    '''
    statement : VARIABLE EQUAL expression SEMICOLON
    '''
    #global declaredVars
    #declaredVars[p[1]] = p[3]
    #p[0] = declaredVars[p[1]]
    p[0] = Assignment(None, p.lineno, p.lexpos, A_Variable(None, p.lineno, p.lexpos, p[1]), p[3])

def p_print(p):
    '''
    statement : PRINT LPAREN expression RPAREN SEMICOLON
    '''
    #global declaredVars
    #declaredVars[p[1]] = p[3]
    #p[0] = declaredVars[p[1]]
    p[0] = Print_This(None, p.lineno, p.lexpos, p[3])

def p_cons(p):
    '''
    expression : term CONS list
    '''
    #try:
    #    p[3].insert(0,p[1])
    #    p[0] = p[3]
    #except SyntaxError:
    #    print("SYNTAX ERROR")
    p[0] = Cons(None, p.lineno, p.lexpos, p[1], p[3])

#def p_less_than(p):
#    '''
#    expression : number LESS_THAN number
#               | STRING LESS_THAN STRING
#    '''
#    try:
#        p[0] = p[1] < p[3]
#    except SyntaxError:
#        print("SYNTAX ERROR")

def p_less_than(p):
    '''
    expression : expression LESS_THAN expression
    '''
    try:
        p[0] = Less_Than(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        p_error(p)

def p_less_than_equal(p):
    '''
    expression : expression LESS_THAN_EQUAL expression
    '''
    try:
        p[0] = Less_Than_Equal(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        print("SYNTAX ERROR")

def p_equal(p):
    '''
    expression : expression EQUAL_EQUAL expression
    '''
    try:
        p[0] = Equals(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        p_error(p)

def p_greater_than(p):
    '''
    expression : expression GREATER_THAN expression
    '''
    try:
        p[0] = Greater_Than(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        p_error(p)

def p_greater_than_equal(p):
    '''
    expression : expression GREATER_THAN_EQUAL expression
    '''
    try:
        p[0] = Greater_Than_Equal(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        p_error(p)

def p_not_equal(p):
    '''
    expression : expression NOT_EQUAL expression
    '''
    try:
        p[0] = Not_Equals(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        p_error(p)

def p_negation(p):
    '''
    expression : NOT expression
    '''
    try:
        p[0] = Negation(None, p.lineno, p.lexpos, p[2])
    except SyntaxError:
        p_error(p)

def p_conjunction(p):
    '''
    expression : expression AND_ALSO expression
    '''
    try:
        p[0] = Conjunction(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        p_error(p)

def p_disjunction(p):
    '''
    expression : expression OR_ELSE expression
    '''
    try:
        p[0] = Disjunction(None, p.lineno, p.lexpos, p[1], p[3])
    except SyntaxError:
        p_error(p)

def p_paren(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = Parenthesis(None, p.lineno, p.lexpos, p[2])

def p_number_int_real(p):
    'number : REAL'
    p[0] = Real(None, p.lineno, p.lexpos, p[1])

def p_number_int(p):
    'number : INTEGER'
    p[0] = Integer(None, p.lineno, p.lexpos, p[1])

#def p_empty(p):
#    'empty :'
#    p[0] = Empty(None, None, None)


def p_error(p):
#    print("SYNTAX ERROR")
    global errorFlag
    global syntaxFlag
    errorFlag = 1
    syntaxFlag = 1
    p.lexer.skip(1)

parser = yacc.yacc()

#while True:
    #try:
    #    s = input('')
    #except EOFError:
    #    break
f = open(sys.argv[1], "r")
s = f.read()
f.close()
global declaredVars
declaredVars = {}
global errorFlag
global semanticFlag
global syntaxFlag
errorFlag = 0
semanticFlag = 0
syntaxFlag = 0
result = parser.parse(s)
if errorFlag == 0:
    result.execute()
else:
    if syntaxFlag == 1 and semanticFlag == 1:
        print("SYNTAX ERROR")
    else:
        if syntaxFlag == 1:
            print("SYNTAX ERROR")
        if semanticFlag == 1:
            print("SEMANTIC ERROR")