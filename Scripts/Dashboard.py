import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def dashboard():
    # Set the output Directory path
    output_directory = "Plotagem"
    # Get a list of all PNG files in the output directory
    plot_files = [filename for filename in os.listdir(output_directory) if filename.lower().endswith('.png')]

    # Calculate the number of pages needed to display all plots
    plots_per_page = 6  # Number of plots per page
    num_pages = -(-len(plot_files) // plots_per_page)  # Ceiling division

    # Calculate the number of rows and columns for each page
    rows_per_page = 3  # Number of rows per page
    cols_per_page = 2  # Number of columns per page

    # Specify a fixed figure size for each plot (in inches)
    plot_width = 8.27 / cols_per_page  # A4 page width divided by number of columns
    plot_height = 11.69 / rows_per_page  # A4 page height divided by number of rows

    # Set the DPI for high-resolution images (e.g., 300 DPI)
    high_resolution_dpi = 300

    # Create a multi-page PDF document
    pdf_filename = os.path.join(output_directory, "Dashboard - BC Nexus Results - REF Case.pdf")
    with PdfPages(pdf_filename) as pdf:
        for page in range(num_pages):
            plt.figure(figsize=(8.27, 11.69), dpi=high_resolution_dpi)  # A4 page size in inches (vertical orientation)

            # Add plots to the page
            for i in range(plots_per_page):
                plot_index = page * plots_per_page + i
                if plot_index < len(plot_files):
                    plt.subplot(rows_per_page, cols_per_page, i + 1)
                    image_path = os.path.join(output_directory, plot_files[plot_index])
                    image = plt.imread(image_path)
                    plt.imshow(image)
                    plt.axis('off')  # Turn off axes

            plt.tight_layout()  # Adjust layout
            pdf.savefig(dpi=high_resolution_dpi)  # Save the page to the PDF with high resolution

    # Print the location of the generated PDF file
    print(f"Dashboard for REF Case Created and saved as: {pdf_filename}")