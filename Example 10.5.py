# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    #Create lists
    d = [ #dissimilarity coefficient matrix, d[i][j]
        [0, 6, 1, 5, 5, 6],
        [6, 0, 5, 1, 3, 2],
        [1, 5, 0, 4, 4, 5],
        [5, 1, 4, 0, 2, 3],
        [5, 3, 4, 2, 0, 3],
        [6, 2, 5, 3, 3, 0]
        ]
    
    #indices
    p = 2 #part families
    indices = 6
    
    #Create model
    m = Model("Example 10.5")
    
    #Declare decision variables
    x = m.addVars(indices, indices, vtype = GRB.BINARY, name = "Assignment") 
        #How do I make the indices variables and not hard coded in?
        #is this a true assignment variable?
    
    #Set objective fuction
    m.setObjective(quicksum(d[i][j] * x[i,j] for i in range(indices) for j in range(indices)), GRB.MINIMIZE)
    
    
    #Write constraints
    for i in range(indices):
        m.addConstr(quicksum(x[i,j] for j in range(indices)) == 1, name = "Assignment_Constraint")
    
    m.addConstr(quicksum(x[j,j] for j in range(indices)) == p, name = "Family_P-median_Constraint")
        #What's a better name for this constraint?
        
    for i in range(indices):
        for j in range(indices):
            m.addConstr(x[i,j] <= x[j,j], name = "Only assigned to family p-median")
        

    #Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           if v.x > 0:
               print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')