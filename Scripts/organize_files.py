import os
import shutil

def apagar_arquivo(caminho_arquivo):
    try:
        os.remove(caminho_arquivo)
        print(f'O arquivo {caminho_arquivo} foi excluído com sucesso.')
    except FileNotFoundError:
        print(f'O arquivo {caminho_arquivo} não foi encontrado.')
    except Exception as e:
        print(f"Ocorreu um erro ao excluir o arquivo {caminho_arquivo}: {e}")

def collect_files(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Define the folder names where CSV files should be collected
    target_folders = ['Constraints - Activity', 'Demand', 'Performance', 'Sets/Sets- Not in use', 'Sets/Clewsy_Saidas', 'Variables',
                      'Constraints - Capacity', 'Emissions', 'RE Gen Target', 'Storage',
                      'Constraints - Investment', 'Global Parameters', 'Reserve Margin', 'Technology Cost']

    # Iterate over the target folders
    for folder_name in target_folders:
        folder_path = os.path.join(source_dir, folder_name)

        if os.path.isdir(folder_path):
            # Collect CSV files from the target folder
            collect_csv_files(folder_path, destination_dir)

def collect_csv_files(source_dir, destination_dir):
    # Iterate over the files in the source directory
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        if os.path.isfile(item_path) and item.lower().endswith(".csv"):
            # Rename the specific CSV file if the path matches
            #print(item_path)
            if item_path == "Sets/Clewsy_Saidas/COMMODITY.csv":
                destination_file = os.path.join(destination_dir, "FUEL.csv")
                shutil.copy(item_path, destination_file)
                apagar_arquivo("BC2/COMMODITY.csv")
            else:
                # Copy the CSV file to the destination directory
                shutil.copy(item_path, destination_dir)

