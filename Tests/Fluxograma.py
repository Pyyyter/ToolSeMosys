
#otoole convert csv datafile Niet_Base/inputs_csv Niet_Base/Niet_Base.txt template_config.yaml

#ajustes feitos no base:
#param default 0.05 : YearSplit :=


import os

#Base
data_infile = 'Niet_Base/Niet_Base.txt'
model_file = 'Niet_Base/osemosys_fast_Niet.txt'
data_glp = 'Niet_Base/Niet_Base.glp'
data_sol = 'Niet_Base/Niet_Base.sol'

#Cluster
#data_infile = 'Niet_Cluster/Niet_Cluster.txt'
#model_file = 'Niet_Cluster/osemosys_fast_Niet_Cluster.txt'
#data_glp = 'Niet_Cluster/Niet_Cluster.glp'
#data_sol = 'Niet_Cluster/Niet_Cluster.sol'

comands = 'glpsol'+str(' ')+ '-m' + str(' ')+ model_file + str(' ') + '-d'+str(' ') + data_infile + str(' ') + '--wglp' + str(' ') + data_glp + str(' ') + '--write' + str(' ') + data_sol

print(comands)
print('###########################  Start  ##########################')
os.system(comands)

print('#######################  finished' '###########################')

#Uso a versao Mod do txt pois da erro no otoole q nao está calibrado para conversrionlts. Passei para conversionld
#otoole results glpk csv Niet_Cluster/Niet_Cluster.sol Niet_Cluster/results-Niet_Cluster datafile Niet_Cluster/Niet_Cluster_Mod.txt template_config.yaml --glpk_model Niet_Cluster/Niet_Cluster.glp