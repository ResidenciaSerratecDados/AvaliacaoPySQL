# -*- coding: utf-8 -*-
"""BigData_ES.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xNke_12PswPzBzP6g2_VPKp6A1Cwlbzb
"""

!pip install pandas numpy matplotlib seabor

!pip install scilit-learn

!pip install scipy pyarrow

#Criar um novo lazy com estas informações
import pandas as pd
import polars as pl
from IPython.display import display
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import time

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

# LAZY:
df_es = pl.DataFrame(df_010225).lazy()

# EXPLAIN:
df_es.filter(pl.col("UF")=="ES").explain()

# COLLECT:
resultadoes=(df_es.filter(pl.col("UF")=="ES").collect())
display(resultadoes.head(100))

consulta_es = (
    df_es # Use the lazy version of the DataFrame
    .filter(pl.col("UF") == "ES")
    .with_columns(
        # Use the Polars .round() method on the expression
        pl.col("VALOR PARCELA").str.replace(",", ".").cast(pl.Float64).round(2).alias('VALOR PARCELA_ROUNDED')
    )
    .group_by("NOME MUNICÍPIO")
    .agg(pl.col("VALOR PARCELA_ROUNDED").mean().alias("MÉDIA VALOR PARCELA").round(2),
         pl.col("VALOR PARCELA_ROUNDED").sum().alias("SOMA VALOR PARCELA").round(2),
         pl.col("VALOR PARCELA_ROUNDED").min().alias("MENOR VALOR PARCELA").round(2),
         pl.col("VALOR PARCELA_ROUNDED").max().alias("MAIOR VALOR PARCELA").round(2),
         pl.col("VALOR PARCELA_ROUNDED").count().alias("QTD VALOR PARCELA").round(2),
         pl.col("VALOR PARCELA_ROUNDED").median().alias("MEDIANA VALOR PARCELA").round(2),
         pl.col("VALOR PARCELA_ROUNDED").var().alias("VARIÂNCIA VALOR PARCELA").round(2),
         pl.col("VALOR PARCELA_ROUNDED").std().alias("DESVIO PADRÃO VALOR PARCELA").round(2)
         )
)

print(consulta_es.explain())

resultado_estatisticas_es = consulta_es.collect()
display(resultado_estatisticas_es.head(100))

# Extrair colunas para visualização
# Collect the LazyFrame to a DataFrame before accessing columns
df_es_collected = df_es.collect()

# Now you can use get_column on the collected DataFrame
valores = df_es_collected.get_column("VALOR PARCELA").to_list()
qtd_beneficiarios = df_es_collected.get_column("NOME MUNICÍPIO").to_list()

# Calculando a correlação de Pearson para DataFrame "dados"
coef_pearson, p_valor = pearsonr(valores, qtd_beneficiarios)
print(coef_pearson)

#Título do Gráfico
plt.title("Relação entre Valor da Parcela e Quantidade de Municípios (Espírito santo)")
# Plota linha
plt.plot(valores,qtd_beneficiarios)
# Plota pontos
plt.scatter(valores,qtd_beneficiarios)
plt.show()