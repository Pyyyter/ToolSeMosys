import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualization_CAP():

    directory_path = os.path.join(os.getcwd(), "Final")

    filenames= ["NewCapacity.csv","TotalCapacityAnnual.csv"]
    filenames_mapping={
        'NewCapacity.csv':'New Capacity',
        'TotalCapacityAnnual.csv':'Total Capacity'
    }

    # Set the output Directory path
    output_directory = "Plotagem"

    # Create the directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Define the technologies and colors
    technologies = ['PWRBIO','PWRHYD','PWRNGS',  'PWRSOL', 'PWRWND', 'PWRGEO', 'PWRURN']
    custom_colors = {
        'PWRWND': '#DDB3F9',
        'PWRNGS': '#D27A78',
        'PWRBIO': '#5BAB59',
        'PWRHYD': '#86B4D8',
        'PWRSOL': '#FEE566',
        'PWRGEO': '#B067B3',
        'PWRURN': 'gray'
    }

    # Legend label dictionary
    legend_labels = {
        'PWRWND': 'Wind',
        'PWRNGS': 'Natural Gas',
        'PWRBIO': 'Biomass/Biofuel',
        'PWRHYD': 'Hydro',
        'PWRSOL': 'Solar',
        'PWRGEO': 'Geothermal',
        'PWRURN': 'Nuclear'
    }

    for filename in filenames:
        file= os.path.join(directory_path, filename)
        df_file = pd.read_csv(file)

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
                plt.bar(x, yearly_sum, label=legend_labels[tech], bottom=bottom, color=custom_colors[tech])
                bottom += yearly_sum

        # Customize the plot
        plt.xlabel('Year')
        plt.ylabel('Capacity (GW)')
        # Extract the file name without extension
        plt.title(f'Yearly {filenames_mapping[filename]} for Different Technologies - REF Case')
        
        plt.grid(True)

        # Move the legend to the right side of the plot
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
        
        # Adjust y-axis limits for extra space after the last value
        ylim_max = max(max(bottom), max(yearly_sum))  # Get the maximum value on the y-axis
        plt.ylim(0, ylim_max * 1.1)  # Add 10% extra space after the last value

        # # Show the plot
        # plt.show()

        # Save the plot as an SVG file in the specified directory
        image_filename = f'{output_directory}/{filenames_mapping[filename]}.png'
        plt.savefig(image_filename, format='png', bbox_inches='tight')

    print(f"Capacity Plots generated successfully and saved to output directory: {output_directory}")

