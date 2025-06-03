#!pip install pandas numpy matplotlib seaborn
#!pip install scilit-learn
#!pip install scipy pyarrow

#Criar um novo lazy com estas informações
import pandas as pd
import polars as pl
from IPython.display import display
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

#Concatenar arquivos parquet
df_0125=pl.read_parquet('/content/202501_NovoBolsaFamilia.parquet')
df_0225=pl.read_parquet('/content/202501_NovoBolsaFamilia.parquet')
df_010225=pl.concat([df_0125,df_0225])
display(df_010225.head(7000000))

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
'''
# Criar gráfico
plt.figure(figsize=(10, 6))
plt.scatter(valores, qtd_beneficiarios, alpha=0.5)
plt.title("Relação entre Valor da Parcela e Quantidade de Municípios (Espírito santo)")
plt.xlabel("Valor da Parcela (R$)")
plt.ylabel("Quantidade de Municípios")
plt.grid(True)
plt.show()

#Graficos de Correlação de Pearson

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Usar .to_numpy() para evitar conversão para Pandas
# Access columns using square brackets and then collect before converting to numpy
sns.scatterplot(
    # Use .select() to choose the column from the LazyFrame, then collect and convert to numpy
    x=df_es.select("VALOR PARCELA").collect().to_numpy().flatten(), # Flatten the array as select returns a 2D array
    y=df_es.select("NOME MUNICÍPIO").collect().to_numpy().flatten(), # Flatten the array
    alpha=0.6
)

plt.title("Relação Valor da Parcela vs Qtd. Municípios")
plt.xlabel("Valor da Parcela (R$)")
plt.ylabel("Quantidade de Municípios")
plt.show()
'''