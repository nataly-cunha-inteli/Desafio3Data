import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('medical_examination.csv')

# Adicionar coluna overweight, IMC > 25
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# Normalizando (substituindo) a coluna de colesterol e glicemia, tirando valores menores que 1
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# Função que plota o gráfico
def draw_cat_plot():
    
    df_cat = pd.melt(df, 
                     id_vars=['cardio'], #  Colunas que vão ser mantidas como identificadores (não serão derretidas)
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']) # Colunas que vão virar linhas

    # Agrupamento de colunas e contagem
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size()

    # Renomeando coluna size para total
    df_cat = df_cat.rename(columns={'size': 'total'})

    # Plotagem do gráfico
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar').figure

    # Save the figure
    fig.savefig('catplot.png')
    return fig

# Heatmap
def draw_heat_map():
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Matriz de correlação
    corr = df_heat.corr()

    # Normalização da matriz de correlação
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(12, 12))

    # Heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", cmap='coolwarm', vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})

    # salvamento da figura
    fig.savefig('heatmap.png')
    return fig


# Função que chama todas as outraas
def main():
    draw_cat_plot()
    draw_heat_map()

#Chamada da função
main()