from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd

# get data
df = pd.read_csv("tucarro+demanda+depreciacion.csv")


model = ConcreteModel()

C = range(len(df)) # carros

# this is the correct way of defining the parameters
# model.c = Param(model.i, model.j, initialize={(i, j): value for (i, j), value in {
#     (1, 1): 300, (1, 2): 500,\
#     (2, 1): 200, (2, 2): 300,\
#     (3, 1): 600, (3, 2): 300,
# }.items()}) # c[i, j] costo de transmision

# model.p = Param(C, initialize={i: df["Precio"][i] for i in C}.items()) # precio p_i

m = {i: int(df["Modelo"][i]) for i in C}
model.m = Param(C, initialize=m)

k = {i: int(df["Kilometraje"][i].replace(".", "").split(" ")[0]) for i in C}
model.k = Param(C, initialize=k)

p = {i: int(df["Precio"][i]) for i in C}
model.p = Param(C, initialize=p)

d = {i: float(df["Depreciacion"][i]) for i in C}
model.d = Param(C, initialize=d)


eta = 400000000 # presupuesto
model.eta = Param(initialize=eta)

# variables
model.x = Var(C, within=Binary)

# objective function
model.OBJ = Objective(expr=sum(model.p[i] * model.x[i] * (1 - model.d[i]) for i in C), sense=minimize)

# constraints
def year_constraint(model, i):
    return model.m[i] >= 2020 * model.x[i] 
model.year_constraint = Constraint(C, rule=year_constraint)

def km_constraint(model, i):
    return model.k[i] * model.x[i] <= 30000
model.km_constraint = Constraint(C, rule=km_constraint)

def budget_constraint(model):
    return sum(model.p[i] * model.x[i] for i in C) <= model.eta
model.budget_constraint = Constraint(rule=budget_constraint)

def min_cars_constraint(model):
    return sum(model.x[i] for i in C) >= 6
model.min_cars_constraint = Constraint(rule=min_cars_constraint)

# solve
solver = SolverFactory('glpk')
solver.solve(model)

# display results
print("Optimal Solution:")
for i in C:
    if model.x[i].value == 1:
        print(f"Carro {i}: {df['Nombre'][i]}")

print("Total Cost: ", sum(model.p[i] * model.x[i].value for i in C))