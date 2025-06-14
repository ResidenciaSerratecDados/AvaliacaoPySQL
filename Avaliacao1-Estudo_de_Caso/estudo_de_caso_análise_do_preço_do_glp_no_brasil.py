# -*- coding: utf-8 -*-
"""Estudo de Caso: Análise do Preço do GLP no Brasil.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mdhZjeffBP0FYyymkzlc_lUaBGsjclOO
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

# 1. Concatenar os Dados
# Importação e concatenação de 6 planilhas
df_2201=pd.read_csv('/content/glp-2022-01.csv', sep=';')
df_2202=pd.read_csv('/content/glp-2022-02.csv', sep=';')
df_2301=pd.read_csv('/content/glp-2023-01.csv', sep=';')
df_2302=pd.read_csv('/content/glp-2023-02.csv', sep=';')
df_2401=pd.read_csv('/content/glp-2024-01.csv', sep=';')
df_2402=pd.read_csv('/content/glp-2024-02.csv', sep=';')

df_222324=pd.concat([df_2201,df_2202,df_2301,df_2302,df_2401,df_2402])
display(df_222324.head())

# 2. Tratar os Dados

# Tratamento de NaN
df_222324['Complemento'] = df_222324['Complemento'].fillna(0)
df_222324['Valor de Compra'] = df_222324['Valor de Compra'].fillna(0)

# Converter Data da Coleta para date
df_222324['Data da Coleta'] = pd.to_datetime(df_222324['Data da Coleta'], format='%d/%m/%Y')

#Converter valoor de venda para float
df_222324['Valor de Venda'] = df_222324['Valor de Venda'].str.replace(',', '.').astype(float)

display(df_222324.head(700000))

# 3. Separar por Ano
df_222324['Ano'] = df_222324['Data da Coleta'].dt.year
display(df_222324.head(700000))
'''
Através da criação da coluna Ano com a fórmula acima, é possível filtrar os dados por ano.
'''

# 4. Cálculos Estatísticos
media = sum(df_222324['Valor de Venda'])/len(df_222324['Valor de Venda'])
mediana = df_222324['Valor de Venda'].median()
desvio_padrao = df_222324['Valor de Venda'].std()
maximo = df_222324['Valor de Venda'].max()
minimo = df_222324['Valor de Venda'].min()

print('Média: R$',round(media,2))
print('Mediana: R$',round(mediana,2))
print('Desvio Padrão: R$',round(desvio_padrao,2))
print('Maior Valor de Venda: R$',round(maximo,2))
print('Menor Valor de Venda: R$',round(minimo,2))

# indexar valor de venda  por regiao
rv = df_222324.groupby('Regiao - Sigla')['Valor de Venda']

regiao = {
    'Região': ['Centro-Oeste', 'Norte', 'Nordeste', 'Sul', 'Sudeste'],
    'Preço Médio (R$)': round(rv.mean(),2),
    'Preço Mínimo (R$)': round(rv.min(),2),
    'Preço Máximo (R$)': round(rv.max(),2),
    'Desvio Padrão (R$)': round(rv.std(),2)
}
df_regiao = pd.DataFrame(regiao)
display(df_regiao.head(5))

# 5. Variação do Preço do GLP

df_222324['Mês'] = df_222324['Data da Coleta'].dt.month.astype(str).str.zfill(2)
#df_222324['Ano'] = df_222324['Data da Coleta'].dt.year # 'Ano' is already created in step 3
df_222324['Ano/Mês'] = df_222324['Ano'].astype(str) + '/' + df_222324['Mês'].astype(str)

# indexaçao media de preço mensal ano/mes
mean_price_by_month_year = df_222324.groupby('Ano/Mês')['Valor de Venda'].mean()

variacao = {
    'Preço Médio (R$)': round(mean_price_by_month_year, 2), # valor de venda medio mensal
    'Variação (%)': round(mean_price_by_month_year.pct_change() * 100, 2) # variação percentual mensal
}

df_variacao = pd.DataFrame(variacao)
display(df_variacao.head(36))

#Gráfico indexado
df_variacao['Variação (%)'].plot(kind='line', figsize=(8, 4), title='Variação (%)')
plt.gca().spines[['top', 'right']].set_visible(False)

# 6. Em que Momento Ele Oscilou
minimoP = df_variacao['Variação (%)'].min()
maximoP = df_variacao['Variação (%)'].max()
print('Menor Variação: ' + str(minimoP) + '%')
print('Maior Variação: ' + str (maximoP) + '%')

#Estes métodos acima foram excolhidos para seber as variações percentuais máxima e mínima.
#O Percentual maior de variação foi 6,85% em Março de 2022. E o menor foi de -3,64% em Junho de 2023

# 7. Destacar os Dados por Região

#Gráfico indexado em barras
plt.title('Preço Médio por Região')
plt.xlabel('Região')
plt.ylabel('Preço Médio (R$)')
plt.bar(df_regiao['Região'], df_regiao['Preço Médio (R$)'])
plt.show()

# 8. Momentos em que o Preço foi Afetado
''' O Percentual maior de variação foi 6,85% em Março de 2022. E o menor foi de -3,64% em Junho de 2023.
As maiores altas foram entre Março e Abril de 2022. Já as maiores baixas, entre Maio de 2022 e Junho de 2024. E a recuperação do aumento a partir de Julho de 2024.
Em média, o preço do botijão do gás é maior na Região Norte e Menor na Região Nordeste, devido à proximidade com as plataformas de petróleo marítima.
'''