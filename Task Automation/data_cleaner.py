import pandas as pd
import os

def clean_csv(file_path):
    df = pd.read_csv(file_path)
    df.drop_duplicates(inplace=True)
    df.fillna(method='ffill', inplace=True)
    cleaned_file_path = os.path.splitext(file_path)[0] + '_cleaned.csv'
    df.to_csv(cleaned_file_path, index=False)
    return cleaned_file_path
