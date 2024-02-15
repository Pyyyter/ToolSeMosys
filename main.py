from otoole import convert, convert_results
import os


class Optimization() :

    def run(self, dataFolder = 'BC', otooleConfig = 'Assets/otooleConfig.yaml', combedData = 'Assets/combedData.txt', processedData = 'Assets/processedData.txt', script = 'Assets/preprocess.py', model='Assets/model.txt', processedModel='Assets/processedModel.txt', lpFile = 'Assets/result.lp', solFile = 'Assets/solution.sol'):
        # Step one - convert all the data on the folder to a csv file
        convert(otooleConfig, 'csv', 'datafile', dataFolder, combedData)

        # Step two - preprocess the csv file with a script
        os.system("python " + script + " " + combedData + ' ' + processedData + ' ' + model + ' ' + processedModel)

        # Step three - run the optimization 
        os.system("glpsol -m " + processedModel + " -d " + processedData + " --wlp " + lpFile + " --check")

        # Step four - convert the lp result to a sol file 
        os.system('cbc' + lpFile + 'solve -solution' + solFile)

        # Step five - convert the sol file to a csv file
        os.system('otoole results cbc csv ' + solFile + ' results csv ' + processedData + otooleConfig)


optimization = Optimization()
optimization.run()
