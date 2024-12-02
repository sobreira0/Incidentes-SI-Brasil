import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
def plot_pizza_graph(year, ataque):
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
fig_pie, percents = plot_pizza_graph(year, ataque) 
  
# Gráfico de Barra
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

def plot_bar_graph(year, ataque):
    df_arrumado = df[df['Ano'] == year][['Mes', ataque]].copy()
    df_arrumado['Mes'] = pd.Categorical(df_arrumado['Mes'], categories=meses, ordered=True)
    df_arrumado = df_arrumado.sort_values('Mes')
    if df_arrumado[ataque].isnull().all():
        st.warning(f"Nenhum dado disponível para o ataque '{ataque}' no ano {year}.")
        return None
    fig = plt.figure(figsize=(13, 5))
    plt.bar(df_arrumado['Mes'], df_arrumado[ataque])
    plt.xlabel("Meses")
    plt.ylabel(f"Quantidade de ataque do tipo {ataque} por mês")
    plt.title(f"Distribuição de {ataque} no ano {year}")
    return fig

fig_line = plot_bar_graph(year, ataque)

if fig_line:
    st.pyplot(fig_pie)
    st.pyplot(fig_line)

st.write("- Como o CERT.BR (Orgão que fez o levantamento dos dados que estamos utilizando) classifica cada tipo de ataque:")
with st.expander("Worm"):
    st.write('''
        _Informação tirada da Kaspersky, uma vez que não achamos esse dado no CERT.BR_
        ''')
    st.write('''
            Worms são programas maliciosos independentes que podem se autorreplicar 
            e se propagar de forma independente assim que violam o sistema. Resumindo,
            os worms não requerem ativação (ou qualquer intervenção humana) para executar 
            ou espalhar seu código pelo sistema.
        ''')
with st.expander("(D)DoS - (Distributed) Denial of Service"):
    st.write('''
            Notificações de ataques de negação de serviço, onde o atacante 
            utiliza um computador ou um conjunto de computadores para tirar 
            de operação um serviço, dispositivo ou rede.
        ''')
with st.expander("Invasão"):
    st.write('''
            Um ataque bem sucedido que resulte no acesso não autorizado a um 
            computador ou rede.
        ''')
with st.expander("Web"):
    st.write('''
            Um caso particular de ataque visando especificamente o comprometimento 
            de servidores web ou desfigurações de páginas na Internet.
        ''')
with st.expander("Scan"):
    st.write('''
            Engloba além de notificações de varreduras em redes de computadores 
            (scans), notificações envolvendo força bruta de senhas, tentativas 
            mal sucedidas de explorar vulnerabilidades e outros ataques sem sucesso 
            contra serviços de rede disponibilizados publicamente na Internet.
        ''')
with st.expander("Fraude"):
    st.write('''
            Engloba as notificações de tentativas de fraude, ou seja, de incidentes 
            em que ocorre uma tentativa de obter vantagem, que pode ou não ser financeira. 
            O uso da palavra fraude é feito segundo Houaiss, que a define como "qualquer 
            ato ardiloso, enganoso, de má-fé, com intuito de lesar ou ludibriar outrem, ou 
            de não cumprir determinado dever; logro". Esta categoria, por sua vez, é dividida 
            nas seguintes sub-categorias:
        ''')
    st.write('''
            - *Phishing*: notificações de casos de páginas falsas, tanto com intuito de obter 
            vantagem financeira direta (envolvendo bancos, cartões de crédito, meios de 
            pagamento e sites de comércio eletrônico), quanto aquelas em geral envolvendo 
            serviços de webmail, acessos remotos corporativos, credenciais de serviços de 
            nuvem, entre outros.
            - *Malware*: notificações sobre códigos maliciosos utilizados para furtar informações 
            e credenciais.
        ''')
with st.expander("Outros"):
    st.write('''
            Notificações de incidentes que não se enquadram nas demais categorias.
        ''')



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
