import ply.lex as lex
import ply.yacc as yacc
import glob
from program import *

# Tokens
tokens = ('INC',
          'DEC',
          'LEFT',
          'RIGHT',
          'OUTPUT',
          'INPUT',
          'POSITION',
          'JUMP',
          )

t_INC = r'\+'
t_DEC = r'\-'
t_LEFT = r'<'
t_RIGHT = r'>'
t_OUTPUT = r'\.'
t_INPUT = r','
t_POSITION = r'\['
t_JUMP = r'\]'

# Ignore
t_ignore = ' \t'

def t_error(t):
  print('Invalid Character: \'{}\''.format(t.value[0]))
  t.lexer.skip(1)

# Lex time
lexer = lex.lex()

# Parse rules with optional precedence
def p_expression(p):
  """
  expression : operation
              | expression operation
  """
  # Operation
  if len(p) == 2:
    p[0] = Operations([p[1]])
    return

  if not p[1]:
    p[1] = Operations([])

  # Expression Operation
  # P1 = Everything so far
  # P2 = Next item
  p[1].operations.append(p[2])
  p[0] = p[1]


def p_operation(p):
  """
  operation : INC
            | DEC
            | LEFT
            | RIGHT
            | OUTPUT
            | INPUT
            | loop
  """
  # Operation
  if isinstance(p[1], str):
    p[0] = Operation(p[1])
  # Loop
  else:
    p[0] = p[1]

def p_loop(p):
  'loop : POSITION expression JUMP'
  p[0] = Loop(p[2])

def p_error(p):
  print('Syntax Error!')

# Parsing time
parser = yacc.yacc()

# Main code - No error checking here
listing = glob.glob('./bf/*.bf') 
for num, filename in enumerate(listing):
  print('({}) - {}'.format(num, '\\' + filename[2:]))

which = int(input('Select a file to interpret: '))
code = ''
with open(listing[which], 'r') as file:
  code = file.read()

code = code.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')

program = Program(parser.parse(code))
r_o_t = int(input('Run(1) or Transpile(2) or both(3): '))
if r_o_t & 2:
  print('Transpiling:\t{}'.format(listing[which]))
  program.generate(listing[which][5:-3])
if r_o_t & 1:
  print('\nRunning:\t{}'.format(listing[which]))
  program.run()
