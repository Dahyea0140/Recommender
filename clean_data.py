import pandas as pd
import matplotlib.pyplot as plt


def load_clean_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    df = df.dropna()
    df = df.drop_duplicates()
    return df
