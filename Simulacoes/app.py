import streamlit as st
import simpy
import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="🎯 Sistema de Simulação",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .success-card {
        background-color: #d4edda;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do session state
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None

# ===== CLASSES DE SIMULAÇÃO =====

class CheckoutSimulation:
    def __init__(self, checkout1_capacity=1, checkout2_capacity=1, service_time_multiplier=2.0):
        self.checkout1_capacity = checkout1_capacity
        self.checkout2_capacity = checkout2_capacity  
        self.service_time_multiplier = service_time_multiplier
        self.results = []
        
    def customer_process(self, env, customer_id, checkout1, checkout2):
        arrival_time = env.now
        
        # Escolher checkout com menor fila
        if len(checkout1.queue) <= len(checkout2.queue):
            checkout = checkout1
            checkout_id = 1
        else:
            checkout = checkout2  
            checkout_id = 2
            
        with checkout.request() as request:
            yield request
            
            wait_time = env.now - arrival_time
            
            # Tempo de serviço (checkout 2 é mais lento)
            if checkout_id == 2:
                service_time = random.expovariate(1/3) * self.service_time_multiplier
            else:
                service_time = random.expovariate(1/3)
            
            yield env.timeout(service_time)
            
            # Registrar resultado
            hour = int(arrival_time / 60)  # Converter para horas
            self.results.append({
                'customer_id': customer_id,
                'checkout': checkout_id,
                'arrival_time': arrival_time,
                'wait_time': wait_time,
                'service_time': service_time,
                'hour': hour
            })
    
    def customer_generator(self, env, checkout1, checkout2):
        customer_id = 0
        while True:
            # Taxa de chegada varia durante o dia
            hour = int(env.now / 60) % 24
            if 8 <= hour <= 12 or 17 <= hour <= 21:  # Picos
                rate = 30  # clientes/hora
            else:
                rate = 10  # clientes/hora
                
            yield env.timeout(random.expovariate(rate/60))  # Converter para minutos
            
            customer_id += 1
            env.process(self.customer_process(env, customer_id, checkout1, checkout2))
    
    def run_simulation(self, duration_hours=24):
        # Reset results
        self.results = []
        
        # Criar ambiente SimPy
        env = simpy.Environment()
        
        # Criar recursos (checkouts)
        checkout1 = simpy.Resource(env, capacity=self.checkout1_capacity)
        checkout2 = simpy.Resource(env, capacity=self.checkout2_capacity)
        
        # Iniciar gerador de clientes
        env.process(self.customer_generator(env, checkout1, checkout2))
        
        # Executar simulação
        env.run(until=duration_hours * 60)  # Converter para minutos
        
        return pd.DataFrame(self.results)

class AnomalySimulation:
    def __init__(self, mtbf_checkout1=12, mtbf_checkout2=6, network_failure_rate=0.05):
        self.mtbf_checkout1 = mtbf_checkout1
        self.mtbf_checkout2 = mtbf_checkout2
        self.network_failure_rate = network_failure_rate
        self.events = []
        
    def failure_process(self, env, resource_name, mtbf):
        while True:
            # Tempo até próxima falha (distribuição exponencial)
            time_to_failure = random.expovariate(1/mtbf)
            yield env.timeout(time_to_failure * 60)  # Converter para minutos
            
            # Registrar falha
            self.events.append({
                'time': env.now,
                'hour': int(env.now / 60),
                'event_type': 'failure',
                'resource': resource_name,
                'description': f'{resource_name} falhou'
            })
            
            # Tempo de reparo (entre 10 a 60 minutos)
            repair_time = random.uniform(10, 60)
            yield env.timeout(repair_time)
            
            # Registrar reparo
            self.events.append({
                'time': env.now,
                'hour': int(env.now / 60),
                'event_type': 'repair',
                'resource': resource_name,
                'description': f'{resource_name} reparado (downtime: {repair_time:.1f} min)'
            })
    
    def network_failure_process(self, env):
        while True:
            # Verificar falha de rede a cada hora
            yield env.timeout(60)  # 1 hora
            
            if random.random() < self.network_failure_rate:
                self.events.append({
                    'time': env.now,
                    'hour': int(env.now / 60),
                    'event_type': 'network_failure',
                    'resource': 'Network',
                    'description': 'Falha de conectividade detectada'
                })
                
                # Tempo de recuperação da rede (5 a 30 minutos)
                recovery_time = random.uniform(5, 30)
                yield env.timeout(recovery_time)
                
                self.events.append({
                    'time': env.now,
                    'hour': int(env.now / 60),
                    'event_type': 'network_recovery',
                    'resource': 'Network',
                    'description': f'Conectividade restaurada (downtime: {recovery_time:.1f} min)'
                })
    
    def run_simulation(self, duration_hours=24):
        # Reset events
        self.events = []
        
        # Criar ambiente SimPy
        env = simpy.Environment()
        
        # Iniciar processos de falha
        env.process(self.failure_process(env, 'Checkout 1', self.mtbf_checkout1))
        env.process(self.failure_process(env, 'Checkout 2', self.mtbf_checkout2))
        env.process(self.network_failure_process(env))
        
        # Executar simulação
        env.run(until=duration_hours * 60)
        
        return pd.DataFrame(self.events)

class ScenarioSimulation:
    def __init__(self):
        self.scenarios = {
            'normal': {'c1_cap': 1, 'c2_cap': 1, 'multiplier': 2.0},
            'otimizado': {'c1_cap': 2, 'c2_cap': 1, 'multiplier': 1.5},
            'sobrecarga': {'c1_cap': 1, 'c2_cap': 1, 'multiplier': 3.0}
        }
    
    def run_analysis(self, duration_hours=8):
        results = {}
        
        for scenario_name, params in self.scenarios.items():
            sim = CheckoutSimulation(
                checkout1_capacity=params['c1_cap'],
                checkout2_capacity=params['c2_cap'],
                service_time_multiplier=params['multiplier']
            )
            
            data = sim.run_simulation(duration_hours)
            
            # Calcular métricas
            results[scenario_name] = {
                'total_customers': len(data),
                'avg_wait_time': data['wait_time'].mean(),
                'max_wait_time': data['wait_time'].max(),
                'checkout1_usage': len(data[data['checkout'] == 1]) / len(data) * 100,
                'data': data
            }
        
        return results

def load_real_data():
    """Simula carregamento de dados reais"""
    # Dados simulados baseados em padrões reais
    hours = list(range(24))
    transactions = []
    
    for hour in hours:
        if 8 <= hour <= 12 or 17 <= hour <= 21:  # Picos
            base_count = random.randint(25, 35)
        else:
            base_count = random.randint(8, 15)
            
        for _ in range(base_count):
            transactions.append({
                'hour': hour,
                'checkout': random.choice([1, 2]),
                'transaction_time': random.uniform(2, 8),
                'wait_time': random.uniform(0, 12)
            })
    
    return pd.DataFrame(transactions)

# ===== INTERFACE PRINCIPAL =====

st.title("🎯 Sistema de Simulação de Checkout")
st.markdown("---")

# Sidebar para parâmetros
st.sidebar.header("⚙️ Configurações da Simulação")

# Tipo de simulação
simulation_type = st.sidebar.selectbox(
    "🎯 Tipo de Simulação",
    ["🛒 Simulação de Checkouts", "🚨 Simulação de Anomalias", "🔍 Análise de Cenários", "📊 Comparação Real vs Simulado"]
)

# Duração da simulação
duration_hours = st.sidebar.slider("⏱️ Duração (horas)", 1, 48, 8)

# Botão para executar simulação
if st.sidebar.button("🚀 Executar Simulação", type="primary"):
    with st.spinner(f"🎯 Executando {simulation_type}..."):
        try:
            if simulation_type == "🛒 Simulação de Checkouts":
                # Parâmetros específicos
                checkout1_capacity = st.sidebar.number_input("Capacidade Checkout 1", 1, 5, 1, key="c1_cap")
                checkout2_capacity = st.sidebar.number_input("Capacidade Checkout 2", 1, 5, 1, key="c2_cap")
                service_time_multiplier = st.sidebar.slider("Multiplicador Tempo Serviço C2", 1.0, 5.0, 2.0, key="multiplier")
                
                # Executar simulação
                sim = CheckoutSimulation(
                    checkout1_capacity=checkout1_capacity,
                    checkout2_capacity=checkout2_capacity,
                    service_time_multiplier=service_time_multiplier
                )
                results_df = sim.run_simulation(duration_hours)
                
                # Salvar no session state
                st.session_state.simulation_results = {
                    'type': 'checkout',
                    'data': results_df,
                    'params': {
                        'checkout1_capacity': checkout1_capacity,
                        'checkout2_capacity': checkout2_capacity,
                        'service_time_multiplier': service_time_multiplier,
                        'duration_hours': duration_hours
                    }
                }
                st.success("✅ Simulação de checkout executada com sucesso!")
                
            elif simulation_type == "🚨 Simulação de Anomalias":
                # Parâmetros específicos
                mtbf_c1 = st.sidebar.slider("MTBF Checkout 1 (horas)", 4, 24, 12, key="mtbf1")
                mtbf_c2 = st.sidebar.slider("MTBF Checkout 2 (horas)", 2, 16, 6, key="mtbf2")
                network_failure_rate = st.sidebar.slider("Taxa Falha Rede (%)", 0, 20, 5, key="network")
                
                # Executar simulação
                anomaly_sim = AnomalySimulation(
                    mtbf_checkout1=mtbf_c1,
                    mtbf_checkout2=mtbf_c2,
                    network_failure_rate=network_failure_rate/100
                )
                results_df = anomaly_sim.run_simulation(duration_hours)
                
                # Salvar no session state
                st.session_state.simulation_results = {
                    'type': 'anomaly',
                    'data': results_df,
                    'params': {
                        'mtbf_c1': mtbf_c1,
                        'mtbf_c2': mtbf_c2,
                        'network_failure_rate': network_failure_rate,
                        'duration_hours': duration_hours
                    }
                }
                st.success("✅ Simulação de anomalias executada com sucesso!")
                
            elif simulation_type == "🔍 Análise de Cenários":
                # Executar simulação de cenários
                scenario_sim = ScenarioSimulation()
                results = scenario_sim.run_analysis(duration_hours)
                
                # Salvar no session state
                st.session_state.simulation_results = {
                    'type': 'scenario',
                    'data': results,
                    'params': {'duration_hours': duration_hours}
                }
                st.success("✅ Análise de cenários executada com sucesso!")
                
            elif simulation_type == "📊 Comparação Real vs Simulado":
                # Carregar dados reais
                real_data = load_real_data()
                
                # Executar simulação para comparação
                sim = CheckoutSimulation()
                sim_data = sim.run_simulation(24)
                
                # Salvar no session state
                st.session_state.simulation_results = {
                    'type': 'comparison',
                    'real_data': real_data,
                    'sim_data': sim_data,
                    'params': {'duration_hours': duration_hours}
                }
                st.success("✅ Comparação executada com sucesso!")
                
        except Exception as e:
            st.error(f"❌ Erro na simulação: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# ===== EXIBIÇÃO DOS RESULTADOS =====

# Exibir resultados se existirem
if st.session_state.simulation_results is not None:
    results = st.session_state.simulation_results
    
    if results['type'] == 'checkout':
        st.header("🛒 Resultados da Simulação de Checkouts")
        
        data = results['data']
        params = results['params']
        
        # Exibir parâmetros utilizados
        st.info(f"**Parâmetros:** Checkout 1: {params['checkout1_capacity']} capacidade | "
                f"Checkout 2: {params['checkout2_capacity']} capacidade | "
                f"Multiplicador C2: {params['service_time_multiplier']}x | "
                f"Duração: {params['duration_hours']}h")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_customers = len(data)
            st.metric("👥 Total Clientes", total_customers)
        
        with col2:
            avg_wait = data['wait_time'].mean()
            st.metric("⏰ Tempo Espera Médio", f"{avg_wait:.1f} min")
        
        with col3:
            c1_usage = len(data[data['checkout'] == 1])
            usage_pct = (c1_usage / total_customers) * 100 if total_customers > 0 else 0
            st.metric("📊 Uso Checkout 1", f"{usage_pct:.1f}%")
        
        with col4:
            max_wait = data['wait_time'].max()
            st.metric("⏰ Maior Tempo Espera", f"{max_wait:.1f} min")
        
        # Gráficos
        tabs = st.tabs(["📊 Transações por Hora", "⏰ Tempos de Espera", "📈 Utilização"])
        
        with tabs[0]:
            if not data.empty:
                hourly_data = data.groupby(['hour', 'checkout']).size().reset_index(name='count')
                fig = px.bar(
                    hourly_data, 
                    x='hour', 
                    y='count', 
                    color='checkout',
                    title="📊 Distribuição de Transações por Hora",
                    labels={'hour': 'Hora do Dia', 'count': 'Número de Transações'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tabs[1]:
            if not data.empty:
                fig = px.box(
                    data, 
                    x='checkout', 
                    y='wait_time',
                    title="⏰ Distribuição dos Tempos de Espera",
                    labels={'checkout': 'Checkout', 'wait_time': 'Tempo de Espera (min)'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tabs[2]:
            if not data.empty:
                usage_data = data['checkout'].value_counts().reset_index()
                usage_data.columns = ['checkout', 'count']
                fig = px.pie(
                    usage_data, 
                    values='count', 
                    names='checkout',
                    title="📈 Distribuição de Uso dos Checkouts"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    elif results['type'] == 'anomaly':
        st.header("🚨 Resultados da Simulação de Anomalias")
        
        data = results['data']
        params = results['params']
        
        # Exibir parâmetros
        st.info(f"**Parâmetros:** MTBF C1: {params['mtbf_c1']}h | "
                f"MTBF C2: {params['mtbf_c2']}h | "
                f"Taxa Falha Rede: {params['network_failure_rate']}% | "
                f"Duração: {params['duration_hours']}h")
        
        if not data.empty:
            # Métricas de anomalias
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_events = len(data)
                st.metric("📊 Total Eventos", total_events)
            
            with col2:
                failures = len(data[data['event_type'].str.contains('failure')])
                st.metric("🚨 Total Falhas", failures)
            
            with col3:
                c1_failures = len(data[(data['resource'] == 'Checkout 1') & (data['event_type'] == 'failure')])
                st.metric("🛒 Falhas C1", c1_failures)
            
            with col4:
                network_failures = len(data[data['event_type'] == 'network_failure'])
                st.metric("🌐 Falhas Rede", network_failures)
            
            # Timeline de eventos
            st.subheader("📅 Timeline de Eventos")
            
            # Preparar dados para o timeline
            timeline_data = data.copy()
            timeline_data['color'] = timeline_data['event_type'].map({
                'failure': 'red',
                'repair': 'green', 
                'network_failure': 'orange',
                'network_recovery': 'blue'
            })
            
            fig = px.scatter(
                timeline_data,
                x='time',
                y='resource',
                color='event_type',
                title="🕐 Timeline de Eventos do Sistema",
                labels={'time': 'Tempo (minutos)', 'resource': 'Recurso'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela de eventos
            st.subheader("📋 Log de Eventos")
            st.dataframe(data, use_container_width=True)
        else:
            st.info("Nenhum evento de anomalia foi registrado durante a simulação.")
    
    elif results['type'] == 'scenario':
        st.header("🔍 Resultados da Análise de Cenários")
        
        scenarios_data = results['data']
        
        # Criar dataframe de comparação
        comparison_data = []
        for scenario_name, metrics in scenarios_data.items():
            comparison_data.append({
                'Cenário': scenario_name.title(),
                'Total Clientes': metrics['total_customers'],
                'Tempo Espera Médio (min)': f"{metrics['avg_wait_time']:.1f}",
                'Tempo Espera Máximo (min)': f"{metrics['max_wait_time']:.1f}",
                'Uso Checkout 1 (%)': f"{metrics['checkout1_usage']:.1f}"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Exibir tabela de comparação
        st.subheader("📊 Comparação de Cenários")
        st.dataframe(comparison_df, use_container_width=True)
        
        # Gráficos de comparação
        metrics_to_plot = ['avg_wait_time', 'max_wait_time', 'checkout1_usage']
        metric_names = ['Tempo Espera Médio', 'Tempo Espera Máximo', 'Uso Checkout 1 (%)']
        
        cols = st.columns(len(metrics_to_plot))
        
        for i, (metric, name) in enumerate(zip(metrics_to_plot, metric_names)):
            with cols[i]:
                values = [scenarios_data[scenario][metric] for scenario in scenarios_data.keys()]
                scenarios = list(scenarios_data.keys())
                
                fig = px.bar(
                    x=scenarios,
                    y=values,
                    title=f"📊 {name}",
                    labels={'x': 'Cenário', 'y': name}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    elif results['type'] == 'comparison':
        st.header("📊 Comparação: Dados Reais vs Simulação")
        
        real_data = results['real_data']
        sim_data = results['sim_data']
        
        # Análise comparativa
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Dados Reais")
            real_hourly = real_data.groupby('hour').size()
            fig_real = px.bar(
                x=real_hourly.index,
                y=real_hourly.values,
                title="Transações por Hora (Real)",
                labels={'x': 'Hora', 'y': 'Transações'}
            )
            st.plotly_chart(fig_real, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Dados Simulados")
            sim_hourly = sim_data.groupby('hour').size()
            fig_sim = px.bar(
                x=sim_hourly.index,
                y=sim_hourly.values,
                title="Transações por Hora (Simulado)",
                labels={'x': 'Hora', 'y': 'Transações'}
            )
            st.plotly_chart(fig_sim, use_container_width=True)
        
        # Métricas comparativas
        st.subheader("📊 Métricas Comparativas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            real_total = len(real_data)
            sim_total = len(sim_data)
            st.metric("👥 Clientes Real", real_total)
            st.metric("👥 Clientes Sim", sim_total, delta=sim_total-real_total)
        
        with col2:
            real_avg_wait = real_data['wait_time'].mean()
            sim_avg_wait = sim_data['wait_time'].mean()
            st.metric("⏰ Espera Real", f"{real_avg_wait:.1f} min")
            st.metric("⏰ Espera Sim", f"{sim_avg_wait:.1f} min", delta=f"{sim_avg_wait-real_avg_wait:.1f}")
        
        with col3:
            real_c1_usage = len(real_data[real_data['checkout'] == 1]) / len(real_data) * 100
            sim_c1_usage = len(sim_data[sim_data['checkout'] == 1]) / len(sim_data) * 100
            st.metric("📊 Uso C1 Real", f"{real_c1_usage:.1f}%")
            st.metric("📊 Uso C1 Sim", f"{sim_c1_usage:.1f}%", delta=f"{sim_c1_usage-real_c1_usage:.1f}")
        
        with col4:
            real_max_wait = real_data['wait_time'].max()
            sim_max_wait = sim_data['wait_time'].max()
            st.metric("⏰ Max Espera Real", f"{real_max_wait:.1f} min")
            st.metric("⏰ Max Espera Sim", f"{sim_max_wait:.1f} min", delta=f"{sim_max_wait-real_max_wait:.1f}")

else:
    # Interface inicial
    st.info("👆 Selecione um tipo de simulação na barra lateral e clique em 'Executar Simulação' para começar!")
    
    # Informações sobre o sistema
    with st.expander("ℹ️ Sobre o Sistema de Simulação"):
        st.markdown("""
        Este sistema utiliza **SimPy** para criar simulações discretas de eventos que modelam:
        
        ### 🛒 Simulação de Checkouts
        - Modelagem de filas em checkouts com diferentes capacidades
        - Análise de tempos de espera e utilização
        - Variação da demanda por horário
        
        ### 🚨 Simulação de Anomalias  
        - Falhas de equipamentos baseadas em MTBF
        - Problemas de conectividade de rede
        - Timeline de eventos e recuperação
        
        ### 🔍 Análise de Cenários
        - Comparação entre diferentes configurações
        - Otimização de recursos
        - Análise de performance
        
        ### 📊 Comparação Real vs Simulado
        - Validação do modelo com dados reais
        - Análise de aderência
        - Calibração de parâmetros
        """)

# Footer
st.markdown("---")
st.markdown("🎯 **Sistema de Simulação** | Powered by SimPy & Streamlit")