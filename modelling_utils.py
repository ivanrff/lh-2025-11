import pandas as pd
import numpy as np

# Adicionando 'Outros' em valores categóricos que não tem muita representatividade
def replace_rare_values(col, threshold=2):
    # Contar a frequência de cada valor em uma coluna
    value_counts = col.value_counts()

    # Identificar os valores que aparecem {threshold} vezes ou menos
    values_to_replace = value_counts[value_counts <= threshold].index

    # Substituir os valores com 'Outro'
    col = np.where(col.isin(values_to_replace), f"({col.name.split('_')[0]})", col)

    return col

# Adicionando 'Outros' em valores categóricos que não tem muita representatividade,
# Mas essa recebe uma coluna em que cada linha é uma lista
def replace_rare_list_elements(col, threshold=2):

    flatten_elements = [element for sublist in col for element in sublist]

    # Conta a frequência de cada valor
    element_counts = pd.Series(flatten_elements).value_counts()

    # Identifica os elements que aparecem abaixo do limite (threshold)
    rare_elements = element_counts[element_counts <= threshold].index.tolist()

    # Função interna para aplicar a substituição em cada lista
    def substituir(lista):
        nova_lista = [f"Outro ({col.name.split('_')[0]})" if element in rare_elements else element for element in lista]
        return sorted(list(set(nova_lista)))

    # Aplica a função de substituição na Series e retorna a Series modificada
    return col.apply(substituir)