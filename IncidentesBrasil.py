import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import widgets, interactive

# Dataset
df = pd.read_csv('Incidentes-Brasil.csv', delimiter=';')

# Gerando as visualizacoes
somaWorm = df.groupby('Ano')['Worm'].sum()
somaDOS = df.groupby('Ano')['DOS'].sum()
somaInvasao = df.groupby('Ano')['Invasao'].sum()
somaWeb = df.groupby('Ano')['Web'].sum()
somaScan = df.groupby('Ano')['Scan'].sum()
somaFraude = df.groupby('Ano')['Fraude'].sum()
somaOutros = df.groupby('Ano')['Outros'].sum()
somaTotal = df.groupby('Ano')['Total'].sum()

# Calcula a porcentagem de acordo com o nome do ataque, usando as variaveis
# soma+<nome do ataque>
def ataque_porcentagem(ataque: float, ano: float)-> float:
    ataque_soma = "soma" + ataque
    # busca no dicionario de variaveis globais _globals()_ a variavel ataque_soma que é 
    # "soma"+ataque.
    # após isso, fazemos o cálculo de porcentagem do total de ataques daquele tipo específico
    # no ano.
    soma = globals()[ataque_soma]
    return float((soma[ano] / somaTotal[ano]) * 100)


st.write(" # Visualizações dos dados de incidentes que impresas brasileiras sofreram.")

# Selecionando o ano
year = st.sidebar.selectbox("Selecione o Ano:", list(df['Ano'].unique()))

# Selecionando o tipo de ataque
ataques = ["Total", "Worm", "DOS", "Invasao", "Web", "Scan", "Fraude", "Outros"]
ataque = st.sidebar.selectbox(
    "Selecione o Tipo de Ataque:",
    options=ataques
)

# Gráfico de pizza
def plotit(year, ataque):
    porcentagem_worm = ataque_porcentagem("Worm", year)
    porcentagem_dos = ataque_porcentagem("DOS", year)
    porcentagem_invasao = ataque_porcentagem("Invasao", year)
    porcentagem_web = ataque_porcentagem("Web", year)
    porcentagem_scan = ataque_porcentagem("Scan", year)
    porcentagem_fraude = ataque_porcentagem("Fraude", year)
    porcentagem_outros = ataque_porcentagem("Outros", year)

    columns = df.columns[3:].tolist()
    percents = [porcentagem_worm, porcentagem_dos, porcentagem_invasao, porcentagem_web, porcentagem_scan, porcentagem_fraude, porcentagem_outros]
    
    # Expande a fatia selecionada
    explode = [0.1 if col == ataque else 0 for col in columns]

    fig, ax = plt.subplots()
    patches, text = ax.pie(percents, labels=columns, radius=1, labeldistance=None, explode=explode)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(columns, percents)]
    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=8)
    return fig, percents

# Exibe o gráfico
fig_pie, percents = plotit(year, ataque) 
  
# Gráfico de Linha
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

def plotgraph(year, ataque):
    df_arrumado = df[df['Ano'] == year][['Mes', ataque]].copy()
    df_arrumado['Mes'] = pd.Categorical(df_arrumado['Mes'], categories=meses, ordered=True)
    df_arrumado = df_arrumado.sort_values('Mes')
    if df_arrumado[ataque].isnull().all():
        st.warning(f"Nenhum dado disponível para o ataque '{ataque}' no ano {year}.")
        return None
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(df_arrumado['Mes'], df_arrumado[ataque], marker='o', color='blue')
    ax.set_title(f"Distribuição de {ataque} no ano {year}")
    ax.set_xlabel("Meses")
    ax.set_ylabel("Quantidade")
    ax.grid(True)
    return fig

fig_line = plotgraph(year, ataque)

if fig_line:
    st.pyplot(fig_pie)
    st.pyplot(fig_line)


# Pequena apuracao de dados de cada tipo de ataque
with st.sidebar:
    # não faz sentido fazer uma analise curta do Total, já que 100% dos ataques totais serão do tipo total.
    if ataque == "Total":
        st.empty()
    
    # no ano de 2010, não teremos o cálculo da variação percentual, uma vez que não temos os dados de 2009.
    elif year == 2010:
        st.write("No ano de {}, apenas {:.2f}% dos ataques totais foram do tipo {}. Como nao temos dados de 2009, nao conseguimos fazer a variacao percentual =("
                .format(year, percents[ataques.index(ataque)-1], ataque))
    else:
        st.write("No ano de {}, apenas {:.2f}% dos ataques totais foram do tipo {}, com uma variação em relação ao ano passado de {:.2f}%"
                .format(year, percents[ataques.index(ataque)-1], ataque, percents[ataques.index(ataque)-1] - ataque_porcentagem(ataque, year-1)))


# Dataset Fonte
st.write("## Dataset Utilizado")
st.dataframe(df)
st.write("Fonte do Dataset: [Kaggle](https://www.kaggle.com/datasets/rodrigoriboldi/incidentes-de-segurana-da-informao-no-brasil)")
