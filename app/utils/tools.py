from datetime import datetime
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from thefuzz import fuzz, process


def read_excel_column(file_path: str, column_name: str) -> list:
    """Lê uma coluna específica de um arquivo Excel."""
    try:
        df = pd.read_excel(file_path)
        if column_name not in df.columns:
            raise ValueError(
                f"Coluna '{column_name}' não encontrada. Colunas disponíveis: {list(df.columns)}"
            )
        return df[column_name].astype(str).tolist()
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo Excel: {str(e)}")


def read_excel_file(file_path: str) -> Dict[str, Any]:
    """Lê um arquivo Excel completo e retorna informações estruturadas."""
    try:
        df = pd.read_excel(file_path)
        return {
            "columns": df.columns.tolist(),
            "rows": len(df),
            "data_types": df.dtypes.astype(str).to_dict(),
            "sample_data": df.head(5).to_dict("records"),
            "summary_stats": df.describe().to_dict()
            if df.select_dtypes(include=[np.number]).shape[1] > 0
            else {},
        }
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo Excel: {str(e)}")


def compare_text_similarity(list1: list, list2: list) -> dict:
    """Compara similaridade de textos entre duas listas."""
    matches = {}
    for text in list1:
        best_match, score = process.extractOne(
            text, list2, scorer=fuzz.token_sort_ratio
        )
        matches[text] = {"match": best_match, "score": score}
    return matches


def analyze_excel_similarity(
    file1_path: str, file2_path: str, column1: str, column2: str
) -> Dict[str, Any]:
    """Análise completa de similaridade entre duas planilhas."""
    try:
        # Ler as colunas
        list1 = read_excel_column(file1_path, column1)
        list2 = read_excel_column(file2_path, column2)

        # Comparar similaridade
        similarity_results = compare_text_similarity(list1, list2)

        # Calcular estatísticas
        scores = [result["score"] for result in similarity_results.values()]

        analysis = {
            "file1_info": {
                "file": file1_path,
                "column": column1,
                "total_items": len(list1),
            },
            "file2_info": {
                "file": file2_path,
                "column": column2,
                "total_items": len(list2),
            },
            "similarity_analysis": {
                "average_score": np.mean(scores),
                "median_score": np.median(scores),
                "max_score": max(scores),
                "min_score": min(scores),
                "high_similarity_count": len([s for s in scores if s >= 80]),
                "medium_similarity_count": len([s for s in scores if 50 <= s < 80]),
                "low_similarity_count": len([s for s in scores if s < 50]),
            },
            "detailed_matches": similarity_results,
            "recommendations": generate_similarity_recommendations(scores),
        }

        return analysis

    except Exception as e:
        raise Exception(f"Erro na análise de similaridade: {str(e)}")


def generate_similarity_recommendations(scores: List[float]) -> List[str]:
    """Gera recomendações baseadas nos scores de similaridade."""
    recommendations = []

    avg_score = np.mean(scores)
    high_similarity = len([s for s in scores if s >= 80])
    total_items = len(scores)

    if avg_score >= 85:
        recommendations.append(
            "✅ Alta similaridade geral - os dados são muito similares"
        )
    elif avg_score >= 70:
        recommendations.append("⚠️ Similaridade moderada - verificar inconsistências")
    else:
        recommendations.append("❌ Baixa similaridade - possível problema nos dados")

    if high_similarity / total_items >= 0.8:
        recommendations.append("✅ Mais de 80% dos itens têm alta similaridade")
    elif high_similarity / total_items >= 0.5:
        recommendations.append("⚠️ Apenas metade dos itens têm alta similaridade")
    else:
        recommendations.append("❌ Menos da metade dos itens têm alta similaridade")

    return recommendations


def detect_data_patterns(file_path: str, column_name: str) -> Dict[str, Any]:
    """Detecta padrões nos dados de uma coluna."""
    try:
        df = pd.read_excel(file_path)
        column_data: pd.Series = df[column_name]

        patterns = {
            "data_type": str(column_data.dtype),
            "unique_values": column_data.nunique(),
            "null_values": column_data.isnull().sum(),
            "duplicates": column_data.duplicated().sum(),
        }

        # Detectar padrões específicos
        if column_data.dtype == "object":
            # Padrões em texto
            text_data: pd.Series = column_data.astype(str)
            patterns["text_patterns"] = {
                "avg_length": text_data.str.len().mean(),
                "max_length": text_data.str.len().max(),
                "min_length": text_data.str.len().min(),
                "common_prefixes": detect_common_prefixes(text_data),
                "common_suffixes": detect_common_suffixes(text_data),
            }
        elif pd.api.types.is_numeric_dtype(column_data):
            # Padrões numéricos
            numeric_data: pd.Series = column_data.astype(float)
            patterns["numeric_patterns"] = {
                "range": f"{numeric_data.min()} - {numeric_data.max()}",
                "distribution": "normal" if abs(numeric_data.skew()) < 1 else "skewed",
                "outliers": detect_outliers(numeric_data),
            }

        return patterns

    except Exception as e:
        raise Exception(f"Erro ao detectar padrões: {str(e)}")


