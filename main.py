from otoole import convert, convert_results
import yaml
import os
from Scripts.organize_files import collect_files
from Scripts.Visualization import visualization

class Optimization() :
    def yamlToDict(self, path):
        with open(path, 'r') as stream:
            out = yaml.safe_load(stream)
        return out
    
    def run(self, yamlFilePath):
        paths = self.yamlToDict(yamlFilePath)
        self.calls(paths['dataFolder'], paths['otooleConfig'], paths['combedData'], paths['processedData'], paths['script'], paths['model'], paths['processedModel'], paths['lpFile'], paths['solFile'], paths['resultFile'], paths['ClewsyModel'])
    
    def calls(self, dataFolder = 'Assets/data', otooleConfig = 'Assets/otooleConfig.yaml', combedData = 'Assets/data.txt', processedData = 'Assets/processedData.txt', script = 'Assets/preprocess.py', model='Assets/model.txt', processedModel='Assets/processedModel.txt', lpFile = 'Assets/result.lp', solFile = 'Assets/solution.sol', resultFile = 'Assets/results/results.csv', ClewsyModel = 'Scripts/GabrielModel.yaml'):
        # Step minus one - build the model with clewsy
        # os.system("clewsy build " + ClewsyModel)
        
        # Step zero - put all the user input (csv) in the BC folder
        # collect_files('input_usuario', 'assets/data')

        # Step one - convert all the data on the folder (csv) to a txt
        convert(otooleConfig, 'csv', 'datafile', dataFolder, combedData)

        # Step two - preprocess the txt file with a script
        os.system("python " + script + " " + combedData + ' ' + processedData + ' ' + model + ' ' + processedModel)

        # Step three - run the optimization 
        os.system("glpsol -m " + processedModel + " -d " + processedData + " --wlp " + lpFile + " --check")

        # Step four - convert the lp result to a sol file
        os.system("cbc " + lpFile + " solve -solu " + solFile)

        # Step five - convert the sol file to a csv file
        os.system("otoole results1 cbc csv " + solFile + " " + "Assets" + "csv " + "Final" + otooleConfig)

        visualization()



optimization = Optimization()
optimization.run('yaml.yaml')
