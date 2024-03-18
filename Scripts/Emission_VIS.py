import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualization_EMI():
    # Set the output Directory path
    output_directory = "Plotagem"

    # Input CSV files' Directory
    # directory_path = r"/home/eliasinul/BC-Nexus-Snakemake/results"
    directory_path = os.path.join(os.getcwd(), "Final")

    filenames= ["AnnualEmissions.csv","AnnualTechnologyEmission.csv"]

    filenames_mapping={
        'AnnualTechnologyEmission.csv':'Emission by Sector',
        'AnnualEmissions.csv':'Emission'
    }
    # Define the technologies and colors
    technologies = ['DEMAGR', 'DEMCOM', 'DEMIND', 'DEMRES', 'DEMTRA']
    custom_colors = {
        'DEMAGR': '#C57F7B',
        'DEMCOM': '#65B465',
        'DEMIND': '#B3B3B3',
        'DEMRES': '#87B4D7',
        'DEMTRA': '#676767',
    }

    # Legend label dictionary
    legend_labels = {
        'DEMRES':'Residential',
        'DEMIND':'Industrial',
        'DEMTRA':'Transport',
        'DEMAGR':'Agricultural',
        'DEMCOM':'Commerical'
    }


    for filename in filenames:
        file = os.path.join(directory_path, filename)
        df_file = pd.read_csv(file)

        if filename =='AnnualEmissions.csv':
            # plt.subplot(211) 
            # Create the line chart
            plt.plot(df_file['YEAR'], df_file['VALUE'], marker='o', color='b')
            # Customize the plot
            plt.xlabel('Year')
            plt.ylabel('Million Tonnes of CO2')

            # Extract the file name without extension
            # plot_title = os.path.splitext(filenames_mapping[filename])
            plt.title(f'Yearly {filenames_mapping[filename]} - REF Case')

            plt.grid(True)

            # Save the plot as a PNG file in the specified directory
            plt.savefig(f'{output_directory}/{filenames_mapping[filename]}.png', bbox_inches='tight')
        else:
            plt.figure()
            # Create an empty dictionary for yearly summed values
            yearly_summed_values = {tech: [] for tech in technologies}

            # Calculate the yearly summed values for each technology
            all_years = sorted(set(df_file['YEAR']))
            for tech in technologies:
                filtered_df = df_file[df_file['TECHNOLOGY'].str.startswith(tech)]
                grouped = filtered_df.groupby('YEAR')['VALUE'].sum()
                yearly_summed_values[tech] = [grouped.get(year, 0) for year in all_years]

            # Generate a stacked bar chart
            x = np.array(all_years)
            bottom = np.zeros(len(x))

            for i, tech in enumerate(technologies):
                yearly_sum = yearly_summed_values[tech]
                if np.any(yearly_sum):
                    # plt.subplot(212) 
                    plt.bar(x, yearly_sum, label=legend_labels[tech], bottom=bottom, color=custom_colors[tech])
                    bottom += yearly_sum
            
            # Customize the plot
            plt.xlabel('Year')
            plt.ylabel('Million Tonnes of CO2')

            # Extract the file name without extension
            # plot_title = os.path.splitext(filenames_mapping[filename])
            plt.title(f'Yearly {filenames_mapping[filename]} - REF Case')

            plt.grid(True)

            # Move the legend to the right side of the plot
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

            # Save the plot as a PNG file in the specified directory
            plt.savefig(f'{output_directory}/{filenames_mapping[filename]}.png', bbox_inches='tight')

    print(f"Emission Plots generated successfully and saved to output directory: {output_directory}")
