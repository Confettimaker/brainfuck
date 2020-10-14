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