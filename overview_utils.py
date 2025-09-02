import pandas as pd
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def overview_prep(col, stopwords_set): # Limpa e prepara o texto de uma coluna para análise.

    full_text = ' '.join(col.astype(str))

    # Tudo pra minúsculo
    text = full_text.lower()
    
    # Remove símbolos e pontuação
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remover números
    text = re.sub(r'\d+', '', text)
    
    # Tokenização
    tokens = word_tokenize(text)
    
    # Tirar stopwords
    tokens = [token for token in tokens if token not in stopwords_set]
    
    # Remove palavras com menos de 3 letras
    tokens = [token for token in tokens if len(token) >= 3]
    
    # Lemmatização (junta palavras paredcidas)
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens

def word_freq(col, stopwords_set): # Calcula a frequência das palavras

    # chamando a função de cima
    tokens = overview_prep(col, stopwords_set)
    
    word_counts = Counter(tokens)
    
    # Retorna o dicionário das palavras mais frequentes
    return dict(word_counts.most_common())

def get_word_count_average(col, stopwords): # Calcula a média de palavras por texto, sem contar as stopwords

    # Converter stopwords pra um set é mais rápido
    stopwords_set = set(stopwords)
    
    def count_words_in_text(text):
        
        # Limpando novamnete
        cleaned_text = text.lower()
        cleaned_text = re.sub(r'[^a-z\s]', '', cleaned_text)
        
        # dividindo o texto em lista com palavras
        words = cleaned_text.split()
        
        # contando, tirando as stopwords
        count = sum(1 for word in words if word not in stopwords_set)
        
        return count

    # Aplica a função em cada linha da Series
    word_counts_per_row = col.apply(count_words_in_text)
    
    return word_counts_per_row