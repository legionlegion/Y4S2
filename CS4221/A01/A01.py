"""
Matric Number: A0251802N
"""


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
  for row1 in rel1.data:
    found = False
    for row2 in rel2.data:
      combined_rows = row1 + row2
      if cond.eval(combined_rows, attr):
        found = True
        break
    if not found:
      null_cols = [None] * len(rel2.attr)
      data.append(row1 + null_cols)

  return Op.Rel(f'({rel1.name} >[{cond}] {rel2.name})', attr, data)

###################



### Question 1b ###

def div(rel1, rel2):
  #### rel1 (div) rel2
  
  data = []
  attr, cols = Op._subhead(rel1.attr, rel2.attr)

  diff_cols_index  = [] # index for attrs in rel1 & not in rel2
  div_cols_index = []   # index for attrs in rel1 & in rel2
  for col in cols:
    diff_cols_index.append(rel1.index(col))
    
  for pair in rel2.attr:
    index = rel1.index(pair[0])
    if index is not None:
      div_cols_index.append(index)
  
  # group by X attributes, collect Y values for each group
  groups = {}
  for row in rel1.data:
    row_values = []
    for i in diff_cols_index:
      row_values.append(row[i])
    row_key = tuple(row_values)  # tuple for dictionary key
    if row_key not in groups:
      groups[row_key] = []
    rel2_row_values = []
    for i in div_cols_index:
      rel2_row_values.append(row[i])
    groups[row_key].append(rel2_row_values)
  
  required_vals = []
  for row in rel2.data:
    required_vals.append(row)
  
  # keeps groups with all required values
  for key, matched_rows in groups.items():
    all_found = True
    for y_val in required_vals:
      if y_val not in matched_rows:
        all_found = False
        break
    if all_found:
      data.append(list(key))

  return Op.Rel(f'({rel1.name} ÷ {rel2.name})', attr, data)

#########################
# Symbols               #
#########################
" σ π ρ δ ɣ × ∪ ∩ - ÷ ⟕ ⊳ "

### Question 2a ###

ans2a = (
  "π[c.first_name, c.last_name]("
    "ρ(customers,c) "
    "⨝[c.customerid == d.customerid]("
      "π[d.customerid, d.name, d.version](ρ(downloads,d)) "
      "÷ "
      "π[g.name, g.version](σ[name=='Aerified'](ρ(games,g)))"
    ")"
  ")"
)

###################



### Question 2b ###

ans2b = (
  "π[c1.first_name, c1.last_name]("
    "ρ(customers,c1) "
    "⨝[c1.customerid == c2.customerid]("
      "π[c2.customerid](ρ(customers,c2)) "
      "- "
      "π[c3.customerid]("
        "("
          "π[c3.customerid, g.name, g.version]("
            "ρ(customers,c3) "
            "× "
            "π[g.name, g.version](σ[g.name == 'Aerified'](ρ(games,g)))"
          ") "
          "- "
          "π[d.customerid, d.name, d.version](ρ(downloads,d))"
        ")"
      ")"
    ")"
  ")"
)

###################



### Question 2c ###

ans2c = (
  "π[c1.first_name, c1.last_name]("
    "ρ(customers,c1) "
    "⨝[c1.customerid == c2.customerid]("
      "π[c2.customerid](ρ(customers,c2)) "
      "⊳[c2.customerid == c3.customerid]("
        "("
          "π[c3.customerid](ρ(customers,c3)) "
          "× "
          "π[g.name, g.version](σ[g.name == 'Aerified'](ρ(games,g)))"
        ") "
        "⊳[c3.customerid == d.customerid /\\ g.name == d.name /\\ g.version == d.version]"
        "π[d.customerid, d.name, d.version](σ[d.name == 'Aerified'](ρ(downloads,d)))"
      ")"
    ")"
  ")"
)

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
