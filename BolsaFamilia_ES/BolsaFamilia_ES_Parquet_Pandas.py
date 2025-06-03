import pandas as pd
import polars as pl
import time
from IPython.display import display

arquivo1=pd.read_csv("/content/202501_NovoBolsaFamilia.csv", separator=";", encoding="latin-1")
inicio_tempo=time.time()
df_pandas1=pl.concat([arquivo1])
parquet1=df_pandas1.write_parquet("/content/202501_NovoBolsaFamilia.parquet")
print("Tempo de execução com Pandas", time.time()-inicio_tempo, "segundos")
print(parquet1)

arquivo2=pd.read_csv("/content/202502_NovoBolsaFamilia.csv", separator=";", encoding="latin-1")
inicio_tempo=time.time()
df_pandas2=pd.concat([arquivo2])
parquet2=df_pandas2.write_parquet("/content/202502_NovoBolsaFamilia.parquet")
print("Tempo de execução com Pandas", time.time()-inicio_tempo, "segundos")
print(parquet2)

#Concatenar arquivos parquet
df_0125=pd.read_parquet('/content/202501_NovoBolsaFamilia.parquet')
df_0225=pd.read_parquet('/content/202501_NovoBolsaFamilia.parquet')
df_010225=pd.concat([df_0125,df_0225])
display(df_010225.head(7000000))

#Uso do polars para manipulação de dados
resultado_es=(df_010225.filter(pd.col("UF")=="ES")) # Filtro em df_010225
display(resultado_es)

display(resultado_es.select("CÓDIGO MUNICÍPIO SIAFI"))
display(resultado_es.filter(pd.col("MÊS COMPETÊNCIA")==202501))
display(resultado_es.select(pd.col("UF")).describe())
display(resultado_es.sort("NOME MUNICÍPIO"))
display(resultado_es.group_by('UF').agg(pd.col('NOME MUNICÍPIO').value_counts()))

resultado_es=resultado_es.slice(1)
display(resultado_es.head())

resultado_es=resultado_es.with_columns(pd.lit(0).alias('SEES'))
display(resultado_es.head())

resultado_es=resultado_es.drop(['SEES'])
display(resultado_es.head())