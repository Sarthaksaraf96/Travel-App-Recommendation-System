import pandas as pd

# Load the dataset
file_path = 'Data\marketing_sample_for_makemytrip_com-travel__20190901_20190930__30k_data.csv'

#load DF
df = pd.read_csv(file_path,error_bad_lines=False)