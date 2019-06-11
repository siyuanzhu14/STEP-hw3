def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1

def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def readTimes(line, index):
  token = {'type': 'TIMES'}
  return token, index + 1

def readDivide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1

def readLeftP(line, index):
  token = {'type': 'LEFTP'}
  return token, index + 1

def readRightP(line, index):
  token = {'type': 'RIGHTP'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readTimes(line, index)
    elif line[index] == '/':
      (token, index) = readDivide(line, index)
    elif line[index] == '(':
      (token, index) = readLeftP(line, index)
    elif line[index] == ')':
      (token, index) = readRightP(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


#return a tokens without parentheses, elimilating the priority order of calculation
def flatten(tokens):
    
  left_list = []#the list containing the positions of '('
  right_list = []#positions of ')'
  
  index = 0
  while index < len(tokens):
      if tokens[index]['type'] == 'RIGHTP':
          right_list +=  [index]
      elif tokens[index]['type'] == 'LEFTP':
          left_list += [index]
      index += 1

  index = 0
  for tempR in right_list:
      tempL = [x for x in left_list if x < tempR][-1]

      #(tempL,tempR) is the contains all the elements we need to deal with now(no parentheses inside)
      tempTokens = list(filter(None,tokens[tempL+1:tempR]))
      #use temporary Tokens instead of deleting the empty elements because the positions have been memoed.
      
      #calculate the elements inside the parentheses
      tokens[tempL]={'type':'NUMBER', 'number': evaluate(tempTokens)}
      
      tokens[tempL+1:tempR+1] = [{}]*(tempR-tempL)
      left_list.remove(tempL)
      
  return list(filter(None,tokens))



def evaluate(tokens):

  tokens = flatten(tokens)
  
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  
  index = 1
  while index < len(tokens): #Multiplication and division go first
      if tokens[index]['type'] == 'TIMES':
          tokens[index - 1]['number'] *= tokens[index + 1]['number']
          tokens[index] = {}
          tokens[index + 1] = {}
          tokens = list(filter(None,tokens))
          index -= 1
      elif tokens[index]['type'] == 'DIVIDE':
          tokens[index - 1]['number'] /= tokens[index + 1]['number']
          tokens[index] = {}
          tokens[index + 1] = {}
          tokens = list(filter(None,tokens))
          index -= 1
      else:
          index += 1
          
  index = 1
  while index < len(tokens):
      if tokens[index]['type'] == 'NUMBER':
          if tokens[index - 1]['type'] == 'PLUS':
            answer += tokens[index]['number']
          elif tokens[index - 1]['type'] == 'MINUS':
            answer -= tokens[index]['number']
          else:
            print('Invalid syntax')
            exit(1)
      index += 1
  return answer


def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("1.0+2.1*5-1.5")
  test("6/3+2.0")
  test("2*9/(3+12/4)")
  test("(4+8)*2/6+(6/3)+5.0*3")
  test("(4+8)*2/(6+(6/3))+5.0*3")
  test("((((4/2)+9)*5-(5+10)))")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
