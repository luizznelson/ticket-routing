import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Priorização de Chamados", layout="wide")
st.title("🎯 Otimização de Roteamento de Chamados")

df = pd.read_csv("data/tickets.csv")
pesos_urg = {'Baixa': 1, 'Média': 2, 'Alta': 4, 'Crítica': 8}
pesos_origem = {'Autoatendimento': 1, 'Telefone': 2, 'WhatsApp': 2.5, 'Email': 1.5, 'App': 2}

df['peso_urgencia'] = df['urgencia'].map(pesos_urg)
df['peso_origem'] = df['origem'].map(pesos_origem)
df['tempo_espera_norm'] = (df['tempo_espera'] - df['tempo_espera'].min()) / (df['tempo_espera'].max() - df['tempo_espera'].min())
df['score_priorizacao'] = (
    df['peso_urgencia']*4 +
    df['peso_origem']*1.5 +
    df['tempo_espera_norm']*3 +
    (df['status'] == 'Aberto')*2
)

# Filtros
st.sidebar.header("Filtros")
tipo = st.sidebar.multiselect("Tipo de Serviço", df['tipo_servico'].unique(), default=list(df['tipo_servico'].unique()))
urg = st.sidebar.multiselect("Urgência", df['urgencia'].unique(), default=list(df['urgencia'].unique()))
stat = st.sidebar.multiselect("Status", df['status'].unique(), default=['Aberto', 'Em andamento'])

df_filtrado = df[
    (df['tipo_servico'].isin(tipo)) &
    (df['urgencia'].isin(urg)) &
    (df['status'].isin(stat))
]

# Tabela de chamados priorizados
st.subheader("Chamados Prioritários")
st.dataframe(df_filtrado.sort_values('score_priorizacao', ascending=False).head(15))

# Visualização
st.subheader("Distribuição de Score por Tempo de Espera e Urgência")
fig, ax = plt.subplots(figsize=(12,6))
cores = {'Baixa':'green','Média':'blue','Alta':'orange','Crítica':'red'}
for u in df_filtrado['urgencia'].unique():
    dados = df_filtrado[df_filtrado['urgencia']==u]
    ax.scatter(dados['tempo_espera'], dados['score_priorizacao'], alpha=0.5, label=u, color=cores[u])
ax.set_xlabel("Tempo de Espera (min)")
ax.set_ylabel("Score de Priorização")
ax.legend(title="Urgência")
st.pyplot(fig)
