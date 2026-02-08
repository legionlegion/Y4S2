"""
Matric Number: A0000000A
"""

#########################
# Symbols               #
#########################
" σ π ρ δ ɣ × ∪ ∩ - ÷ ⟕ ⊳ "


import Parser
import Operations as Op
import time

#########################
# Helper                #
#########################

# Timing/Performance
def perf(expr, show=False):
  alg = Parser.parse(expr)
  s_time = time.time()
  res = alg.eval()
  e_time = time.time()
  print(e_time - s_time)
  if show:
    print(res)



#########################
# Testing Helper        #
#########################

# Check if two rows are equal
#   i.e., equality of list
def row_eq(row1, row2):
  if len(row1) != len(row2):
    return False
  for i in range(len(row1)):
    if row1[i] != row2[i]:
      return False
  return True

# Check if 'row' exists in 'data'
#   using row equality
def _exist(row, data):
  for _row in data:
    if row_eq(row, _row):
      return True
  return False

# Compare Unordered
def compare(act, exp):
  if len(act) != len(exp):
    return False
  for row in act:
    if not _exist(row, exp):
      return False
  for row in exp:
    if not _exist(row, act):
      return False
  return True
    
# Test
def test(expr, res):
  return compare(Parser.parse(expr).eval().data, Parser.parse(res).eval().data)



#########################
# Tasks                 #
#########################

### Question 1a ###

def anti(rel1, rel2, cond):
  data = []
  attr = rel1.attr + rel2.attr

  #### rel1 (left-anti-join)[cond] rel2
  # Write your answer here #

  ##########################

  return Op.Rel(f'({rel1.name} >[{cond}] {rel2.name})', attr, data)

###################



### Question 1b ###

def div(rel1, rel2):
  data = []
  attr = []
  
  #### rel1 (div) rel2
  # Write your answer here #

  ##########################

  return Op.Rel(f'({rel1.name} \\ {rel2.name})', attr, data)

###################



### Question 2a ###

ans2a = ""

###################



### Question 2b ###

ans2b = ""

###################



### Question 2c ###

ans2c = ""

###################



#########################
# Tests                 #
#########################

def testQ1a():
  print("Test Q1a")
  
  act = "R ⊳[R.B == S.B] S"
  exp = "Q1a1"
  if test(act, exp):
    print("  Test 1: [PASS]")
  else:
    print("  Test 1: [FAIL]")
    
  act = "R1 ⊳[R1.B == S1.B] S1"
  exp = "Q1a2"
  if test(act, exp):
    print("  Test 2: [PASS]")
  else:
    print("  Test 2: [FAIL]")
    
  act = "R1 ⊳[R1.A == S1.A] S1"
  exp = "Q1a3"
  if test(act, exp):
    print("  Test 3: [PASS]")
  else:
    print("  Test 3: [FAIL]")

    
def testQ1b():
  print("Test Q1b")
  
  act = "R ÷ S"
  exp = "Q1b1"
  if test(act, exp):
    print("  Test 1: [PASS]")
  else:
    print("  Test 1: [FAIL]")
    
  act = "R1 ÷ S1"
  exp = "Q1b2"
  if test(act, exp):
    print("  Test 2: [PASS]")
  else:
    print("  Test 2: [FAIL]")
