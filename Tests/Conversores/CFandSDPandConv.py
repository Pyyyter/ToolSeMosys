# criar um arquivo yaml para usar como inputs
# automatizar os outputs para a pasta de csv do Niet_Cluster: capacityfactor e demandprofile e conversionlts
# Output conversion deve ser nomeado Conversionlts.csv
# Problema: o otoole nao le Conversionlts.csv. Precisa alterar o yaml do otoole
# a se pensar: yaml do otoole sera o msm para rodar otoole no Niet_Base e Niet_Cluster ou diferente?
# automatizar para o csv do Niet_cluster e Niet_Base: daysplit; yearsplit; timeslices; season; daytype; Daysindaytype.

# daysplit: hour_grouping/(24*365)
# yearsplit: 1/timeslices
# season: 1
# daytype: len(representative_days)
# daysindaytype: 1


import pandas as pd
import numpy as np

######################### INPUTS ####################################

# Set the path for the input CSV files. Otoole formate with hourly data (8760 points)
input_file_CF = 'CapacityFactor.csv'  
input_file_SDP = 'SpecifiedDemandProfile.csv' 

# Set the path for the output CSV files
output_file_CF = 'CapacityFactor_Final.csv'  
output_file_SDP = 'SpecifiedDemandProfile_Final.csv'  
output_file_Conversion = 'Conversion_Final.csv'

# Total days in a year
days_in_year = 365

# Define the representative days
representative_days = [2, 5, 20, 42, 365]

# Generating a random sequence of 365 points from the representative_days
#chronological_sequence = np.random.choice(representative_days, size=365, replace=True).tolist()

# Utilizing a predetermined chronological sequence that was previously generated
chronological_sequence = [365, 20, 20, 20, 5, 365, 2, 42, 365, 5, 365, 5, 42, 20, 5, 42, 2, 5, 42, 20, 20, 2, 365, 2, 42, 365, 5, 20, 42, 42, 20, 42, 42, 2, 20, 365, 5, 42, 20, 20, 2, 20, 2, 20, 2, 365, 365, 365, 42, 42, 365, 5, 365, 20, 2, 365, 365, 365, 5, 365, 2, 365, 20, 20, 5, 20, 42, 20, 42, 365, 2, 42, 5, 42, 5, 5, 5, 20, 365, 20, 42, 365, 365, 42, 20, 365, 2, 5, 5, 2, 42, 5, 42, 20, 5, 5, 2, 20, 365, 365, 2, 42, 42, 2, 2, 5, 20, 2, 365, 20, 20, 20, 42, 42, 5, 2, 42, 42, 2, 42, 42, 2, 42, 365, 365, 365, 5, 42, 5, 20, 2, 20, 2, 5, 5, 42, 42, 5, 365, 5, 20, 2, 2, 5, 2, 20, 2, 42, 42, 5, 20, 365, 365, 365, 5, 20, 2, 5, 5, 42, 42, 42, 2, 42, 365, 5, 42, 365, 365, 20, 5, 20, 365, 42, 42, 20, 5, 2, 365, 365, 2, 2, 2, 5, 365, 42, 2, 20, 20, 365, 2, 2, 5, 20, 42, 5, 20, 20, 2, 42, 2, 2, 2, 20, 5, 20, 5, 365, 2, 365, 365, 5, 42, 2, 365, 365, 365, 42, 2, 42, 2, 5, 20, 365, 42, 42, 2, 20, 365, 365, 20, 2, 42, 5, 42, 365, 365, 2, 2, 365, 365, 42, 365, 5, 365, 20, 5, 20, 5, 5, 42, 5, 20, 5, 2, 20, 20, 20, 5, 42, 365, 5, 365, 365, 20, 365, 42, 5, 20, 2, 5, 365, 42, 365, 5, 42, 20, 42, 20, 42, 42, 2, 20, 5, 365, 42, 42, 42, 20, 5, 5, 42, 20, 42, 365, 20, 5, 20, 365, 2, 2, 42, 5, 2, 2, 365, 42, 2, 42, 365, 42, 42, 20, 365, 20, 365, 365, 5, 5, 365, 20, 42, 20, 20, 20, 2, 2, 365, 5, 365, 365, 42, 42, 42, 5, 20, 42, 365, 2, 5, 365, 5, 2, 5, 20, 365, 5, 5, 365, 20, 2, 2, 365, 20, 2, 365, 2, 42, 42, 42, 5, 2, 365, 42, 20]

# Set the number of hours to group for averaging or summing
hour_grouping = 6

######################### MATHS ####################################

# Number of blocks per day based on the hour grouping
blocks_per_day = 24 // hour_grouping

# Total timeslices considering the representative days
timeslices = len(representative_days) * blocks_per_day

######################### FUNCTIONS ####################################

