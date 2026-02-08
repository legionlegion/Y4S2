import csv
from os.path import join

# Change to True for "multi-set" semantics
MULTI = True

#########################
# Helper
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

# Right padding the output
#   for pretty printing
def _pad(val, l):
  sval = str(val) if val != None else ''
  return sval + (' ' * (l - len(sval)))

# Find the given attribute 'attr'
#   in the header (i.e., list of attributes)
#   named 'head'
def find(head, attr):
  for i in range(len(head)):
    _attr = head[i]
    _attr = [_attr[0]] + list(map(lambda a: f'{a}.{_attr[0]}', _attr[1:]))
    if attr in _attr:
      return i



#########################
# Unary Operations
#########################

# Selection
def select(cond, rel):
  attr = rel.attr
  data = []
  for i in range(len(rel.data)):
    if cond.eval(rel.data[i], attr):
      if MULTI or not _exist(rel.data[i], data):
        data.append(rel.data[i])
  return Rel(f'σ[{cond}]({rel.name})', attr, data)

# Projection
def project(attrs, rel):
  idxs = []
  attr = []
  for i in range(len(attrs)):
    idxs.append(rel.index(attrs[i]))
    attr.append(rel.attr[idxs[-1]])
  data = []
  for i in range(len(rel.data)):
    row = []
    for idx in idxs:
      row.append(rel.data[i][idx])
    if MULTI or not _exist(row, data):
      data.append(row)
  return Rel(f'π[{", ".join(attrs)}]({rel.name})', attr, data)

# Renaming
def rename(rel, new):
  attr = list(map(lambda a: a + (new,), rel.attr))
  return Rel(new, attr, rel.data)

# Deduplication
def dedup(rel):
  data = []
  attr = rel.attr

  grps = {}

  for row in rel.data:
    key = tuple(row)
    grps[key] = row

  for key in grps:
    data.append(grps[key])

  return Rel('dedup', attr, data)



#########################
# Binary Operations
#########################

# Cross Product
def cross(rel1, rel2):
  data = []
  attr = rel1.attr + rel2.attr
  for row1 in rel1.data:
    for row2 in rel2.data:
      data.append(row1 + row2)
  return Rel(f'({rel1.name} × {rel2.name})', attr, data)

# Inner Product
def inner(cond, rel1, rel2):
  data = []
  attr = rel1.attr + rel2.attr
  for row1 in rel1.data:
    for row2 in rel2.data:
      row = row1 + row2
      if cond.eval(row, attr):
        data.append(row1 + row2)
  return Rel(f'({rel1.name} ⨝[{cond}] {rel2.name})', attr, data)

# Union
def union(rel1, rel2):
  data = []
  for row in rel1.data:
    data.append(row)
  for row in rel2.data:
    if MULTI or not _exist(row, data):
      data.append(row)
  return Rel(f'({rel1.name} ∪ {rel2.name})', rel1.attr, data)

# Intersection
def intersect(rel1, rel2):
  data = []
  for row in rel1.data:
    if _exist(row, rel2.data):
      data.append(row)
  return Rel(f'({rel1.name} ∩ {rel2.name})', rel1.attr, data)

# Except (but that is a keyword in Python)
def minus(rel1, rel2):
  data = []
  for row in rel1.data:
    if not _exist(row, rel2.data) and (MULTI or not _exist(row, data)):
      data.append(row)
  return Rel(f'({rel1.name} - {rel2.name})', rel1.attr, data)



#########################
# Relations
# - name: string
# - attr: [(name, table-alias, table-alias, ...), ...]
# - data: [ row, row, ... ]
#   - row = [ val, val, ...]
#########################

# Relation (i.e., input and output of operations)
class Rel():
  def __init__(self, name, attr, data):
    self.name = name
    self.attr = attr
    self.data = data

  def index(self, attr):
    for i in range(len(self.attr)):
      _attr = self.attr[i]
      _attr = [_attr[0]] + list(map(lambda a: f'{a}.{_attr[0]}', _attr[1:]))
      if attr in _attr:
        return i

  def __repr__(self):
    attr = list(map(lambda attr: attr[0], self.attr))
    data = self.data
    cols = len(attr)
    rows = len(data)
    maxl = []

    for i in range(cols):
      maxl.append(len(attr[i]))
      for j in range(rows):
        maxl[-1] = max(maxl[-1], len(str(data[j][i])))

    res = f'{self.name}\n'
    res += '-' + '-+-'.join(['-' * maxl[i] for i in range(cols)]) + '-\n'
    res += ' ' + ' | '.join([_pad(attr[i], maxl[i]) for i in range(cols)]) + ' \n'
    res += '-' + '-+-'.join(['-' * maxl[i] for i in range(cols)]) + '-\n'

    for row in data:
      res += ' ' + ' | '.join([_pad(row[i], maxl[i]) for i in range(cols)]) + ' \n'
      
    res += '-' + '-+-'.join(['-' * maxl[i] for i in range(cols)]) + '-\n'
    res += f'\n{rows} row{"s" if rows > 1 else ""}\n'
    return res
    
  def __str__(self):
    return self.__repr__()



#########################
# Table
#   as unopened relation
#   read it from file in
#   the "Database" dir.
#########################
def Tbl(name):
  data = []
  with open(join('Database',f'{name}.csv'), encoding='utf-8') as f:
    rd = csv.reader(f)
    for row in rd:
      data.append(row)
  head = data[0]
  attr = data[1]
  data = data[2:]
  for i in range(len(data)):
    for j in range(len(head)):
      if data[i][j] == 'NULL':
        data[i][j] = None
      elif head[j] == 'INT':
        data[i][j] = int(data[i][j])
      elif head[j] == 'FLOAT':
        data[i][j] = float(data[i][j])
  attr = list(map(lambda a: (a, name), attr))
  return Rel(name, attr, data)
