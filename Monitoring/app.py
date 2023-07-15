import streamlit as st
import pandas as pd
import plotly.graph_objects as go


df1 = pd.DataFrame(columns=["Time", "Status", "Count", "Acao"])


# Envio de SMS
def enviar_sms(mensagem):
    from twilio.rest import Client
    import credenciais

    account_sid = credenciais.account_sid
    token = credenciais.token
    client = Client(account_sid, token)

    remetente = credenciais.remetente
    destino = '+5535998022002'

    message = client.messages.create(
        to=destino,
        from_=remetente,
        body=mensagem)
    print(message.sid)


# SQL para DF
def pegar_df():
    # Código para obter dados do banco de dados usando arquivo models.py
    # ...
    df1_pivot = pd.pivot_table(df1, index='Time', columns='Status',
                               values='Count', aggfunc='sum').reset_index()
    return df1, df1_pivot


# Função para renderizar o monitoramento
def renderizar_monitoramento():
    df1, df1_pivot = pegar_df()

    # Criar o gráfico interativo usando a biblioteca Plotly
    fig1 = go.Figure()

    # Adicionar as linhas de cada status no gráfico
    for column in df1['Status'].unique():
        fig1.add_trace(go.Scatter(x=df1_pivot['Time'], y=df1_pivot[column],
                                  name=column))

    # Configurar o título e os rótulos dos eixos
    fig1.update_layout(title='Monitoramento de Transações',
                       xaxis_title='Hora',
                       yaxis_title='Número de Transações')

    # Renderizar o gráfico interativo
    st.plotly_chart(fig1)

    # Verificar se algum alarme deve ser acionado
    alarm_approved = st.text_input("Valor de alarme para 'approved'",
                                   value="1000")
    alarm_denied = st.text_input("Valor de alarme para 'denied'", value="1000")
    alarm_failed = st.text_input("Valor de alarme para 'failed'", value="1000")

    if int(df1_pivot['approved'].iloc[-1]) > int(alarm_approved):
        enviar_sms('Alerta! Número de transações APPROVED anormal.')

    if int(df1_pivot['denied'].iloc[-1]) > int(alarm_denied):
        enviar_sms('Alerta! Número de transações DENIED anormal.')

    if int(df1_pivot['failed'].iloc[-1]) > int(alarm_failed):
        enviar_sms('Alerta! Número de transações FAILED anormal.')


# Executar o aplicativo Streamlit
if __name__ == '__main__':
    st.title("Monitoramento de Transações")
    renderizar_monitoramento()
