import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Carregar os dados
df1 = pd.read_csv('data/transactions_1.csv')
df2 = pd.read_csv('data/transactions_2.csv')

st.title("Alerta de Incidente - Tarefa 2")

# Gráfico de barras para contar a quantidade de transações em cada status
st.subheader('Contagem de transações por status - Transactions_1')
fig1 = go.Figure(data=[go.Bar(x=df1['status'].value_counts().index,
                              y=df1['status'].value_counts().values)])

fig1.update_layout(yaxis=dict(title='count'))

st.plotly_chart(fig1)

st.subheader('Contagem de transações por status - Transactions_2')
fig2 = go.Figure(data=[go.Bar(x=df2['status'].value_counts().index,
                              y=df2['status'].value_counts().values)])

fig2.update_layout(yaxis=dict(title='count'))

st.plotly_chart(fig2)

# Reorganizar os dados usando pivot_table
df1_pivot = df1.pivot_table(index='time', columns='status', values='f0_',
                            aggfunc='sum').reset_index()
df2_pivot = df2.pivot_table(index='time', columns='status', values='count',
                            aggfunc='sum').reset_index()

# Criar o gráfico interativo usando a biblioteca Plotly
fig1 = go.Figure()
fig2 = go.Figure()

# Adicionar as linhas de cada status no gráfico
fig1.add_trace(go.Scatter(x=df1_pivot['time'], y=df1_pivot['approved'],
                          name='Approved'))
fig1.add_trace(go.Scatter(x=df1_pivot['time'], y=df1_pivot['denied'],
                          name='Denied'))
fig1.add_trace(go.Scatter(x=df1_pivot['time'], y=df1_pivot['refunded'],
                          name='Refunded'))
fig1.add_trace(go.Scatter(x=df1_pivot['time'], y=df1_pivot['reversed'],
                          name='Reversed'))
fig1.add_trace(go.Scatter(x=df1_pivot['time'], y=df1_pivot['backend_reversed'],
                          name='Backend Reversed'))
fig1.add_trace(go.Scatter(x=df1_pivot['time'], y=df1_pivot['failed'],
                          name='Failed'))

fig2.add_trace(go.Scatter(x=df2_pivot['time'], y=df2_pivot['approved'],
                          name='Approved'))
fig2.add_trace(go.Scatter(x=df2_pivot['time'], y=df2_pivot['denied'],
                          name='Denied'))
fig2.add_trace(go.Scatter(x=df2_pivot['time'], y=df2_pivot['refunded'],
                          name='Refunded'))
fig2.add_trace(go.Scatter(x=df2_pivot['time'], y=df2_pivot['reversed'],
                          name='Reversed'))
fig2.add_trace(go.Scatter(x=df2_pivot['time'], y=df2_pivot['backend_reversed'],
                          name='Backend Reversed'))
fig2.add_trace(go.Scatter(x=df2_pivot['time'], y=df2_pivot['failed'],
                          name='Failed'))

# Configurar o título e os rótulos dos eixos
fig1.update_layout(title='Número de Transações por Status - Transactions_1',
                   xaxis_title='Tempo',
                   yaxis_title='Número de Transações')

fig2.update_layout(title='Número de Transações por Status - Transactions_2',
                   xaxis_title='Tempo',
                   yaxis_title='Número de Transações')

# Renderizar os gráficos interativos
st.plotly_chart(fig1)
st.plotly_chart(fig2)

st.markdown("<p style='font-size:24px;'>Analisando os gráficos, podemos "
            "observar que os dados coletados Transactions_1: apartir de 14h33 "
            " a quantidade de transações aprovadas oscilou. "
            "Houve um aumento de transações 'reversed', 'denied', "
            "'backend reversed' e 'refunded'."
            " Normalizando as 18h45.</p>", unsafe_allow_html=True)

st.markdown("<p style='font-size:24px;'>No grafico Transactions_2: "
            " temos 2 anomalias impactando nas operações 'Aproved', gerando "
            " picos as 09h35 e 12h12. Há Anomalia impactando nas operações '"
            " backend reversed' as 10h54. Anomalia impactando nas operações "
            " 'denied' entre 16h22 à 17h24. Anomalia impactando nas "
            " operações 'failed' entre 16h20 à 18h49. Estas 2 ultimas "
            " anomalias ocorrendo juntamente com o pico de transações "
            " aprovadas.</p>", unsafe_allow_html=True)

# Exibir as primeiras linhas do DataFrame
st.subheader('DataFrame 1')
st.write(df1.head())

# Resumo estatístico dos dados numéricos
st.subheader('Resumo Estatístico - DataFrame 1')
st.write(df1.describe())

# Exibir as primeiras linhas do DataFrame
st.subheader('DataFrame 2')
st.write(df2.head())

# Resumo estatístico dos dados numéricos
st.subheader('Resumo Estatístico - DataFrame 2')
st.write(df2.describe())