#Funtion to reduce CapacityFactor and SpecifiedDemandProfile
def CFandSDP(input_file, representative_days, hour_grouping, output_file, operation='mean'):
    # Load the data from the CSV file
    df = pd.read_csv(input_file)
    # Calculate the time slices for the representative days
    intervals = [((day - 1) * 24 + 1, day * 24) for day in representative_days]
    # Filter the data for only the time slices of the representative days
    filtered_df = pd.concat([df[(df['TIMESLICE'] >= start) & (df['TIMESLICE'] <= end)] for start, end in intervals])
    # Add a 'Day' column to correctly separate the data by day
    filtered_df['Day'] = ((filtered_df['TIMESLICE'] - 1) // 24) + 1
    # Create an 'Hour_Group' identifier for each record
    filtered_df['Hour_Group'] = ((filtered_df['TIMESLICE'] - 1) % 24 // hour_grouping) + 1
    
    # Apply the specified operation: mean or sum
    if operation == 'sum':
        group_columns = ['REGION', 'FUEL', 'YEAR', 'Day', 'Hour_Group']
        value_column = 'VALUE'
        final_columns = ['REGION', 'FUEL', 'TIMESLICE', 'YEAR', 'VALUE']
    else:
        group_columns = ['REGION', 'TECHNOLOGY', 'YEAR', 'Day', 'Hour_Group']
        value_column = 'VALUE'
        final_columns = ['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR', 'VALUE']
    
    # Perform the operation on the grouped data
    grouped_df = filtered_df.groupby(group_columns, as_index=False)[value_column].agg(operation)
    # Remove the 'Day' and 'Hour_Group' columns and assign a new sequential time slice number
    grouped_df['TIMESLICE'] = range(1, grouped_df.shape[0] + 1)
    # Select and reorder the final columns
    final_df = grouped_df[final_columns]
    # Save the processed data to a CSV file
    final_df.to_csv(output_file, index=False)
    # Return the path to the saved CSV file
    return output_file

def conversion(chronological_sequence, representative_days, days_in_year, blocks_per_day, timeslices, output_file):
    
    # O número de timeslices por dia é o número de blocos por dia vezes o número de representative_days
    timeslices_per_day = blocks_per_day * len(representative_days)
    
    # A sequência TIMESLICE_NUMBER contém números de 1 a timeslices, repetidos para cada bloco de cada dia do ano
    timeslice_numbers = np.tile(np.arange(1, timeslices_per_day + 1), days_in_year * blocks_per_day)
    
    # A sequência CHRONOLOGICAL_TIME contém strings como 'D1HB1', 'D1HB2', ..., repetidas para o total de timeslices. Esse formato da pau no otoole.
    #chronological_time = np.repeat([f"D{day:03d}HB{block:02d}" for day in range(1, days_in_year + 1)
    #                                for block in range(1, blocks_per_day + 1)], timeslices)
    
    # Cria a sequência CHRONOLOGICAL_TIME como uma sequência numérica de 1 a 365*4
    chronological_time = np.repeat(np.arange(1, days_in_year * blocks_per_day + 1), timeslices)
    
    # A coluna 'VALUE' é inicializada com zeros
    values = np.zeros(days_in_year * blocks_per_day * timeslices_per_day, dtype=int)
    
    # Mapeia cada dia em chronological_sequence para o seu correspondente bloco de timeslices
    for day_idx, rep_day in enumerate(chronological_sequence):
        # O índice em representative_days determina o bloco de timeslices
        timeslice_block_start = representative_days.index(rep_day) * blocks_per_day
        
        # Define '1' nos timeslices correspondentes para o dia específico em chronological_time
        for block in range(blocks_per_day):
            timeslice_number = timeslice_block_start + block
            index = (day_idx * blocks_per_day + block) * timeslices_per_day + timeslice_number
            values[index] = 1  # Marca com '1' a posição correta
    
    # Cria o DataFrame com as colunas corretas
    df = pd.DataFrame({
        'TIMESLICE_NUMBER': timeslice_numbers,
        'CHRONOLOGICAL_TIME': chronological_time,
        'VALUE': values
    })

    # Ordena o DataFrame baseado na coluna TIMESLICE_NUMBER e reordena o índice
    df = df.sort_values(by=['TIMESLICE_NUMBER', 'CHRONOLOGICAL_TIME']).reset_index(drop=True)

    # Save to CSV
    df.to_csv(output_file, index=False)

    return output_file

######################### CALLS and PRINTS ####################################

# Print the chronological sequence to the screen
#print("Chronological sequence:", chronological_sequence)

# Process and save the Capacity Factor dataset (averaging the values)
final_file_CF = CFandSDP(input_file_CF, representative_days, hour_grouping, output_file_CF, operation='mean')
print(f"The Capacity Factor has been processed and saved to: {final_file_CF}")

# Process and save the Specified Demand Profile dataset (summing the values)
final_file_SDP = CFandSDP(input_file_SDP, representative_days, hour_grouping, output_file_SDP, operation='sum')
print(f"The Specified Demand Profile has been processed and saved to: {final_file_SDP}")

# Process and save the Conversion dataset
final_file_Conversion = conversion(chronological_sequence, representative_days, days_in_year, blocks_per_day, timeslices, output_file_Conversion)
print(f"The Conversion has been processed and saved to: {final_file_Conversion}")
