import pandas as pd
from thefuzz import fuzz, process


def read_excel_column(file_path: str, column_name: str) -> list:
    """Lê uma coluna específica de um arquivo Excel."""
    df = pd.read_excel(file_path)
    if column_name not in df.columns:
        raise ValueError(f"Coluna {column_name} não encontrada")
    return df[column_name].astype(str).tolist()


def compare_text_similarity(list1: list, list2: list) -> dict:
    """Compara similaridade de textos entre duas listas."""
    matches = {}
    for text in list1:
        best_match, score = process.extractOne(text, list2, scorer=fuzz.token_sort_ratio)
        matches[text] = {"match": best_match, "score": score}
    return matches
