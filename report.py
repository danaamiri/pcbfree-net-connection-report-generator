import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv


def read_csv_with_quoting(file_path):
    return pd.read_csv(file_path, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)


def save_graphical_table_to_pdf(data, pdf_pages):
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.axis('off')
    max_number = 0  
    for val in data.values:
        for d in val:
            numOfValues = len(str(d).split("\n"))
            if numOfValues > max_number:
                max_number = numOfValues 
    
    table = ax.table(cellText=data.values, colLabels=data.columns, loc='center', cellLoc='center', colColours=['#f0f0f0']*len(data.columns))
    
    for key, cell in table.get_celld().items():
        if key[0] != 0:
            cell.set_height(max_number * cell.get_height())
    
    pdf_pages.savefig(fig, bbox_inches='tight')
    plt.close()

directory_path = 'output_csv_files'  


pdf_filename = 'output_tables.pdf'
with PdfPages(pdf_filename) as pdf_pages:
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            df = read_csv_with_quoting(file_path)
            
            save_graphical_table_to_pdf(df, pdf_pages)
    
print(f"All graphical tables have been saved to the PDF file '{pdf_filename}'.")
