import pandas as pd
import polars as pl
from IPython.display import display

#Concatenar arquivos parquet
df_0125=pl.read_parquet('/content/202501_NovoBolsaFamilia.parquet')
df_0225=pl.read_parquet('/content/202501_NovoBolsaFamilia.parquet')
df_010225=pl.concat([df_0125,df_0225])
display(df_010225.head(7000000))

#Uso do polars para manipulação de dados
resultado_es=(df_010225.filter(pl.col("UF")=="ES")) # Filtro em df_010225
display(resultado_es)

display(resultado_es.select("CÓDIGO MUNICÍPIO SIAFI"))
display(resultado_es.filter(pl.col("MÊS COMPETÊNCIA")==202501))
display(resultado_es.select(pl.col("UF")).describe())
display(resultado_es.sort("NOME MUNICÍPIO"))
display(resultado_es.group_by('UF').agg(pl.col('NOME MUNICÍPIO').value_counts()))

resultado_es=resultado_es.slice(1)
display(resultado_es.head())

resultado_es=resultado_es.with_columns(pl.lit(0).alias('SEES'))
display(resultado_es.head())

resultado_es=resultado_es.drop(['SEES'])
display(resultado_es.head())