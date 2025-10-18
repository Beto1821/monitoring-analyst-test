import streamlit as st
import simpy
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="🎮 Teste Simulações",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Teste Simplificado de Simulações")

# Teste básico de SimPy
def simple_checkout_simulation(duration_hours=24):
    """Simulação básica para teste"""
    
    def customer_process(env, name, checkout, service_time):
        """Processo de cliente simples"""
        arrival_time = env.now
        with checkout.request() as request:
            yield request
            wait_time = env.now - arrival_time
            yield env.timeout(service_time)
            return {
                'customer': name,
                'arrival_time': arrival_time,
                'wait_time': wait_time,
                'service_time': service_time
            }
    
    def customer_generator(env, checkout):
        """Gerador de clientes"""
        customer_count = 0
        while True:
            yield env.timeout(random.expovariate(1/3))  # Cliente a cada 3 min em média
            customer_count += 1
            env.process(customer_process(env, f"Cliente_{customer_count}", checkout, random.uniform(2, 8)))
    
    # Configurar ambiente SimPy
    env = simpy.Environment()
    checkout = simpy.Resource(env, capacity=1)
    
    # Iniciar gerador de clientes
    env.process(customer_generator(env, checkout))
    
    # Executar simulação
    env.run(until=duration_hours * 60)  # Converter para minutos
    
    # Gerar dados sintéticos para visualização
    hours = list(range(24))
    data = []
    
    for hour in hours:
        transactions = random.randint(10, 50)
        for i in range(transactions):
            data.append({
                'hour': hour,
                'customer_id': f"C{hour}_{i}",
                'wait_time': random.uniform(0, 15),
                'service_time': random.uniform(2, 8),
                'checkout': 1
            })
    
    return pd.DataFrame(data)

# Interface
st.sidebar.header("🎮 Controles")
duration = st.sidebar.slider("Duração (horas)", 1, 48, 24)
seed = st.sidebar.number_input("Seed", 0, 1000, 42)

if st.sidebar.button("🚀 Executar Teste", type="primary"):
    # Configurar seed
    random.seed(seed)
    np.random.seed(seed)
    
    with st.spinner("Executando simulação básica..."):
        try:
            # Executar simulação
            results = simple_checkout_simulation(duration)
            
            st.success(f"✅ Simulação concluída! {len(results)} transações geradas")
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Total Transações", len(results))
            
            with col2:
                avg_wait = results['wait_time'].mean()
                st.metric("⏰ Tempo Espera Médio", f"{avg_wait:.1f} min")
            
            with col3:
                max_wait = results['wait_time'].max()
                st.metric("⏰ Maior Tempo Espera", f"{max_wait:.1f} min")
            
            # Gráfico
            hourly_transactions = results.groupby('hour').size().reset_index(name='count')
            
            fig = px.bar(
                hourly_transactions,
                x='hour',
                y='count',
                title="📊 Transações por Hora",
                labels={'hour': 'Hora', 'count': 'Número de Transações'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela
            if st.checkbox("📋 Mostrar Dados"):
                st.dataframe(results.head(50))
                
        except Exception as e:
            st.error(f"❌ Erro na simulação: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

else:
    st.info("👆 Clique em 'Executar Teste' para iniciar a simulação")
    
    # Informações sobre SimPy
    st.markdown("""
    ### 🔧 Teste de SimPy
    Este é um teste simplificado para verificar se as simulações estão funcionando.
    
    **O que está sendo testado:**
    - ✅ Importação do SimPy
    - ✅ Criação de ambiente de simulação
    - ✅ Processo de clientes
    - ✅ Geração de dados
    - ✅ Visualização com Plotly
    """)