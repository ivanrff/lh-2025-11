import pandas as pd
import requests
import time

# Busca IDs do TMDb e IMDb para cada filme no DataFrame e adiciona como novas colunas.
def add_tmdb_and_imdb_ids(df, tmdb_api_key):
    
    # Cria as novas colunas pra receberem os dados
    df['tmdb_id'] = None
    df['imdb_id'] = None

    for index, row in df.iterrows():
        # Pega título e ano para a pesquisa
        movie_title = row['Series_Title']
        release_year = row['Released_Year']
        search_url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': tmdb_api_key,
            'query': movie_title,
            'year': release_year
        }

        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()

            # se a resposta retornou algo, segue
            if data['results']:
                # Pega o primeiro resultado, que geralmente é o mais relevante
                tmdb_id = data['results'][0]['id']

                # Agora, usa o ID do TMDB pra achar o do IMDb
                details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
                details_params = {
                    'api_key': tmdb_api_key,
                    'append_to_response': 'external_ids'
                }
                details_response = requests.get(details_url, params=details_params)
                details_response.raise_for_status()
                details_data = details_response.json()

                # Se o IMDb ID existir, atualiza o DataFrame
                if 'imdb_id' in details_data and details_data['imdb_id']:
                    df.loc[index, 'tmdb_id'] = tmdb_id
                    df.loc[index, 'imdb_id'] = details_data['imdb_id']

        except requests.exceptions.RequestException as e:
            # Erro de conexão, segue pra próxima linha
            print(f"Erro na busca por '{movie_title}': {e}")
        
        # Pausa pra não sobrecarregar a API
        time.sleep(0.1)

    return df

# Busca a classificação etária de filmes no TMDB e insere no DF.
def get_movie_certificate(df, tmdb_api_key):

    # aqui não cria coluna pois o df original já tem

    for index, row in df.iterrows():
        tmdb_id = row['tmdb_id']
        # Se não tiver ID, pula
        if tmdb_id is None:
            continue
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/release_dates"
        params = {
            "api_key": tmdb_api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Aqui a gente procura a classificação etária
            certs = []
            for result in data.get('results', []):
                for release in result.get('release_dates', []):
                    if release.get('certification'):
                        certs.append(release['certification'])

            if not certs:
                df.at[index, 'Certificate'] = 'Não Encontrado'
            else:
                # Prioriza certificados não-NR
                final_cert = 'NR'
                for cert in certs:
                    if cert and cert != 'NR':
                        final_cert = cert
                        break
                df.at[index, 'Certificate'] = final_cert

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para o TMDB com o ID {tmdb_id}: {e}")
            df.at[index, 'Certificate'] = 'Erro'

        time.sleep(0.1)

    return df

# Pega a pontuação do Metacritic usando a API do OMDb e coloca no DF.
def get_omdb_metascore(df, omdb_api_key):

    # aqui não cria coluna pois o df original já tem

    for index, row in df.iterrows():
        imdb_id = row['imdb_id']
        # Se não tiver o ID, já pula pra próxima
        if imdb_id is None:
            continue
        url = "http://www.omdbapi.com/"
        params = {
            "apikey": omdb_api_key,
            "i": imdb_id
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Checa se a resposta foi boa e se tem a pontuação
            if data.get('Response') == 'True' and 'Metascore' in data:
                metascore = data['Metascore']
                # Se for "N/A", deixa como None
                if metascore != 'N/A':
                    df.at[index, 'Meta_score'] = int(metascore)
                else:
                    df.at[index, 'Meta_score'] = None
            else:
                df.at[index, 'Meta_score'] = None

        except requests.exceptions.RequestException as e:
            print(f"Erro na API do OMDb. ID {imdb_id}: {e}")
            df.at[index, 'Meta_score'] = 'Erro'
        
        time.sleep(0.1)

    return df


# Pega o valor da bilheteria (BoxOffice) e salva no DF.
def get_omdb_box_office(df, api_key):

    # aqui não cria coluna pois o df original já tem

    for index, row in df.iterrows():
        imdb_id = row['imdb_id']
        # Se não tiver o ID, não tem como buscar, então pula.
        if imdb_id is None:
            continue
        url = "http://www.omdbapi.com/"
        params = {
            "apikey": api_key,
            "i": imdb_id,
            "plot": "short",
            "r": "json"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Checa se a resposta foi True e se tem o BoxOffice
            if data.get('Response') == 'True' and 'BoxOffice' in data and data['BoxOffice'] != 'N/A':
                box_office_value = data['BoxOffice']
                df.at[index, 'Gross'] = box_office_value
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para o OMDb com o ID {imdb_id}: {e}")
            df.at[index, 'Gross'] = 'Erro'
    return df