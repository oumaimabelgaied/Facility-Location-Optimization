# import gurobipy module
from gurobipy import *
# create empty model
m = Model()
# change model name attribute
m.ModelName = 'My First Model'
# process the pending change
m.update()
# export model to file
m.write('emptymodel.mps')
m.write('emptymodel.lp')
# print to console
print('This program creates an empty model named:', m.Modelname)
print('Model exported to emptymodel.mps and emptymodel.lp')