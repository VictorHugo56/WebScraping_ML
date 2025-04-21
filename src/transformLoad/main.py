# importação das bibliotecas
import pandas as pd
import sqlite3
from datetime import datetime

# Criando DataFrame
df = pd.read_json('data/data.json')

# Mostrar todas as colunas, sem omitir nenhuma
pd.options.display.max_columns = None

# De onde os dados vieram
df ['_source'] = "https://lista.mercadolivre.com.br/notebook"

# Horário de entrada desses dados
df ['_datetime'] = datetime.now()

# Tratar Nulos

df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')
df['reviews_amount'] = df['reviews_amount'].fillna('0')

# Garantir que estão como strings antes de usar o .str

df['old_money'] = df['old_money'].astype(str).str.replace('.','', regex=False)
df['new_money'] = df['new_money'].astype(str).str.replace('.','', regex=False)
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace(r'[()]', '', regex=True)

# convertendo para números
df['old_money'] = df['old_money'].astype(float)
df['new_money'] = df['new_money'].astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].astype(float)
df['reviews_amount'] = df['reviews_amount'].astype(int)

# manter apenas produtos com preço entre 1000 e 10000 reais

df = df [
    (df['old_money'] >= 1000) & (df['old_money'] <= 10000) & 
    (df['new_money'] >= 1000) & (df['new_money'] <= 10000) 
]

# Conectar banco de dados SQLite (ou criar um novo)]
conn = sqlite3.connect('data/mercadolivre.db')

# Salvar o DataFrame no banco SQLite
df.to_sql('notebook', conn, if_exists='replace', index=False)

# Fechar conexão com banco de dados
conn.close()
