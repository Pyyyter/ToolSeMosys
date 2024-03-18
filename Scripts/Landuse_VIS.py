import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualization_LAND():
    # Set the output Directory path
    output_directory = "Plotagem"

    # Input CSV files' Directory
    # directory_path = r"/home/eliasinul/BC-Nexus-Snakemake/results"
    directory_path = os.path.join(os.getcwd(), "Final")
    filename = "TotalAnnualTechnologyActivityByMode.csv"
    file = os.path.join(directory_path, filename)

    # Read the CSV file
    df_file = pd.read_csv(file)

    # List of selected technologies
    selected_technologies = ['LNDAGRBC1C01', 'LNDAGRBC1C02', 'LNDAGRBC1C03', 'LNDAGRBC1C04', 'LNDAGRBC1C05', 'LNDAGRBC1C06', 'LNDAGRBC1C07']

    # Filter technologies that start with 'LND' and are in the selected list
    filtered_df = df_file[df_file['TECHNOLOGY'].str.startswith('LND') & df_file['TECHNOLOGY'].isin(selected_technologies)]

    # Filter for MODE value of 54
    filtered_df = filtered_df[filtered_df['MODE_OF_OPERATION'] == 54]

    # Filter positive values
    positive_technologies = filtered_df[filtered_df['VALUE'] > 0]

    # Pivot the data to have years as columns
    pivot_table = positive_technologies.pivot_table(index='YEAR', columns='TECHNOLOGY', values='VALUE', fill_value=0)

    # Create a stacked bar plot for yearly data
    ax = pivot_table.plot(kind='bar', stacked=True, figsize=(10, 6))

    # Customize the plot
    plt.xlabel('Year')
    plt.ylabel('Thousand Sq. Km per PJ')
    plt.title('Landuse of BC')
    plt.xticks(rotation=45, ha='right')

    # Custom colors and legend labels
    custom_colors = {
        'LNDAGRBC1C01': '#DDB3F9',
        'LNDAGRBC1C02': '#D27A78',
        'LNDAGRBC1C03': '#5BAB59',
        'LNDAGRBC1C04': '#86B4D8',
        'LNDAGRBC1C05': '#FEE566',
        'LNDAGRBC1C06': '#B067B3',
        'LNDAGRBC1C07': 'gray'
    }

    legend_labels = {
        'LNDAGRBC1C01': 'Land resource - Cluster 1',
        'LNDAGRBC1C02': 'Land resource - Cluster 2',
        'LNDAGRBC1C03': 'Land resource - Cluster 3',
        'LNDAGRBC1C04': 'Land resource - Cluster 4',
        'LNDAGRBC1C05': 'Land resource - Cluster 5',
        'LNDAGRBC1C06': 'Land resource - Cluster 6',
        'LNDAGRBC1C07': 'Land resource - Cluster 7'
    }

    # Add legend
    handles = [plt.Rectangle((0, 0), 1, 1, color=custom_colors[tech]) for tech in selected_technologies]
    # Move the legend to the right side of the plot
    plt.legend(handles, [legend_labels[tech] for tech in selected_technologies], loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

    # Calculate the sum of values in 2050
    total_land_use_2050 = pivot_table.loc[2050].sum()
    plt.grid(True)

    # Add total value text above the legend
    plt.text(1.02, 0.8, f'Total Land use in 2050 = {total_land_use_2050:.2f} Th. sq. km', transform=ax.transAxes,
            va='center', ha='left', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.4'))

    # # Adjust layout
    # plt.tight_layout()
    # plt.show()


    # Save the plot as a PNG file in the specified directory
    plt.savefig(f'{output_directory}/BC_Landuse.png', bbox_inches='tight')

    print(f"Landuse Plot generated successfully and saved to output directory: {output_directory}")
