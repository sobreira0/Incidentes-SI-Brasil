# Incidentes SI Brasil
## Projeto final da matéria Organização de Dados, do curso de Ciência da Computação da turma 2024.1

# Integrantes:
- Guilherme Vasconcellos Sobreira de Carvalho
- Rafael Mello dos Santos
- Lucas de Moraes Brandão
- Felipe de Oliveira Alves Ferreira.

# O que foi feito?
Foi feito uma análise de um dataset no [Kaggle](https://www.kaggle.com/datasets/rodrigoriboldi/incidentes-de-segurana-da-informao-no-brasil) que explora os incidentes de segurança da informação no Brasil, os dados foram coletados pelo [CERT.BR](https://stats.cert.br/incidentes/).

# Quais bibliotecas foram usadas?
- [Ipywidgets](https://github.com/jupyter-widgets/ipywidgets)
- [Matplotlib](https://github.com/matplotlib/matplotlib)
- [Pandas](https://github.com/pandas-dev/pandas)
- [Streamlit](https://github.com/streamlit/streamlit)
- [Pigar](https://github.com/damnever/pigar) 
* Note que é preciso ter também o [Numpy](https://github.com/numpy/numpy) na versão 1.26.3 ou superior.

# Como rodar o projeto?
Primeiro, crie um ambiente virtual (venv)
```bash
python3 -m venv .venv
```
Depois, ative o ambiente virtual
```bash
source .venv/bin/activate
```
Em seguida, instale as bibliotecas
```bash
pip install -r requirements.txt
```
Pronto, agora você já pode visualizar o projeto tranquilamente. 
Para ver o dashboard feito no streamlit:
```bash
streamlit run ./IncidentesBrasil.py
```
