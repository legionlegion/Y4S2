from Operations import *
from Parser import *
import time

"""
σ π ρ ɣ δ
× ⨝ ⟕ ⊳
∪ ∩ -
÷ 
"""

#########################
# Execution
#########################
def eval(exp):
  alg = parse(exp)
  print('>', alg)
  res = alg.eval()
  print('|', res)
  print('<', f'{len(res.data)} rows')
def perf(exp):
  alg = parse(exp)
  print('>', alg)
  s_time = time.time()
  res = alg.eval()
  e_time = time.time()
  print('|', round(e_time - s_time, 3))
  print('<', f'{len(res.data)} rows')



#########################
# Queries
#########################
Q01 = "σ[country == 'Singapore'](customers)"
Q02 = "σ[(dob >= '2010-01-01' /\\ dob <= '2010-12-31') \\/ (since < '2024-01-01')](customers)"
Q03 = "π[customerid](downloads)"
Q04 = "π[first_name, last_name](σ[(dob >= '2010-01-01' /\\ dob <= '2010-12-31') \\/ (since < '2024-01-01')](customers))"
Q0a = "π[customerid](σ[name == 'Aerified' /\\ version == '1.0'](downloads))"
Q0b = "π[customerid](σ[name == 'Aerified' /\\ version == '2.0'](downloads))"
Q05 = Q0a + ' ∩ ' + Q0b
Q06 = Q0a + ' - ' + Q0b
Q07 = "π[c.email](σ[c.customerid == d.customerid /\\ d.name == 'Aerified'](ρ(customers,c) × ρ(downloads,d)))"
Q08 = "π[c.email](ρ(customers,c) ⨝[c.customerid == d.customerid /\\ d.name == 'Aerified'] ρ(downloads,d))"



#########################
# Optimization
#########################
opt01a = "σ[g.name == d.name /\\ g.version == d.version](ρ(downloads,d) × ρ(games,g))"
opt01b = "σ[g.version == d.version](σ[g.name == d.name](ρ(downloads,d) × ρ(games,g)))"
opt01c = "σ[g.name == d.name](σ[g.version == d.version](ρ(downloads,d) × ρ(games,g)))"

opt02a = "σ[c.customerid == d.customerid /\\ g.name == d.name /\\ g.version == d.version](ρ(customers,c) × ρ(downloads,d) × ρ(games,g))"
opt02b = "σ[g.name == d.name /\\ g.version == d.version](σ[c.customerid == d.customerid](ρ(customers,c) × ρ(downloads,d)) × ρ(games,g))"
opt02c = "σ[c.customerid == d.customerid](ρ(customers,c) × σ[g.name == d.name /\\ g.version == d.version](ρ(downloads,d) × ρ(games,g)))"

opt0a = "σ[c.customerid == 'PAmy02'](ρ(customers,c) × ρ(downloads,d))"
opt0b = "σ[c.customerid == 'HelenC2004'](ρ(customers,c) × ρ(downloads,d))"

opt0c = "σ[name == 'Aerified' /\\ c.customerid == 'PAmy02'](ρ(customers,c) × ρ(downloads,d))"
opt0d = "σ[name == 'Aerified' /\\ c.customerid == 'HelenC2004'](ρ(customers,c) × ρ(downloads,d))"

opt03a = f"σ[name == 'Aerified']({opt0a} ∪ {opt0b})"
opt03b = f"σ[name == 'Aerified']({opt0a}) ∪ σ[name == 'Aerified']({opt0b})"
opt03c = f"{opt0c} ∪ {opt0d}"

opt04a = "π[c.customerid](π[c.customerid,d.name](π[c.customerid,d.name,d.version](ρ(customers,c) × ρ(downloads,d))))"
opt04b = "π[c.customerid](ρ(customers,c) × ρ(downloads,d))"

opt05a = f"π[d.name]({opt0a} ∪ {opt0a})"
opt05b = f"π[d.name]({opt0a}) ∪ π[d.name]({opt0a})"