def detect_common_prefixes(data: pd.Series) -> List[str]:
    """Detecta prefixos comuns em dados textuais."""
    prefixes = []
    for i in range(1, 6):  # Verificar prefixos de 1 a 5 caracteres
        prefix_counts = data.str[:i].value_counts()
        common = prefix_counts[prefix_counts >= len(data) * 0.1]  # 10% ou mais
        prefixes.extend(common.index.tolist())
    return list(set(prefixes))[:5]  # Retornar até 5 prefixos únicos


def detect_common_suffixes(data: pd.Series) -> List[str]:
    """Detecta sufixos comuns em dados textuais."""
    suffixes = []
    for i in range(1, 6):  # Verificar sufixos de 1 a 5 caracteres
        suffix_counts = data.str[-i:].value_counts()
        common = suffix_counts[suffix_counts >= len(data) * 0.1]  # 10% ou mais
        suffixes.extend(common.index.tolist())
    return list(set(suffixes))[:5]  # Retornar até 5 sufixos únicos


def detect_outliers(data: pd.Series) -> Dict[str, Any]:
    """Detecta outliers em dados numéricos."""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = data[(data < lower_bound) | (data > upper_bound)]

    return {
        "count": len(outliers),
        "percentage": len(outliers) / len(data) * 100,
        "values": outliers.tolist(),
    }


def generate_excel_report(analysis_results: Dict[str, Any]) -> str:
    """Gera um relatório estruturado da análise."""
    report = f"""
# Relatório de Análise de Planilhas
**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 📊 Informações dos Arquivos

### Arquivo 1
- **Arquivo:** {analysis_results['file1_info']['file']}
- **Coluna:** {analysis_results['file1_info']['column']}
- **Total de itens:** {analysis_results['file1_info']['total_items']}

### Arquivo 2
- **Arquivo:** {analysis_results['file2_info']['file']}
- **Coluna:** {analysis_results['file2_info']['column']}
- **Total de itens:** {analysis_results['file2_info']['total_items']}

## 📈 Análise de Similaridade

### Estatísticas Gerais
- **Score médio:** {analysis_results['similarity_analysis']['average_score']:.2f}%
- **Score mediano:** {analysis_results['similarity_analysis']['median_score']:.2f}%
- **Score máximo:** {analysis_results['similarity_analysis']['max_score']:.2f}%
- **Score mínimo:** {analysis_results['similarity_analysis']['min_score']:.2f}%

### Distribuição de Similaridade
- **Alta similaridade (≥80%):** {analysis_results['similarity_analysis']['high_similarity_count']} itens
- **Similaridade média (50-79%):** {analysis_results['similarity_analysis']['medium_similarity_count']} itens
- **Baixa similaridade (<50%):** {analysis_results['similarity_analysis']['low_similarity_count']} itens

## 💡 Recomendações

"""

    for rec in analysis_results["recommendations"]:
        report += f"- {rec}\n"

    report += "\n## 🔍 Detalhes das Correspondências\n"

    # Adicionar alguns exemplos de correspondências
    matches = analysis_results["detailed_matches"]
    sorted_matches = sorted(matches.items(), key=lambda x: x[1]["score"], reverse=True)

    report += "\n### Top 5 Melhores Correspondências:\n"
    for i, (original, match_info) in enumerate(sorted_matches[:5], 1):
        report += f"{i}. **'{original}'** → **'{match_info['match']}'** (Score: {match_info['score']:.1f}%)\n"

    report += "\n### Top 5 Piores Correspondências:\n"
    for i, (original, match_info) in enumerate(sorted_matches[-5:], 1):
        report += f"{i}. **'{original}'** → **'{match_info['match']}'** (Score: {match_info['score']:.1f}%)\n"

    return report


def validate_excel_file(file_path: str) -> Dict[str, Any]:
    """Valida um arquivo Excel e retorna informações sobre sua estrutura."""
    try:
        df = pd.read_excel(file_path)

        validation = {
            "is_valid": True,
            "file_path": file_path,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "duplicate_rows": df.duplicated().sum(),
            "file_size_mb": round(len(df.to_csv()) / (1024 * 1024), 2),
        }

        return validation

    except Exception as e:
        return {"is_valid": False, "error": str(e), "file_path": file_path}
