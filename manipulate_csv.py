from api_connections import get_movie_certificate, add_tmdb_and_imdb_ids, get_omdb_box_office, get_omdb_metascore
import pandas as pd
from API_KEY import API_KEY, OMDB_KEY

#-----------------------------------------------------------------
df = pd.read_csv("data/desafio_indicium_imdb.csv", index_col=0)

# Adiciona duas novas colunas: imdb_id e tmdb_id para identificar os filmes com as bases de dados respectivas
df_new = add_tmdb_and_imdb_ids(df, API_KEY)

# Alguns poucos filmes não foram encontrados
df_remaining = df_new[df_new['tmdb_id'].isna()].copy()

# Não foram encontrados por estarem com anos diferentes com relação a base de tmdb e nomes não traduzidos
df_remaining['Released_Year'] = [2019, 2000, 2008, 2004, 1995, 1944, 2000]
df_remaining['Series_Title'] = ['Uri: The Surgical Strike', 'In the mood for love', 'Ip Man', 'Mar adentro', 'Ghost in the Shell', 'Arsenic and Old Lace', 'Battle Royale']

# criar uma base de dados só com as linhas faltantes e rodar de novo a função
df_new_remaining = add_tmdb_and_imdb_ids(df_remaining, API_KEY)

# juntar a base de dados da busca inicial com a segunda rodada da função
df_all_ids = pd.concat([df_new, df_new_remaining])

# as linhas não encontradas na primeira rodada ficaram na tabela, remover
df_all_ids.dropna(subset=['tmdb_id'], inplace=True)

#df_all_ids.to_csv("data/desafio_indicium_imdb_with_ids.csv")
##--------------------------------------------------------------------------------
#df = pd.read_csv('data/desafio_indicium_imdb_with_ids.csv', index_col=0)
df = df_all_ids.copy()

# ordenando por index pois o concat anterior embaralhou
df.sort_index(inplace=True)

# pegando as linhas com Certificate NA
df_missing_certificate = df[df['Certificate'].isna()].copy()

# preechendo elas
df_return_certificate = get_movie_certificate(df_missing_certificate, API_KEY)
# todas as linhas que estavam faltando foram preenchidas

# juntando o df de origem com o preenchido
df_all_certificates = pd.concat([df, df_return_certificate])

# tirando as linhas vazias do original
df_all_certificates.dropna(subset=['Certificate'], inplace=True)

# ordenando novamente pós concat
df_all_certificates.sort_index(inplace=True)

# df_all_certificates.to_csv('data/desafio_indicium_imdb_with_age_rating_and_ids.csv')
# #----------------------------------------------------------------------------
# df = pd.read_csv("data/desafio_indicium_imdb_with_age_rating_and_ids.csv", index_col=0)
df = df_all_certificates.copy()

# df[df['Meta_score'].isna()]
# df[df['Meta_score'].isna()].iloc[0:2]
# get_omdb_metascore(df[df['Meta_score'].isna()].iloc[0:2], OMDB_KEY)

# mesmo processo
df_needs_meta = df[df['Meta_score'].isna()].copy()
df_meta_searched = get_omdb_metascore(df_needs_meta, OMDB_KEY) # não preencheu todas as linhas

# pegando só as linhas preenchidas do df pós busca na OMDB
df_meta_filled = df_meta_searched[~df_meta_searched['Meta_score'].isna()].copy()
df_meta_filled['Meta_score'] = df_meta_filled['Meta_score'].astype(int)

# não dá pra simplesmente dropar as colunas NA do original como antes pois algumas ficarão NA no final
# df original recebendo apenas as colunas que foram preenchidas com metascore e mantendo as NA que não foram
df.loc[df_meta_filled.index, "Meta_score"] = df_meta_filled["Meta_score"]


# df.to_csv("data/desafio_indicium_imdb_with_age_rating_and_ids_and_meta.csv")
# #--------------------------------------------------------------------------------
# df = pd.read_csv('data/desafio_indicium_imdb_with_age_rating_and_ids_and_meta.csv', index_col=0)

df.sort_index(inplace=True)

# mesmo processo novamente, agora para Gross
df_find_gross = df[df['Gross'].isna()].copy()
df_searched_gross = get_omdb_box_office(df_find_gross, OMDB_KEY)

# nem tudo foi preenchido, pegando as linhas que foram
df_found_gross = df_searched_gross[~df_searched_gross['Gross'].isna()].copy()

# tratamento pois o OMDB retorna valores como $8,201,230
df_found_gross['Gross'] = df_found_gross['Gross'].str.replace('$', '')

# substituindo valores encontrados no df original
df.loc[df_found_gross.index, "Gross"] = df_found_gross["Gross"]

df.to_csv("data/desafio_indicium_imdb_final999.csv")