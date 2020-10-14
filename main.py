import ply.lex as lex
import ply.yacc as yacc
import glob
from sys import stdout

class Program:
  def __init__(self, operations):
    self.operations = operations
    self.pointer = 0
    self.memory = [0] * 10
    self.buffer = []
    self.tab_depth = 0
    self.target_code = ''
  
  def run(self):
    self.operations.run(self)
  
  def generate(self, name):
    self.addline('from sys import stdout\n\nmemory = [0] * 10\npointer = 0\nbuffer = []\n')
    self.operations.generate(self)
    with open('./py/{}.py'.format(name), 'w') as file:
      file.write(self.target_code)
  
  def addline(self, code):
    self.target_code += '\t' * self.tab_depth + code + '\n'

class Loop:
  def __init__(self, operations):
    self.operations = operations
  
  def run(self, program):
    while program.memory[program.pointer] != 0:
      self.operations.run(program)
  
  def generate(self, program):
    program.addline('while memory[pointer] != 0:')
    program.tab_depth += 1
    self.operations.generate(program)
    program.tab_depth -= 1

class Operations:
  def __init__(self, operations):
    self.operations = operations
  
  def run(self, program):
    for operation in self.operations:
      operation.run(program)
  
  def generate(self, program):
    for operation in self.operations:
      operation.generate(program)

class Operation:
  def __init__(self, operation):
    self.operation = operation
  
  def run(self, program):
    if isinstance(self.operation, Loop):
      self.operation.run(program)
    else:
      if self.operation == '+':
        program.memory[program.pointer] += 1
      elif self.operation == '-':
        program.memory[program.pointer] -= 1
      elif self.operation == '>':
        program.pointer += 1
        if program.pointer >= len(program.memory):
          program.memory.append(0)
      elif self.operation == '<':
        program.pointer -= 1
        if program.pointer < 0:
          program.pointer = 0
      elif self.operation == '.':
        stdout.write(chr(program.memory[program.pointer]))
        stdout.flush()
      elif self.operation == ',':
        char = ''
        if len(program.buffer) == 0:
          program.buffer = [i for i in input('\n<< ')]
        if len(program.buffer) == 0:
          char = 0
        else:
          char = ord(program.buffer.pop(0))
        program.memory[program.pointer] = char
  
  def generate(self, program):
    if isinstance(self.operation, Loop):
      self.operation.generate(program)
    else:
      if self.operation == '+':
        program.addline('memory[pointer] += 1')
      elif self.operation == '-':
        program.addline('memory[pointer] -= 1')
      elif self.operation == '>':
        program.addline('pointer += 1')
        program.addline('if pointer >= len(memory): memory.append(0)')
      elif self.operation == '<':
        program.addline('pointer -= 1')
        program.addline('if pointer < 0: pointer = 0')
      elif self.operation == '.':
        program.addline('stdout.write(chr(memory[pointer]))')
        program.addline('stdout.flush()')
      elif self.operation == ',':
        program.addline('char = \'\'')
        program.addline('if len(buffer) == 0: buffer = [i for i in input(\'\\n<< \')]')
        program.addline('if len(buffer) == 0: char = 0')
        program.addline('else: char = ord(buffer.pop(0))')
        program.addline('memory[pointer] = char')



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
